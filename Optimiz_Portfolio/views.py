# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from datetime import datetime, timedelta
# import pandas as pd
# import yfinance as yf
# from pypfopt import EfficientFrontier, expected_returns, risk_models
# print("start.......")
# class PortfolioPerformance(APIView):
#     def post(self, request):
#         try:
#             tickers = request.data.get('tickers')
#             print("tickers:", tickers)
            
#             # Retrieve 'period' from query parameters
#             period = int(request.query_params.get('period', 0))
#             print("period:", period)
            
#             start_date = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')
#             end_date = datetime.today().strftime('%Y-%m-%d')
#             # Download data
#             data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']

#             # Calculate expected returns and covariance matrix
#             mu = expected_returns.mean_historical_return(data)
#             Sigma = risk_models.sample_cov(data)

#             # Risk-free rate
#             risk_free_rate = 0.07

#             # Create an instance of EfficientFrontier
#             ef = EfficientFrontier(mu, Sigma)

#             # Add constraints
#             ef.add_constraint(lambda w: w >= 0)

#             # Optimize for maximum Sharpe ratio
#             ef.efficient_return(target_return=0.8)

#             # Get cleaned weights
#             cleaned_weights = ef.clean_weights()

#             # Get portfolio performance
#             expected_return, volatility, sharpe_ratio = ef.portfolio_performance(risk_free_rate=risk_free_rate)

#             portfolio_data = pd.DataFrame(columns=["Ticker", "Weight", "Expected Return", "Volatility", "Sharpe Ratio", "Risk Free Rate"])

#             for ticker, weight in cleaned_weights.items():
#                 portfolio_data = portfolio_data.append({"Ticker": ticker, "Weight": weight}, ignore_index=True)

#             portfolio_data.loc[0, "Expected Return"] = expected_return
#             portfolio_data.loc[0, "Volatility"] = volatility
#             portfolio_data.loc[0, "Sharpe Ratio"] = sharpe_ratio
#             portfolio_data.loc[0, "Risk Free Rate"] = risk_free_rate

#             excel_filename = "portfolio_performance.xlsx"
#             portfolio_data.to_excel(excel_filename, index=False)

#             return Response({"message": "Portfolio performance data saved to portfolio_performance.xlsx"}, status=status.HTTP_201_CREATED)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
