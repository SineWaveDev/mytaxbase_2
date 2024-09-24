import requests
from rest_framework.response import Response
from rest_framework.decorators import api_view
from requests.exceptions import RequestException

@api_view(['POST'])
def check_pan_details(request):
    # Get userId from the request body
    user_id = request.data.get('userId')

    # The URL of the external API
    url = "https://eportal.incometax.gov.in/iec/registrationapi/saveEntity"

    # The payload to be sent to the external API
    payload = {
        "serviceName": "checkPanDetailsService",
        "userId": user_id
    }

    # Define your proxy settings
    proxies = {
        "http": "http://45.114.142.178:80",
        "https": "http://45.114.142.178:80",  # Use the same proxy for HTTPS
    }

    # Make the POST request to the external API
    try:
        api_response = requests.post(url, json=payload, proxies=proxies)
        api_response.raise_for_status()  # Check if the request was successful (status code 2xx)

        # Return the external API's response as it is
        return Response(api_response.json(), status=api_response.status_code)

    except RequestException as e:
        # Handle errors (e.g., API is unreachable, timeout, etc.)
        return Response({"error": str(e)}, status=500)
