from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework import serializers
import yfinance as yf
from datetime import datetime
import pytz
import pandas as pd

# Define the serializer directly in views.py
class SymbolSerializer(serializers.Serializer):
    symbols = serializers.ListField(child=serializers.CharField(), required=True)
    financial_year = serializers.CharField(required=True)  # New field for financial year

class StockDataView(APIView):
    parser_classes = [JSONParser]
    renderer_classes = [JSONRenderer]

    def post(self, request):
        serializer = SymbolSerializer(data=request.data)
        if serializer.is_valid():
            symbols = serializer.validated_data['symbols']
            financial_year = serializer.validated_data['financial_year']

            # Parse the financial year
            try:
                start_year, end_year = map(int, financial_year.split('-'))
                financial_year_start = datetime(start_year, 4, 1)
                financial_year_end = datetime(end_year, 3, 31)
            except ValueError:
                return Response({"error": "Invalid financial year format. Use 'YYYY-YYYY'."}, status=status.HTTP_400_BAD_REQUEST)

            # Localize start and end dates to Asia/Kolkata timezone
            start_date = pytz.timezone('Asia/Kolkata').localize(financial_year_start)
            end_date = pytz.timezone('Asia/Kolkata').localize(financial_year_end)

            all_dividends = []
            all_splits = []

            for symbol in symbols:
                stock = yf.Ticker(symbol)

                # Fetch and filter dividends for the financial year
                dividends = stock.dividends.reset_index()
                dividends = dividends[(dividends['Date'] >= start_date) & (dividends['Date'] <= end_date)]
                dividends['Stock'] = symbol
                all_dividends.append(dividends)

                # Fetch and filter splits for the financial year
                splits = stock.splits.reset_index()
                splits = splits[(splits['Date'] >= start_date) & (splits['Date'] <= end_date)]
                splits['Stock'] = symbol
                all_splits.append(splits)

            # Combine all dividends and splits data into single DataFrames
            if all_dividends:
                dividends_data = pd.concat(all_dividends, axis=0)
                dividends_data = dividends_data[['Stock', 'Dividends', 'Date']]
            else:
                dividends_data = pd.DataFrame(columns=['Stock', 'Dividends', 'Date'])

            if all_splits:
                splits_data = pd.concat(all_splits, axis=0)
                splits_data = splits_data[['Stock', 'Stock Splits', 'Date']]
            else:
                splits_data = pd.DataFrame(columns=['Stock', 'Stock Splits', 'Date'])

            # Ensure the datetime columns are timezone unaware
            dividends_data['Date'] = pd.to_datetime(dividends_data['Date']).dt.tz_localize(None)
            splits_data['Date'] = pd.to_datetime(splits_data['Date']).dt.tz_localize(None)

            # Convert DataFrames to JSON serializable format
            response_data = {
                'dividends': dividends_data.to_dict(orient='records'),
                'splits': splits_data.to_dict(orient='records')
            }

            return Response(response_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
