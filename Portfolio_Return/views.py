import json
import os
import io
import zipfile
import time
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse  # Import HttpResponse here
from rest_framework.views import APIView

class GeneratePortfolioReport(APIView):
    def post(self, request):
        # Check if JSON data is provided in the request
        if not request.data:
            return Response({"error": "No JSON data provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Convert null values to None in Python
        json_data = json.dumps(request.data)
        json_data = json.loads(json_data.replace("null", "None"))
        data = pd.DataFrame(json_data)
      
        data['Purchase Date'] = pd.to_datetime(data['Purchase Date'], format='%d-%m-%Y %H:%M:%S').dt.strftime('%Y-%m-%d')
        data['Sale / Valuation Date'] = pd.to_datetime(data['Sale / Valuation Date'], format='%d-%m-%Y %H:%M:%S').dt.strftime('%Y-%m-%d')

        # Ensure 'QTY' is numeric
        data['QTY'] = pd.to_numeric(data['QTY'])

        # Sort values by 'Purchase Date'
        data.sort_values(by='Purchase Date', inplace=True)

        close_prices_with_qty = pd.DataFrame()

        for index, row in data.iterrows():
            script = row['Name of Script']
            purchase_date = row['Purchase Date']
            sell_date = row['Sale / Valuation Date']
            qty = row['QTY']

            stock_data = yf.download(script, start=purchase_date, end=sell_date)
            close_price = stock_data['Close']

            close_price_with_qty = pd.DataFrame({
                script: close_price.values,
                script + '_QTY': qty,
                script + '_Value': qty * close_price,
            }, index=close_price.index)

            close_prices_with_qty = pd.concat([close_prices_with_qty, close_price_with_qty], axis=1)

        merged_df = close_prices_with_qty.groupby(level=0, axis=1).sum()
        merged_df.reset_index(inplace=True)
        close_prices_with_qty = merged_df

        ns_columns = [col for col in merged_df.columns if col.endswith('.NS')]

        ns_columns_df = merged_df[ns_columns]

        close_prices_with_qty.set_index('Date', inplace=True)

        date_column = close_prices_with_qty.index

        ns_columns_df.insert(0, 'Date', date_column)

        stocks = ns_columns_df.columns[1:]  # Pehla column 'Date' hai isliye 1 se start karo

        stock_data = {}

        for stock in stocks:
            non_zero_rows = ns_columns_df[ns_columns_df[stock] != 0]
            # Start date
            start_date = non_zero_rows['Date'].iloc[0]
            # End date
            end_date = non_zero_rows['Date'].iloc[-1]
            stock_prices = yf.download(stock, start=start_date, end=end_date)['Close']  # Stock ka close price
            stock_data[stock] = stock_prices

        stock_prices_df = pd.DataFrame(stock_data)

        stock_prices_df = stock_prices_df.reindex(close_prices_with_qty.index)

        for column in stock_prices_df.columns:

            if column in close_prices_with_qty.columns:
                close_prices_with_qty[column] = stock_prices_df[column].values

        close_prices_with_qty.reset_index(inplace=True)

        close_prices_with_qty['Portfolio_Value'] = close_prices_with_qty.filter(like='_Value').sum(axis=1)
        close_prices_with_qty['Portfolio_Return'] = close_prices_with_qty['Portfolio_Value'].pct_change()

        first_purchase_date_processed = False
        for index, row in data.iterrows():
            purchase_date = row['Purchase Date']
            purchase_price = row['Rate']
            purchase_QTY = row['QTY']

            # Convert purchase_price from string to float
            purchase_price = float(purchase_price)

            if purchase_date in data['Purchase Date'].values:
                # Convert purchase_date to a datetime object
                purchase_date = pd.to_datetime(purchase_date)

                # Initialize a flag to check if a matching row was found
                match_found = False
                day_increment = 1

                # Loop until a match is found or a reasonable limit is reached
                while not match_found and day_increment <= 30:  # Limit to 30 days
                    potential_date = purchase_date + pd.Timedelta(days=day_increment)
                    matched_rows = close_prices_with_qty[close_prices_with_qty['Date'] == potential_date]

                    if not matched_rows.empty:
                        row_index = matched_rows.index[0]
                        portfolio_value = close_prices_with_qty.loc[row_index, 'Portfolio_Value']
                        net_purchase_value = purchase_price * purchase_QTY

                        try:
                            previous_day_portfolio_value = close_prices_with_qty.iloc[row_index - 1]['Portfolio_Value']
                        except KeyError:
                            previous_day_portfolio_value = 0

                        denominator = net_purchase_value + previous_day_portfolio_value
                        result = portfolio_value / denominator / 100

                        close_prices_with_qty.at[row_index, 'Portfolio_Return'] = result

                        match_found = True
                    else:
                        day_increment += 1

                if not match_found:
                    print(f"No matching row found within 30 days for purchase date: {purchase_date}")

                # Example usage of first_purchase_date_processed
                if not first_purchase_date_processed:
                    first_purchase_date_processed = True


        sell_transactions_grouped = data[data['Sale / Valuation Date'] >= '11/07/2023'].groupby(
            'Sale / Valuation Date')

        for sell_date, group_data in sell_transactions_grouped:
            sell_date_np = np.datetime64(sell_date)

            if sell_date_np in close_prices_with_qty['Date'].values:
                row_index = close_prices_with_qty[close_prices_with_qty['Date'] == sell_date].index[0]
                portfolio_value = close_prices_with_qty.loc[row_index, 'Portfolio_Value']

                if sell_date in data['Purchase Date'].values:
                    purchase_data = data[data['Purchase Date'] == sell_date]
                    net_transaction_value = group_data['Net Sale / Market Value'].sum() - purchase_data[
                        'Net Purchase Value'].sum()
                else:
                    net_transaction_value = group_data['Net Sale / Market Value'].sum()

                try:
                    previous_day_portfolio_value = close_prices_with_qty.iloc[row_index - 1]['Portfolio_Value']
                except KeyError:
                    previous_day_portfolio_value = 0

                denominator = previous_day_portfolio_value - net_transaction_value
                result = portfolio_value / denominator / 100

                close_prices_with_qty.at[row_index, 'Portfolio_Return'] = result

        rolling_std_dev = close_prices_with_qty['Portfolio_Return'].rolling(window=30).std()
        close_prices_with_qty['Portfolio_std_dev'] = rolling_std_dev

        

        rolling_sharpe_ratio = close_prices_with_qty['Portfolio_Return'].rolling(window=30).mean() / \
                            close_prices_with_qty['Portfolio_Return'].rolling(window=30).std()
        close_prices_with_qty['Sharpe_Ratio'] = rolling_sharpe_ratio
        rolling_max = close_prices_with_qty['Portfolio_Value'].cummax()
        daily_drawdown = close_prices_with_qty['Portfolio_Value'] / rolling_max - 1
        max_daily_drawdown = daily_drawdown.expanding(min_periods=1).min()
        close_prices_with_qty['Max_Drawdown'] = max_daily_drawdown

        close_prices_with_qty.fillna(0, inplace=True)

        close_prices_with_qty.reset_index(inplace=True)


        # Filter the DataFrame
        filtered_df = merged_df[(merged_df['Date'] >= '2023-04-01') & (merged_df['Date'] <= '2024-03-31')]

        # Convert 'Date' column to datetime
        filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])

        # Calculate cumulative return
        filtered_df['Cumulative_Return'] = (1 + filtered_df['Portfolio_Return']).cumprod() - 1

        # Calculate amplified standard deviation
        amplification_factor = 50  # Adjust as needed
        filtered_df['Amplified_Std_Dev'] = filtered_df['Portfolio_std_dev'] * amplification_factor

        # Plotting
        sns.set_style("whitegrid")
        fig, ax1 = plt.subplots(figsize=(19, 10))

        # Plot Cumulative Return
        ax1.plot(filtered_df['Date'], filtered_df['Cumulative_Return'], color='blue', label='Cumulative Return')

        # Plot Amplified Standard Deviation
        ax1.plot(filtered_df['Date'], filtered_df['Amplified_Std_Dev'], color='red', linestyle='--', label='Amplified Standard Deviation')

        # Set labels and tick parameters for ax1
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Cumulative Return and Amplified Standard Deviation', color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')

        # Create a twin axis for Sharpe Ratio
        ax2 = ax1.twinx()

        # Plot Sharpe Ratio
        ax2.plot(filtered_df['Date'], filtered_df['Sharpe_Ratio'], color='green', linestyle='-.', label='Sharpe Ratio')

        # Set labels and tick parameters for ax2
        ax2.set_ylabel('Sharpe Ratio', color='green')
        ax2.tick_params(axis='y', labelcolor='green')

        # Combine legends from both axes
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', bbox_to_anchor=(0.05, 0.95))

        # Title of the plot
        plt.title('Cumulative Return, Amplified Standard Deviation, and Sharpe Ratio')

        # Display the plot
        plt.show()

        # Convert the CSV file and plot image to bytes objects
        csv_bytes = close_prices_with_qty.to_csv(index=False).encode()
        png_bytes = io.BytesIO()
        plt.savefig(png_bytes, format='png')
        png_bytes.seek(0)

        # Close the plot
        plt.close()

        # Create a zip file in memory
        zip_bytes = io.BytesIO()
        with zipfile.ZipFile(zip_bytes, 'w') as zip_file:
            zip_file.writestr('close_prices_with_qty.csv', csv_bytes)
            zip_file.writestr('plot.png', png_bytes.getvalue())

        # Set response content type to zip file
        response = HttpResponse(zip_bytes.getvalue(), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=portfolio_report.zip'

        return response