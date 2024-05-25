# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from pypfopt import EfficientFrontier, expected_returns, risk_models
from django.http import HttpResponse
from io import BytesIO

@api_view(['POST'])
def calculate_portfolio_performance(request):
    tickers = request.data.get('tickers', [])  # Assuming tickers are sent as a list in the request data
    risk_free_rate = float(request.data.get('risk_free_rate'))
    target_return = float(request.data.get('target_return'))
    
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')
    data = yf.download(tickers, start=start_date, end=end_date)['Adj Close']
    mu = expected_returns.mean_historical_return(data)
    Sigma = risk_models.sample_cov(data)
    
    ef = EfficientFrontier(mu, Sigma)
    ef.add_constraint(lambda w: w >= 0)
    ef.efficient_return(target_return=target_return)
    cleaned_weights = ef.clean_weights()
    expected_return, volatility, sharpe_ratio = ef.portfolio_performance(risk_free_rate=risk_free_rate)
    
    # Create DataFrame for portfolio performance data
    portfolio_data = pd.DataFrame(columns=["Ticker", "Weight", "Expected Return", "Volatility", "Sharpe Ratio", "Risk Free Rate"])
    for ticker, weight in cleaned_weights.items():
        portfolio_data = portfolio_data._append({"Ticker": ticker, "Weight": weight}, ignore_index=True)
    
    portfolio_data.loc[0, "Expected Return"] = expected_return
    portfolio_data.loc[0, "Volatility"] = volatility
    portfolio_data.loc[0, "Sharpe Ratio"] = sharpe_ratio
    portfolio_data.loc[0, "Risk Free Rate"] = risk_free_rate

    # Create Excel file
    excel_buffer = BytesIO()
    excel_writer = pd.ExcelWriter(excel_buffer, engine='xlsxwriter')
    portfolio_data.to_excel(excel_writer, index=False, sheet_name='Portfolio Performance')
    excel_writer.close()  # Close the Excel writer
    excel_buffer.seek(0)

    # Return Excel file as response
    response = HttpResponse(excel_buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=portfolio_performance.xlsx'
    
    return response