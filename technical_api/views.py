from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
import yfinance as yf
import numpy as np
import pandas as pd
import requests

from datetime import datetime


class TechnicalAnalysis(APIView):
    def get(self, request, *args, **kwargs):
        # Get parameters from the URL query parameters
        tickers = request.query_params.get('tickers')
        period = request.query_params.get('period')
        interval = request.query_params.get('interval')
        customer_id = request.query_params.get('customer_id')
        customer_name = request.query_params.get('customer_name')
        source = request.query_params.get('source')
        ip = request.query_params.get('ip')

        # Check if tickers is None
        if tickers is None:
            return Response({'error': 'Tickers parameter is missing.'}, status=status.HTTP_400_BAD_REQUEST)

        ohlcv_data = {}

        # Ensure tickers is a list
        tickers = tickers.split(',')

        # looping over tickers and storing OHLCV dataframe in dictionary
        for ticker in tickers:
            temp = yf.download(ticker, period=period, interval=interval)
            temp.dropna(how="any", inplace=True)
            ohlcv_data[ticker] = temp

        def MACD(DF, a=12, b=26, c=9):
            """function to calculate MACD
            typical values a(fast moving average) = 12; 
                            b(slow moving average) =26; 
                            c(signal line ma window) =9"""
            df = DF.copy()
            df["ma_fast"] = df["Adj Close"].ewm(span=a, min_periods=a).mean()
            df["ma_slow"] = df["Adj Close"].ewm(span=b, min_periods=b).mean()
            df["macd"] = df["ma_fast"] - df["ma_slow"]
            df["signal"] = df["macd"].ewm(span=c, min_periods=c).mean()
            return df.loc[:, ["macd", "signal"]]

        for ticker in ohlcv_data:
            ohlcv_data[ticker][["MACD", "SIGNAL"]] = MACD(
                ohlcv_data[ticker], a=12, b=26, c=9)

        def ATR(DF, n=14):
            "function to calculate True Range and Average True Range"
            df = DF.copy()
            df["H-L"] = df["High"] - df["Low"]
            df["H-PC"] = abs(df["High"] - df["Adj Close"].shift(1))
            df["L-PC"] = abs(df["Low"] - df["Adj Close"].shift(1))
            df["TR"] = df[["H-L", "H-PC", "L-PC"]].max(axis=1, skipna=False)
            df["ATR"] = df["TR"].ewm(com=n, min_periods=n).mean()
            return df["ATR"]

        for ticker in ohlcv_data:
            ohlcv_data[ticker]["ATR"] = ATR(ohlcv_data[ticker])

        def Boll_Band(DF, n=14):
            "function to calculate Bollinger Band"
            df = DF.copy()
            df["MB"] = df["Adj Close"].rolling(n).mean()
            df["UB"] = df["MB"] + 2*df["Adj Close"].rolling(n).std(ddof=0)
            df["LB"] = df["MB"] - 2*df["Adj Close"].rolling(n).std(ddof=0)
            df["BB_Width"] = df["UB"] - df["LB"]
            return df[["MB", "UB", "LB", "BB_Width"]]

        for ticker in ohlcv_data:
            ohlcv_data[ticker][["MB", "UB", "LB", "BB_Width"]
                               ] = Boll_Band(ohlcv_data[ticker])

        def RSI(DF, n=14):
            "function to calculate RSI"
            df = DF.copy()
            df["change"] = df["Adj Close"] - df["Adj Close"].shift(1)
            df["gain"] = np.where(df["change"] >= 0, df["change"], 0)
            df["loss"] = np.where(df["change"] < 0, -1*df["change"], 0)
            df["avgGain"] = df["gain"].ewm(alpha=1/n, min_periods=n).mean()
            df["avgLoss"] = df["loss"].ewm(alpha=1/n, min_periods=n).mean()
            df["rs"] = df["avgGain"]/df["avgLoss"]
            df["rsi"] = 100 - (100 / (1 + df["rs"]))
            return df["rsi"]

        for ticker in ohlcv_data:
            ohlcv_data[ticker]["RSI"] = RSI(ohlcv_data[ticker])

        def ADX(DF, n=20):
            "function to calculate ADX"
            df = DF.copy()
            df["ATR"] = ATR(DF, n)
            df["upmove"] = df["High"] - df["High"].shift(1)
            df["downmove"] = df["Low"].shift(1) - df["Low"]
            df["+dm"] = np.where((df["upmove"] > df["downmove"])
                                 & (df["upmove"] > 0), df["upmove"], 0)
            df["-dm"] = np.where((df["downmove"] > df["upmove"])
                                 & (df["downmove"] > 0), df["downmove"], 0)
            df["+di"] = 100 * (df["+dm"]/df["ATR"]
                               ).ewm(alpha=1/n, min_periods=n).mean()
            df["-di"] = 100 * (df["-dm"]/df["ATR"]
                               ).ewm(alpha=1/n, min_periods=n).mean()
            df["ADX"] = 100 * abs((df["+di"] - df["-di"])/(df["+di"] +
                                  df["-di"])).ewm(alpha=1/n, min_periods=n).mean()
            return df["ADX"]

        for ticker in ohlcv_data:
            ohlcv_data[ticker]["ADX"] = ADX(ohlcv_data[ticker], 20)

        # Replace NaN values with 0 in each DataFrame
        for ticker, data in ohlcv_data.items():
            ohlcv_data[ticker].fillna(0, inplace=True)

        excel_file_path = 'ohlcv_data_analysis.xlsx'
        with pd.ExcelWriter(excel_file_path, engine='xlsxwriter') as writer:
            for ticker, data in ohlcv_data.items():
                # Add a new column for datetime
                data['Datetime'] = data.index

                # Reorder columns with datetime as the first column
                data = data[['Datetime'] +
                            [col for col in data.columns if col != 'Datetime']]

                data.to_excel(writer, sheet_name=ticker, index=False)

                # Get the xlsxwriter workbook and worksheet objects
                workbook = writer.book
                worksheet = writer.sheets[ticker]

                # Add a format for borders around all cells
                border_format = workbook.add_format({'border': 1})

                # Apply the border format to all cells in the worksheet
                worksheet.conditional_format(
                    0, 0, len(data), len(data.columns) - 1,
                    {'type': 'no_errors',
                     'format': border_format})

                # Get the max value in the ADX column for conditional formatting
                max_adx = data['ADX'].max()

                # Add a format for white, light green, and dark green based on ADX ranges
                white_format = workbook.add_format(
                    {'bg_color': 'white', 'border': 1})
                light_green_format = workbook.add_format(
                    {'bg_color': '#c6efce', 'border': 1})
                dark_green_format = workbook.add_format(
                    {'bg_color': '#6aa84f', 'border': 1})

                # Apply conditional formatting to the ADX column
                worksheet.conditional_format(
                    1, data.columns.get_loc('ADX'), len(
                        data) + 1, data.columns.get_loc('ADX'),
                    {'type': 'cell',
                     'criteria': 'between',
                     'minimum': 0,
                     'maximum': 25,
                     'format': white_format})

                worksheet.conditional_format(
                    1, data.columns.get_loc('ADX'), len(
                        data) + 1, data.columns.get_loc('ADX'),
                    {'type': 'cell',
                     'criteria': 'between',
                     'minimum': 25,
                     'maximum': 50,
                     'format': light_green_format})

                worksheet.conditional_format(
                    1, data.columns.get_loc('ADX'), len(
                        data) + 1, data.columns.get_loc('ADX'),
                    {'type': 'cell',
                     'criteria': 'between',
                     'minimum': 50,
                     'maximum': max_adx,
                     'format': dark_green_format})

                # Add a format for light red and light green based on RSI ranges
                light_red_format = workbook.add_format(
                    {'bg_color': '#f4cccc', 'border': 1})
                light_green_format_rsi = workbook.add_format(
                    {'bg_color': '#c6efce', 'border': 1})

                # Apply conditional formatting to the RSI column
                worksheet.conditional_format(
                    1, data.columns.get_loc('RSI'), len(
                        data) + 1, data.columns.get_loc('RSI'),
                    {'type': 'cell',
                     'criteria': '>',
                     'value': 70,
                     'format': light_red_format})

                worksheet.conditional_format(
                    1, data.columns.get_loc('RSI'), len(
                        data) + 1, data.columns.get_loc('RSI'),
                    {'type': 'cell',
                     'criteria': '<',
                     'value': 30,
                     'format': light_green_format_rsi})

                # Add a format for white based on RSI being equal to zero
                white_format_rsi = workbook.add_format(
                    {'bg_color': 'white', 'border': 1})

                # Apply conditional formatting to the RSI column for values equal to zero
                worksheet.conditional_format(
                    1, data.columns.get_loc('RSI'), len(
                        data) + 1, data.columns.get_loc('RSI'),
                    {'type': 'cell',
                     'criteria': '=',
                     'value': 0,
                     'format': white_format_rsi})
        # Open the file in binary mode and create a FileResponse
        with open(excel_file_path, 'rb') as excel_file:
            response = HttpResponse(excel_file.read(
            ), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=ohlcv_data_analysis.xlsx'

        print(f'OHLCV data and analysis saved to: {excel_file_path}')

        # Make an additional API request
        api_url = 'https://9rhjqf5ix7.execute-api.ap-south-1.amazonaws.com/dev/apicount?operation=add'
        current_datetime = datetime.now().isoformat()
        payload = {
            "datetime": current_datetime,
            "api_name": "technical_api",
            "customer_id": customer_id,
            "customer_name": customer_name,
            "source": source,
            "ip": ip
        }

        try:
            api_response = requests.post(api_url, json=payload)
            api_response.raise_for_status()
            print(
                f'Additional API request successful. Response: {api_response.text}')
        except requests.exceptions.RequestException as e:
            print(f'Error making additional API request: {e}')

        return response
