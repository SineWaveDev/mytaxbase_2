import pymssql
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from django.contrib.auth.hashers import check_password
from .models import User, RewardTransaction

# Connection parameters for SQL Server (to be used in functions)
SERVER = '3.108.198.195'
DATABASE = 'indiataxes_com_indiataxes'
USERNAME = 'indiataxes_com_indiataxes'
PASSWORD = 'SW_02ITNETCOM'


def get_db_connection():
    """
    Establish a connection to the SQL Server database.
    Returns: pymssql connection object
    """
    return pymssql.connect(
        server=SERVER,
        user=USERNAME,
        password=PASSWORD,
        database=DATABASE
    )


# 1. User Login and First-Time Bonus
@api_view(['POST'])
def user_login(request):
    user_id = request.data.get('userid')
    password = request.data.get('password')

    try:
        # Fetch user from the external SQL database
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM UserAccounts WHERE user_id = %s", (user_id,))
        user_data = cursor.fetchone()

        if user_data is None:
            return Response({"status": "error", "message": "User not found"}, status=404)

        user = User(user_id=user_data[0], password=user_data[1], coin_balance=user_data[2])

        # Check if the password matches (assuming it's hashed)
        if not check_password(password, user.password):
            return Response({"status": "error", "message": "Invalid credentials"}, status=401)

        # First-time login: award 100 coins
        if user.coin_balance == 0:  # assuming 0 balance means it's the first login
            new_balance = user.coin_balance + 100
            cursor.execute("UPDATE UserAccounts SET coin_balance = %s WHERE user_id = %s", (new_balance, user_id))
            connection.commit()

            # Log transaction
            cursor.execute("INSERT INTO UserRewardTransactions (user_id, action_type, coins_awarded, timestamp) VALUES (%s, %s, %s, %s)",
                           (user_id, "First Login Bonus", 100, timezone.now()))
            connection.commit()

        # Return user details and coin balance
        return Response({
            "status": "success",
            "auth_token": "dummy_token",  # You can replace this with a real token generation process
            "user_details": {
                "user_id": user.user_id,
                "coin_balance": user.coin_balance,
            }
        })

    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=500)

    finally:
        cursor.close()
        connection.close()


# 2. Update Coins API
@api_view(['POST'])
def update_coins(request):
    user_id = request.data.get('userId')
    action_type = request.data.get('actionType')
    coins_earned = request.data.get('coinsEarned')

    try:
        # Fetch user from the external SQL database
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT coin_balance FROM UserAccounts WHERE user_id = %s", (user_id,))
        user_data = cursor.fetchone()

        if user_data is None:
            return Response({"status": "error", "message": "User not found"}, status=404)

        current_balance = user_data[0]
        new_balance = current_balance + coins_earned

        # Update the user's coin balance in the database
        cursor.execute("UPDATE UserAccounts SET coin_balance = %s WHERE user_id = %s", (new_balance, user_id))
        connection.commit()

        # Log the transaction
        cursor.execute("INSERT INTO UserRewardTransactions (user_id, action_type, coins_awarded, timestamp) VALUES (%s, %s, %s, %s)",
                       (user_id, action_type, coins_earned, timezone.now()))
        connection.commit()

        return Response({
            "status": "success",
            "new_balance": new_balance,
            "action_type": action_type,
            "coins_earned": coins_earned,
        })

    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=500)

    finally:
        cursor.close()
        connection.close()


# 3. Get User Balance
@api_view(['GET'])
def get_user_balance(request, user_id):
    try:
        # Fetch user balance from the external SQL database
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT coin_balance FROM UserAccounts WHERE user_id = %s", (user_id,))
        user_data = cursor.fetchone()

        if user_data is None:
            return Response({"status": "error", "message": "User not found"}, status=404)

        coin_balance = user_data[0]

        return Response({
            "status": "success",
            "user_id": user_id,
            "coin_balance": coin_balance,
            "last_updated_at": timezone.now(),
        })

    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=500)

    finally:
        cursor.close()
        connection.close()


# 4. Log Transaction
@api_view(['POST'])
def log_transaction(request):
    user_id = request.data.get('userId')
    action_type = request.data.get('actionType')
    coins_awarded = request.data.get('coinsAwarded')
    timestamp = request.data.get('timestamp')

    try:
        # Log the transaction into the external SQL database
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO UserRewardTransactions (user_id, action_type, coins_awarded, timestamp) VALUES (%s, %s, %s, %s)",
                       (user_id, action_type, coins_awarded, timestamp))
        connection.commit()

        return Response({
            "status": "success",
            "message": "Transaction logged successfully",
        })

    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=500)

    finally:
        cursor.close()
        connection.close()
