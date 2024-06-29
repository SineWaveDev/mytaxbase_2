from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import pymssql

# Connection parameters
SERVER = '3.108.198.195'
DATABASE = 'indiataxes_com_indiataxes'
USERNAME = 'indiataxes_com_indiataxes'
PASSWORD = 'SW_02ITNETCOM'

def get_db_connection():
    return pymssql.connect(SERVER, USERNAME, PASSWORD, DATABASE)

@api_view(['POST'])
def check_credentials(request):
    user_id = request.data.get('user_id')
    user_pwd = request.data.get('user_pwd')

    if not user_id or not user_pwd:
        return Response({"error": "User ID and password are required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        connection = get_db_connection()
        cursor = connection.cursor(as_dict=True)
        query = "SELECT CUST_ID, CUST_PWD FROM CS_CUSTOMER WHERE CUST_ID = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()

        if result:
            if result['CUST_PWD'] == user_pwd:
                return Response({"message": "Login successful!"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Incorrect password."}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"error": "User ID not found."}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    finally:
        cursor.close()
        connection.close()
