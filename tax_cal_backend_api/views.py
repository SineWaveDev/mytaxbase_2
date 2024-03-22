# tax_api/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests

@api_view(['POST'])
def calculate_tax(request):
    # Receive JSON payload from the request
    request_data = request.data

    # Extract first_payload from the request data
    first_payload = request_data.get('first_payload', {})

    # Call the first API
    first_api_url = "http://mosversion2.sinewave.co.in/api/calculate/"
    first_response = requests.post(first_api_url, json=first_payload)
    first_data = first_response.json()

    # Initialize second_payload with data from the request_data
    second_payload = request_data.get('second_payload', {})

    # Merge the data obtained from the first response into second_payload
    second_payload.update({
        "BusinessProfession": first_data.get('BusinessProfession', {}),
        "DedutionUSCHVIA": first_data.get('DeductionVI_and_AeighthC_Total', {}),
        "HouseProperty": first_data.get('HouseProperty', {}),
        "Salary": first_data.get('Salary', {}),
        "OtherSources": first_data.get('OtherSources', {})
    })
    # print("second_payload", second_payload)

    # Call the second API with the updated second_payload
    second_api_url = "https://taxapi.sinewave.co.in/API/TaxCalculator/CalculateTax"
    second_response = requests.post(second_api_url, json=second_payload)
    second_data = second_response.json()

    # Combine responses
    combined_response = {
        "first_api_response": first_data,
        "second_api_response": second_data
    }

    return Response(combined_response)
