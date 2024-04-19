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

class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        serializer = ExcelFileSerializer(data=request.data)

        if serializer.is_valid():
            file = serializer.validated_data['file']
            
            # Save the uploaded file
            file_path = f'media/{file.name}'
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            # Process the uploaded file
            data = pd.read_excel(file_path)
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

            close_prices_with_qty['Portfolio_Value'] = close_prices_with_qty.filter(like='_Value').sum(axis=1)
            close_prices_with_qty['Portfolio_Return'] = close_prices_with_qty['Portfolio_Value'].pct_change()

            first_purchase_date_processed = False

            for index, row in data.iterrows():
                purchase_date = row['Purchase Date']
                purchase_price = row['Rate']
                purchase_QTY = row['QTY']

                if purchase_date in data['Purchase Date'].values:
                    row_index = close_prices_with_qty[close_prices_with_qty['Date'] == purchase_date].index[0]
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

            sell_transactions_grouped = data[data['Sale / Valuation Date'] >= '02/02/2024'].groupby('Sale / Valuation Date')

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

            output_file = f'media/close_prices_with_qty.csv'
            close_prices_with_qty.to_csv(output_file)

            # Generate plots
            fig, ax1 = plt.subplots(figsize=(10, 6))
            sns.lineplot(data=close_prices_with_qty, x='Date', y='Portfolio_Return', color='blue', ax=ax1, label='Return')
            ax2 = ax1.twinx()
            sns.lineplot(data=close_prices_with_qty, x='Date', y='Portfolio_std_dev', color='red', ax=ax2, label='Standard Deviation')
            ax1.set_xlabel('Date')
            ax1.set_ylabel('Return', color='blue')
            ax2.set_ylabel('Standard Deviation', color='red')
            plt.title('Portfolio Return and Standard Deviation per Day')
            plt.xticks(rotation=45)
            fig.legend(loc='upper left')
            plt.tight_layout()
            plt.savefig('media/daily_portfolio_return.png')
            plt.close()

            plt.figure(figsize=(10, 6))
            sns.lineplot(data=close_prices_with_qty, x='Date', y='Cumulative_Return', color='green', label='Cumulative Return')
            sns.lineplot(data=close_prices_with_qty, x='Date', y='Portfolio_std_dev', color='orange', label='Portfolio Std Dev')
            sns.lineplot(data=close_prices_with_qty, x='Date', y='Sharpe_Ratio', color='red', label='Sharpe Ratio')
            plt.xlabel('Date')
            plt.ylabel('Value')
            plt.title('Cumulative Portfolio Return vs Portfolio Std Dev vs Sharpe Ratio')
            plt.xticks(rotation=45)
            plt.legend()
            plt.savefig('media/cumulative_return_vs_std_dev_vs_sharpe_ratio.png')
            plt.close()

            return Response({'message': 'File uploaded successfully', 'output_file': output_file}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
