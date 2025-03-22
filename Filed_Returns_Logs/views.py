from django.urls import path
from rest_framework.decorators import api_view
from rest_framework.response import Response
import pymssql

# Database connection parameters
SERVER = '3.108.198.195'
DATABASE = 'indiataxes_com_indiataxes'
USERNAME = 'indiataxes_com_indiataxes'
PASSWORD = 'SW_02ITNETCOM'

# API View to insert data
@api_view(['POST'])
def insert_filed_return(request):
    try:
        data = request.data
        cust_id = data.get('Cust_ID')
        prod_id = data.get('Prod_ID')
        filing_type = data.get('Filing_Type')
        filing_date = data.get('Filing_Date')

        if not all([cust_id, prod_id, filing_type, filing_date]):
            return Response({'error': 'All fields are required'}, status=400)

        # Connect to the database
        conn = pymssql.connect(server=SERVER, user=USERNAME, password=PASSWORD, database=DATABASE)
        cursor = conn.cursor()

        # Insert data
        query = """
            INSERT INTO Logs_FiledReturns (Cust_ID, Prod_ID, Filing_Type, Filing_Date)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (cust_id, prod_id, filing_type, filing_date))
        conn.commit()

        cursor.close()
        conn.close()
        return Response({'message': 'Data inserted successfully'}, status=201)

    except Exception as e:
        return Response({'error': str(e)}, status=500)