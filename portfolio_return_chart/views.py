import json
import io
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.views import APIView

class GeneratePortfolioReportChart(APIView):
    def post(self, request):
        # Check if JSON data is provided in the request
        if not request.data:
            return Response({"error": "No JSON data provided."}, status=status.HTTP_400_BAD_REQUEST)

        # Convert null values to None in Python
        json_data = json.dumps(request.data)
        json_data = json.loads(json_data.replace("null", "None"))
        data = pd.DataFrame(json_data)

        # Check for necessary columns
        required_columns = ['Name of Script', 'Purchase Date', 'Sale / Valuation Date', 'QTY', 'Rate']
        for col in required_columns:
            if col not in data.columns:
                return Response({"error": f"Missing column: {col}"}, status=status.HTTP_400_BAD_REQUEST)

        # Convert date columns to datetime
        data['Purchase Date'] = pd.to_datetime(data['Purchase Date'], format='%d-%m-%Y %H:%M:%S', errors='coerce')
        data['Sale / Valuation Date'] = pd.to_datetime(data['Sale / Valuation Date'], format='%d-%m-%Y %H:%M:%S', errors='coerce')

        # Handle conversion of 'QTY' and 'Rate' columns
        data['QTY'] = pd.to_numeric(data['QTY'], errors='coerce')
        data['Rate'] = pd.to_numeric(data['Rate'], errors='coerce')

        # Drop rows with missing values after conversion
        data.dropna(inplace=True)

        # Sort values by 'Purchase Date'
        data.sort_values(by='Purchase Date', inplace=True)

        close_prices_with_qty = pd.DataFrame()

        for index, row in data.iterrows():
            script = row['Name of Script']
            purchase_date = row['Purchase Date']
            sell_date = row['Sale / Valuation Date']
            qty = row['QTY']

            stock_data = yf.download(script, start=purchase_date, end=sell_date)
            if stock_data.empty:
                continue

            close_price = stock_data['Close']

            close_price_with_qty = pd.DataFrame({
                script: close_price.values,
                script + '_QTY': qty,
                script + '_Value': qty * close_price,
            }, index=close_price.index)

            close_prices_with_qty = pd.concat([close_prices_with_qty, close_price_with_qty], axis=1)

        # Group by date and sum
        merged_df = close_prices_with_qty.groupby(level=0, axis=1).sum()
        merged_df.reset_index(inplace=True)
        close_prices_with_qty = merged_df

        # Filter columns that end with '.NS'
        ns_columns = [col for col in merged_df.columns if col.endswith('.NS')]

        if not ns_columns:
            return Response({"error": "No stock data with '.NS' suffix found."}, status=status.HTTP_400_BAD_REQUEST)

        ns_columns_df = merged_df[ns_columns]
        close_prices_with_qty.set_index('Date', inplace=True)

        date_column = close_prices_with_qty.index
        ns_columns_df.insert(0, 'Date', date_column)

        stocks = ns_columns_df.columns[1:]

        stock_data = {}
        for stock in stocks:
            non_zero_rows = ns_columns_df[ns_columns_df[stock] != 0]
            if not non_zero_rows.empty:
                start_date = non_zero_rows['Date'].iloc[0]
                end_date = non_zero_rows['Date'].iloc[-1]
                stock_prices = yf.download(stock, start=start_date, end=end_date)['Close']
                stock_data[stock] = stock_prices

        stock_prices_df = pd.DataFrame(stock_data)
        stock_prices_df = stock_prices_df.reindex(close_prices_with_qty.index)

        for column in stock_prices_df.columns:
            if column in close_prices_with_qty.columns:
                close_prices_with_qty[column] = stock_prices_df[column].values

        close_prices_with_qty.reset_index(inplace=True)

        # Ensure necessary columns exist before calculations
        if 'Rate' not in data.columns:
            return Response({"error": "'Rate' column is required for calculation."}, status=status.HTTP_400_BAD_REQUEST)

        close_prices_with_qty['Portfolio_Value'] = close_prices_with_qty.filter(like='_Value').sum(axis=1)
        close_prices_with_qty['Portfolio_Return'] = close_prices_with_qty['Portfolio_Value'].pct_change()

        first_purchase_date_processed = False
        for index, row in data.iterrows():
            purchase_date = row['Purchase Date']
            purchase_price = row['Rate']
            purchase_QTY = row['QTY']

            purchase_price = float(purchase_price)

            if purchase_date in data['Purchase Date'].values:
                purchase_date = pd.to_datetime(purchase_date)

                match_found = False
                day_increment = 1

                while not match_found and day_increment <= 30:
                    potential_date = purchase_date + pd.Timedelta(days=day_increment)
                    matched_rows = close_prices_with_qty[close_prices_with_qty['Date'] == potential_date]

                    if not matched_rows.empty:
                        row_index = matched_rows.index[0]
                        portfolio_value = close_prices_with_qty.loc[row_index, 'Portfolio_Value']
                        net_purchase_value = purchase_price * purchase_QTY

                        previous_day_portfolio_value = close_prices_with_qty.iloc[row_index - 1]['Portfolio_Value'] if row_index > 0 else 0

                        denominator = net_purchase_value + previous_day_portfolio_value
                        result = portfolio_value / denominator / 100

                        close_prices_with_qty.at[row_index, 'Portfolio_Return'] = result

                        match_found = True
                    else:
                        day_increment += 1

                if not match_found:
                    print(f"No matching row found within 30 days for purchase date: {purchase_date}")

                if not first_purchase_date_processed:
                    first_purchase_date_processed = True

        sell_transactions_grouped = data[data['Sale / Valuation Date'] >= '11/07/2023'].groupby('Sale / Valuation Date')

        for sell_date, group_data in sell_transactions_grouped:
            sell_date_np = np.datetime64(sell_date)

            if sell_date_np in close_prices_with_qty['Date'].values:
                row_index = close_prices_with_qty[close_prices_with_qty['Date'] == sell_date].index[0]
                portfolio_value = close_prices_with_qty.loc[row_index, 'Portfolio_Value']

                if sell_date in data['Purchase Date'].values:
                    purchase_data = data[data['Purchase Date'] == sell_date]
                    group_data['Net Sale / Market Value'] = group_data['Net Sale / Market Value'].astype(float)
                    purchase_data['Net Purchase Value'] = purchase_data['Net Purchase Value'].astype(float)
                    net_transaction_value = group_data['Net Sale / Market Value'].sum() - purchase_data['Net Purchase Value'].sum()
                else:
                    net_transaction_value = group_data['Net Sale / Market Value'].sum()

                previous_day_portfolio_value = close_prices_with_qty.iloc[row_index - 1]['Portfolio_Value'] if row_index > 0 else 0

                net_transaction_value = float(net_transaction_value)

                denominator = previous_day_portfolio_value - net_transaction_value
                result = portfolio_value / denominator / 100

                close_prices_with_qty.at[row_index, 'Portfolio_Return'] = result

        rolling_std_dev = close_prices_with_qty['Portfolio_Return'].rolling(window=30).std()
        close_prices_with_qty['Portfolio_std_dev'] = rolling_std_dev

        rolling_sharpe_ratio = close_prices_with_qty['Portfolio_Return'].rolling(window=30).mean() / close_prices_with_qty['Portfolio_Return'].rolling(window=30).std()
        close_prices_with_qty['Sharpe_Ratio'] = rolling_sharpe_ratio
        rolling_max = close_prices_with_qty['Portfolio_Value'].cummax()
        daily_drawdown = close_prices_with_qty['Portfolio_Value'] / rolling_max - 1
        max_daily_drawdown = daily_drawdown.expanding(min_periods=1).min()
        close_prices_with_qty['Max_Drawdown'] = max_daily_drawdown

        close_prices_with_qty.fillna(0, inplace=True)

        close_prices_with_qty.reset_index(inplace=True)

        # Filter the DataFrame
        filtered_df = merged_df[(merged_df['Date'] >= '2023-04-01') & (merged_df['Date'] <= '2024-03-31')]

        filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])

        filtered_df['Cumulative_Return'] = (1 + filtered_df['Portfolio_Return']).cumprod() - 1

        amplification_factor = 50
        filtered_df['Amplified_Std_Dev'] = filtered_df['Portfolio_std_dev'] * amplification_factor

        sns.set_style("whitegrid")
        fig, ax1 = plt.subplots(figsize=(19, 10))

        ax1.plot(filtered_df['Date'], filtered_df['Cumulative_Return'], color='blue', label='Cumulative Return')
        ax1.plot(filtered_df['Date'], filtered_df['Amplified_Std_Dev'], color='red', linestyle='--', label='Amplified Standard Deviation')

        ax1.set_xlabel('Date')
        ax1.set_ylabel('Cumulative Return and Amplified Standard Deviation', color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')

        ax2 = ax1.twinx()
        ax2.plot(filtered_df['Date'], filtered_df['Sharpe_Ratio'], color='green', linestyle='-.', label='Sharpe Ratio')
        ax2.set_ylabel('Sharpe Ratio', color='green')
        ax2.tick_params(axis='y', labelcolor='green')

        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', bbox_to_anchor=(0.05, 0.95))

        plt.title('Cumulative Return, Amplified Standard Deviation, and Sharpe Ratio')
        plt.show()

        png_bytes = io.BytesIO()
        plt.savefig(png_bytes, format='png')
        png_bytes.seek(0)
        plt.close()

        response = HttpResponse(png_bytes.getvalue(), content_type='image/png')
        response['Content-Disposition'] = 'attachment; filename=plot.png'

        return response
