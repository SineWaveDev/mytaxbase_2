import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import re

class CallStatusAPIsView(APIView):
    def post(self, request):
        # Step 1: Call API-1 to get the access token
        api1_url = "https://login.microsoftonline.com/f63f8f14-9b26-4bd7-8ccb-4dfd683a99bf/oauth2/v2.0/token"
        api1_payload = {
            "grant_type": "client_credentials",
            "client_id": "363bfc81-18f6-4356-a60d-38f32c1db037",
            "client_secret": "aGQ8Q~9Hwopkz45c_juetCOVS1XlHRVr7f3Z3bSX",
            "scope": "https://graph.microsoft.com/.default",
        }

        try:
            api1_response = requests.post(api1_url, data=api1_payload)
            api1_response.raise_for_status()
            access_token = api1_response.json().get("access_token")
        except requests.exceptions.RequestException as e:
            return Response({"error": "Failed to get access token", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Step 2: Call API-2 with the access token and user-defined email
        user_email = request.query_params.get("email")  # Get email from query params
        if not user_email:
            return Response({"error": "Missing 'email' parameter in request"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", user_email):
            return Response({"error": "Invalid email format"}, status=status.HTTP_400_BAD_REQUEST)

        api2_url = f"https://graph.microsoft.com/v1.0/users/{user_email}"
        api2_headers = {
            "Authorization": f"Bearer {access_token}"
        }

        try:
            api2_response = requests.get(api2_url, headers=api2_headers)
            api2_response.raise_for_status()
            api2_data = api2_response.json()

            # Debug: Log full response
            print("API-2 Response:", api2_data)

            # Retrieve user ID
            user_id = api2_data.get("id")

            if not user_id:
                return Response({"error": "User ID not found in API-2 response", "api2_response": api2_data}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except requests.exceptions.RequestException as e:
            return Response({"error": "Failed to call API-2", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Step 3: Call API-3 with user ID and access token
        api3_url = f"https://graph.microsoft.com/v1.0/users/{user_id}/presence"
        api3_headers = {
            "Authorization": f"Bearer {access_token}"
        }

        try:
            api3_response = requests.get(api3_url, headers=api3_headers)
            api3_response.raise_for_status()
            api3_data = api3_response.json()
        except requests.exceptions.RequestException as e:
            return Response({"error": "Failed to call API-3", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Return final response including input email and API-3 response
        return Response({
            "email": user_email,
            "user_id": user_id,
            "api3_response": api3_data
        }, status=status.HTTP_200_OK)
