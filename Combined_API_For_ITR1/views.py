# tax_api/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests

@api_view(['POST'])
def calculate_tax(request):
    # Receive JSON payload from the request
    request_data = request.data

    # Extract json_creation_payload from the request data
    json_creation_payload = request_data.get('json_creation_payload', {})

    # Call the JSON creation API
    json_creation_api_url = "http://mosversion2.sinewave.co.in/api/Json/"
    json_creation_response = requests.post(json_creation_api_url, json=json_creation_payload)
    json_creation_data = json_creation_response.json()
    print("json_creation_data:", json_creation_data)

    # Call the Digest Code API with the JSON creation API response
    digest_code_api_url = "http://mosversion2.sinewave.co.in/api/digest/"
    digest_code_response = requests.post(digest_code_api_url, json=json_creation_data)
    digest_code_data = digest_code_response.json()
    print("digest_code_data:", digest_code_data)

    # Update the Digest field in the json_creation_data with the digest code
    json_creation_data['Digest'] = digest_code_data.get('Digest', '-')
    print("updated_json_creation_data:", json_creation_data)

    # Call the JSON Compare API with the updated json_creation_data
    json_compare_api_url = "http://mosversion2.sinewave.co.in/api/validate-json/"
    json_compare_response = requests.post(json_compare_api_url, json=json_creation_data)
    json_compare_data = json_compare_response.json()
    print("json_compare_data:", json_compare_data)

    # Combine responses
    combined_response = {
        "json_creation_response": json_creation_data,
        "digest_code_response": digest_code_data,
        "json_compare_response": json_compare_data
    }

    return Response(combined_response)
