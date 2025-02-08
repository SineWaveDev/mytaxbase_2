import yfinance as yf
import numpy as np
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class StockDataAPIView(APIView):
    def post(self, request):
        tickers = request.data.get("tickers", [])

        if not isinstance(tickers, list) or not tickers:
            return Response({"error": "Invalid input. Provide a list of tickers."}, status=status.HTTP_400_BAD_REQUEST)

        # Fetch all tickers' historical data at once (5 years)
        try:
            hist_data = yf.download(tickers, period="5y", progress=False, group_by='ticker')
        except Exception as e:
            return Response({"error": "Failed to fetch stock data", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        script_details = []
        invalid_tickers = []

        def process_ticker(ticker):
            try:
                hist = hist_data[ticker] if len(tickers) > 1 else hist_data
                if hist.empty or 'Close' not in hist:
                    invalid_tickers.append(ticker)
                    return

                hist['returns'] = hist['Close'].pct_change()
                daily_returns = hist['returns'].dropna()

                # Financial calculations
                ann_mean = daily_returns.mean() * 252
                ann_std = daily_returns.std() * np.sqrt(252)
                sharpe_ratio = ann_mean / ann_std if ann_std != 0 else 0
                
                downside_returns = daily_returns[daily_returns < 0]
                sortino_ratio = ann_mean / (downside_returns.std() * np.sqrt(252)) if downside_returns.std() != 0 else 0
                
                rolling_max = hist['Close'].cummax()
                drawdown = (hist['Close'] - rolling_max) / rolling_max
                max_drawdown = drawdown.min()

                calmar_ratio = ann_mean / abs(max_drawdown) if max_drawdown != 0 else 0
                max_dd_duration = (drawdown < 0).astype(int).groupby(drawdown.ge(0).astype(int).cumsum()).sum().max()
                kelly_criterion = (ann_mean / ann_std ** 2) if ann_std != 0 else 0

                # Append formatted data to list
                script_details.append({
                    "Company_Name": ticker,
                    "ann_mean": round(np.nan_to_num(ann_mean, nan=0.0), 10),
                    "ann_std": round(np.nan_to_num(ann_std, nan=0.0), 10),
                    "sharpe": round(np.nan_to_num(sharpe_ratio, nan=0.0), 10),
                    "sortino": round(np.nan_to_num(sortino_ratio, nan=0.0), 10),
                    "max_drawdown": round(abs(np.nan_to_num(max_drawdown, nan=0.0)), 10),
                    "calmar": round(np.nan_to_num(calmar_ratio, nan=0.0), 10),
                    "max_dd_duration": int(np.nan_to_num(max_dd_duration, nan=0.0)),
                    "kelly": round(np.nan_to_num(kelly_criterion, nan=0.0), 10)
                })
            except Exception:
                invalid_tickers.append(ticker)

        # Process tickers in parallel using ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(process_ticker, tickers)

        if invalid_tickers:
            return Response({
                "error": "Invalid tickers found",
                "invalid_tickers": invalid_tickers
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({"Script_Details": script_details}, status=status.HTTP_200_OK)
