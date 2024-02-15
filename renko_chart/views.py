from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import yfinance as yf
from stocktrends import Renko
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.io as pio
import io
import base64
from django.http import HttpResponse


class Renko_Chart(APIView):
    def post(self, request, *args, **kwargs):
        # Get parameters from the URL query parameters
        tickers = request.query_params.getlist('tickers')
        period = request.query_params.get('period')
        interval = request.query_params.get('interval')
        brick_size = float(request.query_params.get(
            'brick_size', 3))  # Default to 3 if not provided

        ohlcv_data = {}
        hour_data = {}
        renko_data = {}

        # Looping over tickers and storing OHLCV dataframe in dictionary
        for ticker in tickers:
            temp = yf.download(ticker, period=period, interval=interval)
            temp.dropna(how="any", inplace=True)
            ohlcv_data[ticker] = temp

            temp = yf.download(ticker, period='1y', interval='1h')
            temp.dropna(how="any", inplace=True)
            hour_data[ticker] = temp

        def ATR(DF, n=14):
            "Function to calculate True Range and Average True Range"
            df = DF.copy()
            df["H-L"] = df["High"] - df["Low"]
            df["H-PC"] = abs(df["High"] - df["Adj Close"].shift(1))
            df["L-PC"] = abs(df["Low"] - df["Adj Close"].shift(1))
            df["TR"] = df[["H-L", "H-PC", "L-PC"]].max(axis=1, skipna=False)
            df["ATR"] = df["TR"].ewm(com=n, min_periods=n).mean()
            return df["ATR"]

        def renko_DF(DF, hourly_df, brick_size):
            "Function to convert OHLC data into Renko bricks"
            df = DF.copy()
            df.reset_index(inplace=True)
            df.drop("Close", axis=1, inplace=True)
            df.columns = ["date", "open", "high", "low", "close", "volume"]
            df2 = Renko(df)
            df2.brick_size = brick_size
            renko_df = df2.get_ohlc_data()
            return renko_df

        for ticker in ohlcv_data:
            renko_data[ticker] = renko_DF(
                ohlcv_data[ticker], hour_data[ticker], brick_size)

        # Function to create and plot Renko chart
        def plot_renko(renko_df, ticker):
            fig = make_subplots(rows=1, cols=1)

            fig.add_trace(go.Candlestick(x=renko_df['date'],
                                         open=renko_df['open'],
                                         high=renko_df['high'],
                                         low=renko_df['low'],
                                         close=renko_df['close'],
                                         increasing_line_color='green',
                                         decreasing_line_color='red'))

            # Use categorical x-axis to avoid gaps in Renko chart
            fig.update_xaxes(type='category')
            fig.update_layout(
                title=f'Renko Chart - {ticker}', xaxis_title='Date', yaxis_title='Price')

            # Save the plot as an image
            img_data = pio.to_image(fig, format='png', width=800, height=600)

            # Encode image data to base64
            img_base64 = base64.b64encode(img_data).decode('utf-8')

            return img_base64

        renko_charts = {}

        # Loop through each ticker and generate the Renko chart
        for ticker in renko_data:
            renko_charts[ticker] = plot_renko(renko_data[ticker], ticker)

        # Prepare and send the response with image download
        for ticker, img_base64 in renko_charts.items():
            response = HttpResponse(base64.b64decode(
                img_base64), content_type='image/png')
            response['Content-Disposition'] = f'attachment; filename="{ticker}_renko_chart.png"'
            return response

        return Response(status=status.HTTP_200_OK)
