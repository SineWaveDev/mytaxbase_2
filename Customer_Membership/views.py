# views.py
from django.http import JsonResponse
from rest_framework.decorators import api_view
import pymssql
from django.conf import settings

# Connection parameters
SERVER = '3.108.198.195'
DATABASE = 'indiataxes_com_indiataxes'
USERNAME = 'indiataxes_com_indiataxes'
PASSWORD = 'SW_02ITNETCOM'

@api_view(['GET'])
def check_customer_age(request):
    cust_id = request.GET.get('cust_id')
    
    if not cust_id:
        return JsonResponse({"error": "Customer ID is required"}, status=400)

    # Initialize result dictionary
    result = {
        "membership": None,
        "platinum": {},
        "gold": {},
        "silver": {}
    }

    # Connect to the database
    try:
        conn = pymssql.connect(server=SERVER, user=USERNAME, password=PASSWORD, database=DATABASE)
        cursor = conn.cursor()

        # Check payment records for Platinum (10 years)
        platinum_query = """
            SELECT MIN(date) AS first_payment_date, MAX(date) AS last_payment_date
            FROM S_AUC_PAYMENT_REGISTER 
            WHERE date BETWEEN DATEADD(YEAR, -10, GETDATE()) AND GETDATE() 
            AND CUST_ID = %s
            GROUP BY CUST_ID;
        """
        cursor.execute(platinum_query, (cust_id,))
        platinum_result = cursor.fetchone()

        if platinum_result and platinum_result[0]:  # Check if result is not None
            result["membership"] = "Platinum"
            result["platinum"]["first_payment_date"] = platinum_result[0]
            result["platinum"]["last_payment_date"] = platinum_result[1]

        # Check for Gold membership (5 years)
        gold_query = """
            SELECT MIN(date) AS first_payment_date, MAX(date) AS last_payment_date
            FROM S_AUC_PAYMENT_REGISTER 
            WHERE date BETWEEN DATEADD(YEAR, -5, GETDATE()) AND GETDATE() 
            AND CUST_ID = %s
            GROUP BY CUST_ID;
        """
        cursor.execute(gold_query, (cust_id,))
        gold_result = cursor.fetchone()

        if gold_result and gold_result[0]:  # Check if result is not None
            if result["membership"] is None:  # Only set membership if not already set
                result["membership"] = "Gold"
            result["gold"]["first_payment_date"] = gold_result[0]
            result["gold"]["last_payment_date"] = gold_result[1]

        # Check for Silver membership (1 year)
        silver_query = """
            SELECT MIN(date) AS first_payment_date, MAX(date) AS last_payment_date
            FROM S_AUC_PAYMENT_REGISTER 
            WHERE date BETWEEN DATEADD(YEAR, -1, GETDATE()) AND GETDATE() 
            AND CUST_ID = %s
            GROUP BY CUST_ID;
        """
        cursor.execute(silver_query, (cust_id,))
        silver_result = cursor.fetchone()

        if silver_result and silver_result[0]:  # Check if result is not None
            if result["membership"] is None:  # Only set membership if not already set
                result["membership"] = "Silver"
            result["silver"]["first_payment_date"] = silver_result[0]
            result["silver"]["last_payment_date"] = silver_result[1]

        # If no membership found, set to No membership
        if result["membership"] is None:
            result["membership"] = "No membership"

        return JsonResponse(result, status=200)

    except pymssql.DatabaseError as e:
        return JsonResponse({"error": str(e)}, status=500)
    finally:
        if conn:
            conn.close()
