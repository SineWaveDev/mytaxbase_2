from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response
from email.mime.text import MIMEText
import smtplib
import random

# List to store all generated OTPs
generated_otps = []


class ClientAPI(APIView):
    """
    This API is for stock buying and selling
    """

    def generate_otp(self):
        return str(random.randint(100000, 999999))

    def get(self, request, format=None):
        global generated_otps  # Use the global variable
        Email = request.GET.get("Email")
        username = request.GET.get("username")
        product_name = request.GET.get("product_name")

        print('Email:', Email)
        print('Username:', username)
        print('Product Name:', product_name)

        # Generate a 6-digit OTP
        otp = self.generate_otp()

        # Add the generated OTP to the list
        generated_otps.append(otp)

        # Set up SMTP connection
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'support@sinewave.co.in'
        smtp_password = 'qqmo cyrz pygw izjp'
        sender_email = 'support@sinewave.co.in'

        # Compose and send email with OTP
        message_body = f'Dear {username},\n\nYour OTP for {product_name} application forget password is: {otp}\n\nPlease do not share the OTP with others.\n\nThanks and Regards,\nSinewave Computer Services PVT.LTD'

        # Use 'plain' instead of 'html' for plain text
        message = MIMEText(message_body, 'plain')
        message['Subject'] = 'OTP For Login'
        message['From'] = sender_email
        message['To'] = Email

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(message)

        data = {
            'message': 'Success',
            'otp': otp  # Include the OTP in the response
        }

        return Response(data)


class VerifyOtpAPI(APIView):
    """
    API to verify OTP for stock buying and selling
    """

    def post(self, request, format=None):
        global generated_otps  # Use the global variable

        # Retrieve data from the request
        email = request.data.get("email")
        username = request.data.get("username")
        product_name = request.data.get("product_name")
        user_entered_otp = request.GET.get("otp")  # Update this line

        print('User Entered OTP:', user_entered_otp)

        if generated_otps:
            print("generated_otps", generated_otps)
            # Get the last generated OTP from the list
            last_generated_otp = generated_otps[-1]

            # Logging for debugging
            print('Last Generated OTP:', last_generated_otp)

            # Check if last_generated_otp is not None before using strip()
            if last_generated_otp is not None:
                if user_entered_otp.strip().lower() == last_generated_otp.strip().lower():
                    # Remove the last generated OTP from the list after successful verification
                    generated_otps.pop()
                    response_data = {'message': 'OTP verification successful'}
                else:
                    response_data = {'message': 'Invalid OTP'}
            else:
                response_data = {'message': 'No OTP found for the given email'}
        else:
            response_data = {'message': 'No OTP found for the given email'}

        return Response(response_data)
