# TDS_Validate_Challan_API/views.py

import requests
import base64
import json
import time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ChainAPIsView(APIView):
    def post(self, request):
        """
        This endpoint will sequentially call five APIs, passing data from one to the next.
        Expects a JSON payload with necessary initial parameters.
        """
        # Extract initial parameters from the request body
        initial_data = request.data
        username = initial_data.get('entity')
        password = initial_data.get('pass')  # Plain password, will be Base64 encoded

        if not username or not password:
            return Response(
                {"error": "Both 'entity' and 'pass' fields are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Encode the password to Base64
        encoded_password = base64.b64encode(password.encode()).decode()

        # Initialize headers
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0'
        }

        session = requests.Session()

        # Step 1: First API Call (GET)
        first_api_url = "https://eportal.incometax.gov.in/iec/foservices/"
        try:
            first_response = session.get(first_api_url, headers=headers, timeout=10)
            first_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return Response({"error": f"First API call failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        # Step 2: Second API Call (POST) with Username
        second_api_url = "https://eportal.incometax.gov.in/iec/loginapi/login"
        second_api_payload = {
            "entity": username,
            "serviceName": "loginService"
        }
        print("second_api_payload:",second_api_payload)

        try:
            time.sleep(1)  # Respectful delay
            second_response = session.post(second_api_url, headers=headers, json=second_api_payload, timeout=10)
            second_response.raise_for_status()
            second_data = second_response.json()
            print("second_API_response:",second_data)
        except requests.exceptions.RequestException as e:
            return Response({"error": f"Second API call failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError:
            return Response({"error": "Second API response is not valid JSON."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the second API responded with success
        if not second_data.get('messages') or second_data['messages'][0].get('desc') != "OK":
            return Response(
                {"error": "Second API login not successful.", "details": second_data.get('messages')},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Step 3: Third API Call (POST) with Additional Data
        third_api_url = "https://eportal.incometax.gov.in/iec/loginapi/login"
        third_api_payload = {
            "errors": second_data.get('errors'),  # Correct the spelling here
            "reqId": second_data.get('reqId'),
            "entity": second_data.get('entity'),
            "entityType": second_data.get('entityType'),
            "role": second_data.get('role'),
            "uidValdtnFlg": second_data.get('uidValdtnFlg'),
            "aadhaarMobileValidated": second_data.get('aadhaarMobileValidated'),
            "secAccssMsg": second_data.get('secAccssMsg'),
            "secLoginOptions": second_data.get('secLoginOptions'),
            "exemptedPan": second_data.get('exemptedPan'),
            "userConsent": second_data.get('userConsent'),
            "imgByte": None,  # Ensure imgByte is null
            "pass": encoded_password,  # Correctly encoded password
            "passValdtnFlg": None,
            "otpGenerationFlag": None,
            "otp": None,
            "otpValdtnFlg": None,
            "otpSourceFlag": None,
            "contactPan": None,
            "contactMobile": None,
            "contactEmail": None,
            "email": None,
            "mobileNo": None,
            "forgnDirEmailId": None,
            "imagePath": None,
            "serviceName": "loginService"
        }

        # Print the payload before sending the request (for debugging)
        print("Third API Payload:", third_api_payload)

        try:
            time.sleep(1.8)  # Respectful delay
            third_response = session.post(third_api_url, headers=headers, json=third_api_payload, timeout=50)
            third_response.raise_for_status()
            third_data = third_response.json()
            print("third_response:", third_data)
        except requests.exceptions.RequestException as e:
            return Response({"error": f"Third API call failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError:
            return Response({"error": "Third API response is not valid JSON."}, status=status.HTTP_400_BAD_REQUEST)

        # # Check if the third API responded with success
        # if not third_data.get('messages') or third_data['messages'][0].get('desc') != "OK":
        #     return Response(
        #         {"error": "Third API login not successful.", "details": third_data.get('messages')},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )
        
        # Step 4: Fourth API Call (POST)
        fourth_api_url = "https://eportal.incometax.gov.in/iec/loginapi/login"
        fourth_api_payload = {
            "clientIp": third_data.get('clientIp'),
            "erros": third_data.get('errors'),
            "reqId": third_data.get('reqId'),
            "entity": third_data.get('entity'),
            "entityType": third_data.get('entityType'),
            "role": third_data.get('role'),
            "uidValdtnFlg": third_data.get('uidValdtnFlg'),
            "aadhaarMobileValidated": third_data.get('aadhaarMobileValidated'),
            "secAccssMsg": third_data.get('secAccssMsg'),
            "secLoginOptions": third_data.get('secLoginOptions'),
            "exemptedPan": third_data.get('exemptedPan'),
            "userConsent": third_data.get('userConsent'),
            "imgByte": third_data.get('imgByte'),
            "otpGenerationFlag": "true",
            "otpValdtnFlg": "true",
            "remark": "Continue",
            "serviceName": "loginService"
        }
        print("fourth_api_payload:", fourth_api_payload)

        try:
            time.sleep(2)  # Respectful delay
            fourth_response = session.post(fourth_api_url, headers=headers, json=fourth_api_payload, timeout=10)
            fourth_response.raise_for_status()
            fourth_data = fourth_response.json()
            print("Fourth_API_response:",fourth_data)
        except requests.exceptions.RequestException as e:
            return Response({"error": f"Fourth API call failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError:
            return Response({"error": "Fourth API response is not valid JSON."}, status=status.HTTP_400_BAD_REQUEST)

        # # Check if the fourth API responded with success
        # if not fourth_data.get('messages') or fourth_data['messages'][0].get('desc') != "OK":
        #     return Response(
        #         {"error": "Fourth API login not successful.", "details": fourth_data.get('messages')},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )

        # Step 5: Fifth API Call (POST) for Payment History
        fifth_api_url = "https://eportal.incometax.gov.in/iec/PaymentAPI/auth/challan/paymenthistory"
        fifth_api_payload = {
            "header": {"formName": "PO-03-PYMNT"},
            "formData": {
                "pan": fourth_data.get("entity"),
                "loggedInUserID": fourth_data.get("entity"),
                "loggedInUserType": fourth_data.get("role")
            }
        }

        print("fifth_api_payload:", fifth_api_payload)

        try:
            time.sleep(1.5)  # Respectful delay
            fifth_response = session.post(fifth_api_url, headers=headers, json=fifth_api_payload, timeout=10)
            fifth_response.raise_for_status()
            fifth_data = fifth_response.json()
            print("fifth_Response:",fifth_data)
        except requests.exceptions.RequestException as e:
            return Response({"error": f"Fifth API call failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        except json.JSONDecodeError:
            return Response({"error": "Fifth API response is not valid JSON."}, status=status.HTTP_400_BAD_REQUEST)

        # Optionally, process the fifth_data as needed before returning
        return Response(fifth_data, status=status.HTTP_200_OK)
