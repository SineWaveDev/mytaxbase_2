from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
import pymssql
from datetime import datetime

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
            created_at = datetime.fromtimestamp(data.get('created_at') / 1000.0).strftime('%Y-%m-%d %H:%M:%S')
            topic = data.get('topic')
            delivery_attempt = data.get('delivery_attempt')
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
