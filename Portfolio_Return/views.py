from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from .serializers import ExcelFileSerializer
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import base64
import io


class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = ExcelFileSerializer(data=request.data)

        if serializer.is_valid():
            file = serializer.validated_data['file']
            
  
            # file_path = f'media/{file.name}'
            # file_name = 'Portfolio Returns 2023-2024.xlsx'
            file_name = 'Book3.xlsx'
            with open(file_name, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            # Process the uploaded file
            data = pd.read_excel(file_name)
            # Sort the DataFrame by 'Purchase Date'
            data.sort_values(by='Purchase Date', inplace=True)
            data['Purchase Date'] = pd.to_datetime(data['Purchase Date'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')
            data['Sale / Valuation Date'] = pd.to_datetime(data['Sale / Valuation Date'], format='%d/%m/%Y').dt.strftime('%Y-%m-%d')

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

                if purchase_date in data['Purchase Date'].values:
                   # row_index = close_prices_with_qty[close_prices_with_qty['Date'] == purchase_date].index[0]
                    #onvert purchase_date to a datetime object
                    purchase_date = pd.to_datetime(purchase_date)

                    # Add one day to purchase_date and find the corresponding row index
                    row_index = close_prices_with_qty[close_prices_with_qty['Date'] == purchase_date + pd.Timedelta(days=1)].index[
                        0]
                    portfolio_value = close_prices_with_qty.loc[row_index, 'Portfolio_Value']
                    net_purchase_value = purchase_price * purchase_QTY

                    try:
                        previous_day_portfolio_value = close_prices_with_qty.iloc[row_index - 1]['Portfolio_Value']
                    except KeyError:
                        previous_day_portfolio_value = 0

                    denominator = net_purchase_value + previous_day_portfolio_value
                    result = portfolio_value / denominator / 100

                    close_prices_with_qty.at[row_index, 'Portfolio_Return'] = result

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

            rolling_sharpe_ratio = close_prices_with_qty['Portfolio_Return'].rolling(window=30).mean() / close_prices_with_qty['Portfolio_Return'].rolling(window=30).std()
            close_prices_with_qty['Sharpe_Ratio'] = rolling_sharpe_ratio

            rolling_max = close_prices_with_qty['Portfolio_Value'].cummax()
            daily_drawdown = close_prices_with_qty['Portfolio_Value'] / rolling_max - 1
            max_daily_drawdown = daily_drawdown.expanding(min_periods=1).min()
            close_prices_with_qty['Max_Drawdown'] = max_daily_drawdown

            close_prices_with_qty.fillna(0, inplace=True)

            close_prices_with_qty.reset_index(inplace=True)

            # Saving close_prices_with_qty to a CSV file
            output_file_csv = io.BytesIO()
            close_prices_with_qty.to_csv(output_file_csv, index=False)
            output_file_csv.seek(0)

            filtered_df = merged_df[(merged_df['Date'] >= '2023-04-01') & (merged_df['Date'] <= '2024-03-31')]

            filtered_df['Date'] = pd.to_datetime(filtered_df['Date'])

            filtered_df['Cumulative_Return'] = (1 + filtered_df['Portfolio_Return']).cumprod() - 1

            amplification_factor = 50  # Adjust as needed
            filtered_df['Amplified_Std_Dev'] = filtered_df['Portfolio_std_dev'] * amplification_factor

            sns.set_style("whitegrid")  # Set style
            fig, ax1 = plt.subplots(figsize=(19, 10))  # Set figure size

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
            # plt.savefig('C:\\Users\\Sinewave#2022\\Downloads\\cumulative_return_vs_std_dev_vs_sharpe_ratio.png')
            plt.close()
            # Saving close_prices_with_qty to a CSV file
            output_file_csv = io.BytesIO()
            close_prices_with_qty.to_csv(output_file_csv, index=False)
            output_file_csv.seek(0)
            
            # Saving the plot to a PNG file
            output_file_png = io.BytesIO()
            plt.savefig(output_file_png)
            output_file_png.seek(0)
            
            # Encode files as base64 strings
            csv_base64 = base64.b64encode(output_file_csv.read()).decode()
            png_base64 = base64.b64encode(output_file_png.read()).decode()
            
            return Response({
                'message': 'File uploaded successfully',
                'close_prices_with_qty_csv': csv_base64,
                'cumulative_return_vs_std_dev_vs_sharpe_ratio_png': png_base64
            }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
