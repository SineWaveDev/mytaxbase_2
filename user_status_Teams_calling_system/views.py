import pymssql
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import re

# Database connection credentials
SERVER = '3.108.198.195'
DATABASE = 'indiataxes_com_indiataxes'
USERNAME = 'indiataxes_com_indiataxes'
PASSWORD = 'SW_02ITNETCOM'


class CallStatusAPIsView(APIView):
    def post(self, request):
        # Step 1: Fetch all email IDs from the database
        try:
            conn = pymssql.connect(SERVER, USERNAME, PASSWORD, DATABASE)
            cursor = conn.cursor()
            query = """
                SELECT EMAIL
                FROM CS_EMPLOYEE
                WHERE DISCONTINUE='0' AND DEPARTMENT='10' AND TEAM='C' AND EMP_ID != '100202'
            """
            cursor.execute(query)
            email_results = cursor.fetchall()
            conn.close()

            # Extract email addresses into a list
            email_ids = [row[0] for row in email_results]

        except Exception as e:
            return Response({"error": "Failed to fetch email IDs from the database", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not email_ids:
            return Response({"error": "No email IDs found in the database"}, status=status.HTTP_404_NOT_FOUND)

        # Step 2: Call API-1 to get the access token
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

        # Step 3: Loop through email IDs and call API-2 and API-3
        user_availability = []

        for user_email in email_ids:
            # Validate email format
            if not re.match(r"[^@]+@[^@]+\.[^@]+", user_email):
                continue  # Skip invalid email addresses

            # API-2: Get user details
            api2_url = f"https://graph.microsoft.com/v1.0/users/{user_email}"
            api2_headers = {
                "Authorization": f"Bearer {access_token}"
            }

            try:
                api2_response = requests.get(api2_url, headers=api2_headers)
                api2_response.raise_for_status()
                api2_data = api2_response.json()

                # Retrieve user ID
                user_id = api2_data.get("id")

                if not user_id:
                    continue  # Skip if user ID not found
            except requests.exceptions.RequestException:
                continue  # Skip if API-2 fails for this email

            # API-3: Get user presence
            api3_url = f"https://graph.microsoft.com/v1.0/users/{user_id}/presence"
            api3_headers = {
                "Authorization": f"Bearer {access_token}"
            }

            try:
                api3_response = requests.get(api3_url, headers=api3_headers)
                api3_response.raise_for_status()
                api3_data = api3_response.json()

                # Extract availability and add to the results
                availability = api3_data.get("availability", "Unknown")
                user_availability.append({
                    "email": user_email,
                    "availability": availability
                })

            except requests.exceptions.RequestException:
                continue  # Skip if API-3 fails for this user

        # Step 4: Return the availability of all users
        return Response(user_availability, status=status.HTTP_200_OK)
