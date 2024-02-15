import os
from dateutil.relativedelta import relativedelta
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
import yfinance as yf
import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import calendar

class PortfolioChart(APIView):
    def post(self, request, *args, **kwargs):
        tickers = request.query_params.get('tickers', '').split(',')
        interval = request.query_params.get('interval')
        period = int(request.query_params.get('period'))
        file = request.query_params.get('file')
        print("tickers:", tickers)
        print("interval:", interval)
        print("period:", period)
        print("file:", file)
        
        def CAGR(DF):
            df = DF.copy()
            df["cum_return"] = (1 + df["mon_ret"]).cumprod()
            n = len(df)/12
            CAGR = (df["cum_return"].tolist()[-1])**(1/n) - 1
            return CAGR

        def volatility(DF):
            df = DF.copy()
            vol = df["mon_ret"].std() * np.sqrt(12)
            return vol

        def sharpe(DF, rf):
            df = DF.copy()
            sr = (CAGR(df) - rf)/volatility(df)
            return sr

        def max_dd(DF):
            df = DF.copy()
            df["cum_return"] = (1 + df["mon_ret"]).cumprod()
            df["cum_roll_max"] = df["cum_return"].cummax()
            df["drawdown"] = df["cum_roll_max"] - df["cum_return"]
            df["drawdown_pct"] = df["drawdown"]/df["cum_roll_max"]
            max_dd = df["drawdown_pct"].max()
            return max_dd
        
        # Adjust start date to be 12 months or 6 months before today's date
        months_ago = dt.datetime.today() - relativedelta(months=period)

        # Adjust the start date based on your requirement
        start = months_ago  # or start_6_months_ago

        ohlc_mon = {}
        end = dt.datetime.today()

        for ticker in tickers:
            ohlc_mon[ticker] = yf.download(ticker, start, end, interval=interval)
            ohlc_mon[ticker].dropna(inplace=True, how="all")
            print(f"Ticker: {ticker}, Keys: {ohlc_mon[ticker].keys()}")

        tickers = list(ohlc_mon.keys())

        return_df = pd.DataFrame()
        for ticker in tickers:
            ohlc_mon[ticker]["mon_ret"] = ohlc_mon[ticker]["Adj Close"].pct_change().fillna(0)
            return_df[ticker] = ohlc_mon[ticker]["mon_ret"]
        return_df.dropna(inplace=True)

        def pflio(DF, m, x, save_file=None):
            df = DF.copy()
            portfolio = []
            monthly_ret = [0]
            portfolio_history = []  

            monthly_stock_returns = {ticker: [] for ticker in df.columns}

            for i in range(len(df)):
                if len(portfolio) > 0:
                    monthly_ret.append(df[portfolio].iloc[i, :].mean())
                    bad_stocks = df[portfolio].iloc[i, :].sort_values(ascending=True)[:x].index.values.tolist()
                    portfolio = [t for t in portfolio if t not in bad_stocks]
                fill = m - len(portfolio)
                new_picks = df.iloc[i, :].sort_values(ascending=False)[:fill].index.values.tolist()
                portfolio = portfolio + new_picks
                portfolio_history.append(portfolio)  

                for ticker in df.columns:
                    monthly_stock_returns[ticker].append(df[ticker].iloc[i])

            monthly_ret_df = pd.DataFrame(np.array(monthly_ret), columns=["mon_ret"])

            if save_file:
                portfolio_with_returns = []
                header_row = ["Month", "Stock1", "Return1", "Stock2", "Return2", "Stock3", "Return3", "Stock4", "Return4",
                            "Stock5", "Return5", "Stock6", "Return6"]
                portfolio_with_returns.append(header_row)

                for i, portfolio_selection in enumerate(portfolio_history):
                    month_index = (i + 3) % 12
                    year = 19 + (i + 3) // 12
                    if month_index == 0:
                        year -= 1  
                    month_abbr = calendar.month_abbr[month_index]

                    portfolio_row = [f"{month_abbr}-{str(year)}"]
                    for j, stock in enumerate(portfolio_selection):
                        portfolio_row.append(stock)
                        portfolio_row.append(monthly_stock_returns[stock][i])
                    portfolio_with_returns.append(portfolio_row)

                with open(save_file, 'w') as f:
                    for portfolio_row in portfolio_with_returns:
                        f.write(','.join(map(str, portfolio_row)) + '\n')

            return monthly_ret_df

        strategy_return = pflio(return_df, 6, 3, save_file='portfolio_history.csv')
        strategy_cagr = CAGR(strategy_return)
        strategy_sharpe = sharpe(strategy_return, 0.025)
        strategy_max_dd = max_dd(strategy_return)

        stock_cagrs = {}
        stock_sharpes = {}
        stock_max_dds = {}

        for ticker in tickers:
            stock_data = yf.download(ticker, start, end, interval=interval)
            stock_data["mon_ret"] = stock_data["Adj Close"].pct_change().fillna(0)
            
            if ticker in stock_data.columns:
                stock_cagrs[ticker] = CAGR(stock_data)
                stock_sharpes[ticker] = sharpe(stock_data, 0.025)
                stock_max_dds[ticker] = max_dd(stock_data)

        return_df.to_csv('portfolio_data.csv')

        fig, ax = plt.subplots()
        plt.plot((1+strategy_return).cumprod())
        plt.plot((1+stock_data["mon_ret"].reset_index(drop=True)).cumprod())
        plt.title("Index Return vs Strategy Return")
        plt.ylabel("Cumulative Return")
        plt.xlabel("Months")
        ax.legend(["Strategy Return","Index Return"])
        plt.savefig('portfolio_comparison.png')
        plt.close()  

        if file == 'csv':
            file_path = 'portfolio_history.csv'
            content_type = 'text/csv'
            filename = 'portfolio_history.csv'
        elif file == 'chart':
            file_path = 'portfolio_comparison.png'
            content_type = 'image/png'
            filename = 'portfolio_comparison.png'
        else:
            return Response({'error': 'Invalid file type specified'})

        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type=content_type)
            response['Content-Disposition'] = f'attachment; filename="{filename}"'

        return response
