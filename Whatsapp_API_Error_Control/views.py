from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pymssql
from datetime import datetime
import dateutil.parser

class WebhookView(APIView):
    def post(self, request, *args, **kwargs):
        # Extract data from request
        data = request.data

        # Connection parameters
        server = '3.108.198.195'
        database = 'indiataxes_com_indiataxes'
        username = 'indiataxes_com_indiataxes'
        password = 'SW_02ITNETCOM'

        # Connect to the database
        try:
            connection = pymssql.connect(server, username, password, database)
            cursor = connection.cursor()
        except pymssql.InterfaceError:
            return Response({'error': 'Could not connect to the database.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Insert data into the table
        try:
            created_at = dateutil.parser.isoparse(data.get('created_at')).strftime('%Y-%m-%d %H:%M:%S')
            topic = data.get('topic')
            delivery_attempt = int(data.get('delivery_attempt'))
            app_id = data.get('app_id')
            webhook_id = data.get('webhook_id')
            project_id = data.get('project_id')
            data_field = str(data.get('data'))

            insert_query = """
            INSERT INTO Taxbase_WhatsAppApi (Created_at, Topic, Delivery_attempt, App_id, Webhook_id, Project_id, Data)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (created_at, topic, delivery_attempt, app_id, webhook_id, project_id, data_field))
            connection.commit()
        except Exception as e:
            connection.rollback()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        finally:
            cursor.close()
            connection.close()

        return Response({'status': 'success', 'data': data}, status=status.HTTP_200_OK)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import pymssql  # SQL Server connector
from datetime import datetime

class TriggerCampaignView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data

            # Extract nested values
            message_data = data.get("data", {}).get("message", {})

            phone_number = message_data.get("phone_number")
            interest_text = message_data.get("message_content", {}).get("text", "").strip()
            user_name = message_data.get("userName", "Sinewave Computer services")

            if not phone_number or not interest_text:
                return Response({'error': 'Missing phone_number or interest_status in payload.'},
                                status=status.HTTP_400_BAD_REQUEST)

            interest_lower = interest_text.lower()
            if interest_lower == "interested":
                campaign_name = "interested"
            elif interest_lower == "not interested":
                campaign_name = "not_interested"
            else:
                return Response({'error': 'Invalid value for interest_status. Use "Interested" or "Not Interested".'},
                                status=status.HTTP_400_BAD_REQUEST)

            # API details
            api_url = "https://backend.api-wa.co/campaign/smartping/api/v2"
            api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY0ZGRmMmM4MGMzZjY5MGU4MTY3Nzc3OSIsIm5hbWUiOiJTaW5ld2F2ZSBDb21wdXRlciBzZXJ2aWNlcyIsImFwcE5hbWUiOiJBaVNlbnN5IiwiY2xpZW50SWQiOiI2NGRkZjJjODBjM2Y2OTBlODE2Nzc3NzQiLCJhY3RpdmVQbGFuIjoiTk9ORSIsImlhdCI6MTY5MjI2NzIwOH0.r5cHWBFTMs_4F70F4z3bb6MGTmkfSN1oOOM5PSaOUT0"  # Replace with your actual key

            payload = {
                "apiKey": api_key,
                "campaignName": campaign_name,
                "destination": phone_number,
                "userName": user_name,
                "templateParams": [],
                "source": "new-landing-page form",
                "media": {},
                "buttons": [],
                "carouselCards": [],
                "location": {},
                "attributes": {},
                "paramsFallbackValue": {}
            }

            response = requests.post(api_url, json=payload)

            # Save to database regardless of external API success
            try:
                conn = pymssql.connect(
                    server='3.108.198.195',
                    user='indiataxes_com_indiataxes',
                    password='SW_02ITNETCOM',
                    database='Campaigns'
                )
                cursor = conn.cursor()
                insert_query = """
                    INSERT INTO LexLegis_Launchpad (userName, phone_number, text, campaign_name)
                    VALUES (%s, %s, %s, %s)
                """
                cursor.execute(insert_query, (user_name, phone_number, interest_text, "LexLegis_Launchpad"))
                conn.commit()
                conn.close()
            except Exception as db_error:
                return Response({'error': 'Database error', 'details': str(db_error)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            if response.status_code == 200:
                return Response({
                    'status': 'API called and data saved successfully',
                    'campaign': campaign_name,
                    'phone_number': phone_number,
                    'user': user_name
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'warning': 'API failed but data saved in database',
                    'campaign': campaign_name,
                    'api_response': response.text
                }, status=status.HTTP_207_MULTI_STATUS)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
