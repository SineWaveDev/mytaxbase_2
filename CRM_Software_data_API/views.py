from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import pyodbc
from datetime import datetime

class InsertCallAPIView(APIView):
    def post(self, request):
        try:
            headers = request.headers

            def parse_date(date_str):
                try:
                    # Try parsing if date exists and is not already in correct format
                    return datetime.strptime(date_str, "%Y-%m-%d").date()
                except:
                    # Try other common formats (like DD/MM/YYYY or MM/DD/YYYY)
                    for fmt in ("%d/%m/%Y", "%m/%d/%Y", "%Y-%m-%d"):
                        try:
                            return datetime.strptime(date_str, fmt).date()
                        except:
                            continue
                    return None  # If all fail

            # Get and sanitize fields
            date = parse_date(headers.get("DATE", ""))
            next_action_date = parse_date(headers.get("NEXT_ACTION_DATE", ""))

            emp_id = headers.get("EMP_ID", "")
            name_of_org = headers.get("NAME_OF_ORGANIZATION", "")
            contact_person = headers.get("CONTACT_PERSON", "")
            area = headers.get("AREA", "")
            city = headers.get("CITY", "")
            contact_no = headers.get("CONTACT_NO", "")
            email_id = headers.get("EMAIL_ID", "")
            product_id = headers.get("PRODUCT_ID", "")
            call_status = headers.get("CALL_STATUS", "")
            call_type = headers.get("CALL_TYPE", "")
            prospect_id = headers.get("PROSPECT_ID", "")
            client_response = headers.get("CLIENT_RESPONSE", "")
            next_action = headers.get("NEXT_ACTION", "")
            travel_time = headers.get("TRAVEL_TIME", "")
            atcall_time = headers.get("ATCALL_TIME", "")
            transfer_to = headers.get("TRANSFER_TO", "")
            source = headers.get("SOURCE", "")
            cust_id = headers.get("CUST_ID", "")
            nature_of_call = headers.get("NATURE_OF_CALL", "")
            dept_id = headers.get("DEPT_ID", "")

            # Connection string
            conn_str = (
                "DRIVER={ODBC Driver 17 for SQL Server};"
                "SERVER=3.108.198.195;"
                "DATABASE=indiataxes_com_indiataxes;"
                "UID=indiataxes_com_indiataxes;"
                "PWD=SW_02ITNETCOM;"
            )
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()

            query = """
                INSERT INTO S_MIS_DAILY_CALLS (
                    DATE, EMP_ID, NAME_OF_ORGANIZATION, CONTACT_PERSON, AREA,
                    CITY, CONTACT_NO, EMAIL_ID, PRODUCT_ID, CALL_STATUS, CALL_TYPE,
                    PROSPECT_ID, CLIENT_RESPONSE, NEXT_ACTION, NEXT_ACTION_DATE,
                    TRAVEL_TIME, ATCALL_TIME, TRANSFER_TO, SOURCE, CUST_ID,
                    NATURE_OF_CALL, DEPT_ID
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            cursor.execute(query, (
                date, emp_id, name_of_org, contact_person, area, city, contact_no, email_id,
                product_id, call_status, call_type, prospect_id, client_response, next_action,
                next_action_date, travel_time, atcall_time, transfer_to, source,
                cust_id, nature_of_call, dept_id
            ))

            conn.commit()
            cursor.close()
            conn.close()

            return Response({"message": "Data inserted successfully"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
