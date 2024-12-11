from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from urllib.parse import urlencode
import requests




class SendEmailAPI(APIView):
    def post(self, request, *args, **kwargs):
        # Get parameters from the URL query parameters
        name = request.query_params.get('name')
        email = request.query_params.get('email')
        webinar_subject = request.query_params.get('webinar_subject')
        webinar_date = request.query_params.get('webinar_date')
        webinar_time = request.query_params.get('webinar_time')
        webinar_url = request.query_params.get('webinar_url')

        # Additional parameter for CC
        cc_email = "rupesh.k@sinewave.in"

        # Email configuration
        sender_email = "crm@sinewave.co.in"
        receiver_email = email
        subject = f"FW: Webinar Registration Successful - {webinar_subject}"

        # Modify the body to include one blank line after each line
        body = f"Dear {name},\n\n" \
               f"Webinar Subject: {webinar_subject}\n\n" \
               f"Date: {webinar_date}\n\n" \
               f"Time: {webinar_time}\n\n" \
               f"Webinar URL: {webinar_url}"

        # Append the provided message to the email body
        closing_message = (
            "\n\nIn case you need support, please feel free to email us at rupesh.k@sinewave.in."
            "\n\nThanking You,\nYours Truly,\nwww.sinewave.co.in"
        )

        body += closing_message

        # Gmail SMTP server and port
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        # Your Gmail account credentials
        username = "crm@sinewave.co.in"
        password = "fzjv eaaj kdcv svqr" 

        # Create the email message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Cc"] = cc_email  # Add CC recipient
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        # Connect to the SMTP server and send the email
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(username, password)
                server.sendmail(sender_email, [receiver_email, cc_email],
                                message.as_string())

            return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class SendEmailAPIHTML(APIView):
    def post(self, request, *args, **kwargs):
        # Get parameters from the URL query parameters
        name = request.query_params.get('name')
        email = request.query_params.get('email')
        url = request.query_params.get('url')
        
        # Email content with formatting for the 'name' parameter
        email_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Password Reset Information</title>
        </head>
        <body>
            <table align="center" width="700px" id="container" cellspacing="0" cellpadding="0" style="border:5px solid #0294cc;">
                <tr>
                    <td>
                        <table bgcolor="#9fd1e4" width="700px" cellspacing="0" cellpadding="0">
                            <tr>
                                <td width="500" align="center" style="font-size:34px; color:black; font-family:calibri; background-color:#9fd1e4;">Password Reset Information</td>
                                <td width="200" align="right" style=""><img src="http://www.sinewave.co.in/images/Sinewave-resetpass.png" alt="Sinewave Logo"/></td>
                            </tr>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td height="20"></td>
                </tr>
                <tr width="650">
                    <td align="left" height="20" style="font-size:16px; color:#0764ad; font-family:calibri; padding-left:20px;">
                        Dear {name},<br/> Thank you for contacting Sinewave. Click the button below to reset your password.
                    </td>
                </tr>
                <tr>
                    <td height="40"></td>
                </tr>
                <tr>
                    <td align="center">
                        <table height="40" width="210px" cellspacing="0" cellpadding="0" border="0">
                            <tr>
                                <td align="center" style="background:#eb822c; color:white; font-family:arial; padding:10px; font-size:14px;">
                                    <a href={url} style="color:white; text-decoration:none; padding:5px;">
                                        <b>RESET YOUR PASSWORD</b>
                                    </a>
                                </td>
                            </tr>
                            <tr>
                                <td height="5" align="center" style="background:#bd6117; color:white; font-family:arial; font-size:14px;"></td>
                            </tr>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td height="20"></td>
                </tr>
                <tr>
                    <td align="left" width="650" style="font-size:16px; color:black; font-family:calibri; padding-left:20px;">
                        <b>IMP Note: </b>This link is valid for one-time use only. Also, reset your password within 15 min. after that it's auto-expired. Your request time is 14/02/2024 15:42:58.
                    </td>
                </tr>
                <tr>
                    <td valign="top" align="center">
                        <table align="center" width="200" border="0" cellspacing="0" cellpadding="0">
                            <tr>
                                <td height="40"></td>
                            </tr>
                            <tr>
                                <td align="center">
                                    <table align="center" width="300" border="0" style="font-family:arial; font-size:14px;">
                                        <tr>
                                            <td><b>To Reset your Password :</b></td>
                                        </tr>
                                        <tr>
                                            <td height="10"></td>
                                        </tr>
                                        <tr>
                                            <td style="line-height:25px;">
                                                <ul>
                                                    <li>Enter your current password.</li>
                                                    <li>Enter your new password.</li>
                                                    <li>Confirm your new password.</li>
                                                    <li>Click "Submit".</li>
                                                </ul>
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td height="10"></td>
                </tr>
                <tr>
                    <td align="center" height="20" style="font-size:18px; color:black; font-family:calibri; padding-left:40px;">
                        <b>Still having trouble? Call Helpline No. : (020)49091000.</b>
                    </td>
                </tr>
                <tr>
                    <td height="40"></td>
                </tr>
                <tr>
                    <td align="center" height="20" style="font-size:11px; color:black; font-family:arial; background-color:#f2f2f2;padding-top:5px;padding-bottom:5px;">
                        Please do not reply to this email. Emails sent to this address will not be answered.
                    </td>
                </tr>
                <tr>
                    <td height="20"></td>
                </tr>
                <tr>
                    <td align="left" style="font-size:11px; font-family:arial; color:black; padding-left:20px;">
                        <table style="font-size:12px; font-family:arial;">
                            <tr>
                                <td>Thanks & Regards,</td>
                            </tr>
                            <tr>
                                <td>Administrator,</td>
                            </tr>
                            <tr>
                                <td>Sinewave Computer Services Pvt. Ltd.</td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>

        """
    

        # Email configuration
        sender_email = "crm@sinewave.co.in"
        receiver_email = email
        subject = "For Change Password On Sinewave Portel"
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject

        # Attach HTML content to the email
        message.attach(MIMEText(email_content, 'html'))

        # Send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login('crm@sinewave.co.in', 'fzjv eaaj kdcv svqr')
            text = message.as_string()
            server.sendmail(sender_email, receiver_email, text)
            return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)



class SendEmailTeamControl(APIView):
    def post(self, request, *args, **kwargs):
        # Get parameters from the URL query parameters
        email = request.query_params.get('email')
        url = request.query_params.get('url')
        companycode = request.query_params.get('companycode')
        username = request.query_params.get('username')
        password = request.query_params.get('password')
        
        # Construct the email body with the provided message
        body = f"Dear Sir/Madam,\n\n" \
               f"Thanks for registering with us. We appreciate your interest in our products.\n\n" \
               f"Your Credentials for Sinewave TeamControl are as following,\n\n" \
               f"URL : {url}\n" \
               f"Company Code : {companycode}\n" \
               f"Username : {username}\n" \
               f"Password : {password}\n\n" \
               f"Thanking you,\n" \
               f"Yours Truly,\n" \
               f"Administrator,\n" \
               f"Sinewave Computer Services Pvt. Ltd.\n" \
               f"http://www.sinewave.co.in"

        # Email configuration
        sender_email = "crm@sinewave.co.in"
        receiver_email = email
        subject = "Credentials for Sinewave TeamControl"
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject

        # Attach plain text content to the email
        message.attach(MIMEText(body, 'plain'))

        # Send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login('crm@sinewave.co.in', 'fzjv eaaj kdcv svqr')
            text = message.as_string()
            server.sendmail(sender_email, receiver_email, text)
            return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)



class SendEmailTaxbaseLicenseVerification(APIView):
    def post(self, request, *args, **kwargs):
        # Get parameters from the JSON request body
        # email = request.query_params.get('email')
        # url = request.query_params.get('url')

        data = request.data
        email = data.get('email')
        url = data.get('url')
        
        # Construct the email body with the provided message
        body = f"Dear Sir/Madam,\n\n" \
               f"To authenticate your license kindly click on below link or paste in browser\n" \
               f"{url}\n\n" \
               f"If you did not request or need help, please let us know immediately at license@sinewave.in\n\n" \
               f"Thanks for connecting with Sinewave!\n" \
               f"Yours truly,\n" \
               f"Support Administrator,\n" \
               f"Sinewave Computer Services Pvt. Ltd."

        # Email configuration
        sender_email = "crm@sinewave.co.in"
        receiver_email = email
        subject = "Taxbase License Verification"
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject

        # Attach plain text content to the email
        message.attach(MIMEText(body, 'plain'))

        # Send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login('crm@sinewave.co.in', 'fzjv eaaj kdcv svqr')
            text = message.as_string()
            server.sendmail(sender_email, receiver_email, text)
            return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)




class ForgotPassword(APIView):
    def post(self, request, *args, **kwargs):
        # Get parameters from the URL query parameters
        id = request.query_params.get('id')
        password = request.query_params.get('password')
        email = request.query_params.get('email')
        
        # Email content with formatting for the 'name' parameter
        email_content = f"""
       <p align=justify><SPAN style="FONT-SIZE: 10pt; FONT-FAMILY: Arial" > Dear Sir/Madam,</SPAN></p><p style="text-align: justify" > <SPAN style="font-size: 10pt; font-family: Arial">Your login details as follows:</SPAN></p><p align=justify> <SPAN style="FONT-SIZE: 10pt; FONT-FAMILY: Arial" >  Login ID : {id}</SPAN></p>  <p align=justify><SPAN style="FONT-SIZE: 10pt; FONT-FAMILY: Arial" >  Password : {password}</SPAN></p>  <br /><p style="text-align: justify" ><span style="font-size: 10pt; font-family: Arial">Thanking you,<br />Yours Truly,<br />Administrator,<br /><a href=http://www.sinewave.co.in >www.sinewave.co.in </a> </span></p>

        """
    

        # Email configuration
        sender_email = "crm@sinewave.co.in"
        receiver_email = email
        subject = "Forgot Password"
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject

        # Attach HTML content to the email
        message.attach(MIMEText(email_content, 'html'))

        # Send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login('crm@sinewave.co.in', 'fzjv eaaj kdcv svqr')
            text = message.as_string()
            server.sendmail(sender_email, receiver_email, text)
            return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)







class FetchDataAPIView(APIView):
    def get(self, request):
        pincode = request.query_params.get('pincode', None)
        if not pincode:
            return Response({'error': 'Pincode is required'}, status=status.HTTP_400_BAD_REQUEST)

        api_url = 'https://api.data.gov.in/resource/9115b89c-7a80-4f54-9b06-21086e0f0bd7'
        api_key = '579b464db66ec23bdd000001d16ce4b1164e435344fa6d817c33e649'
        params = {
            'api-key': api_key,
            'format': 'json',
            'filters[pincode]': pincode
        }

        # Encode the parameters properly
        encoded_params = urlencode(params)

        # Create the full URL
        full_url = f"{api_url}?{encoded_params}"
        print("full_url:",full_url)

        try:
            response = requests.get(full_url)
            if response.status_code == 200:
                data = response.json()
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Failed to fetch data'}, status=response.status_code)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class OfficePhoneRequestEmail(APIView):
    def post(self, request, *args, **kwargs):
        # Get parameters from the JSON request body
        email = request.query_params.get('email')
        name = request.query_params.get('name')
        mobile_number = request.query_params.get('mobile_number')

        # Construct the email body with the provided message
        body = f"Dear {name},\n\n" \
               f"Account call back request booked by Customer.\n\n" \
               f"Kindly call on the following number and clear the call.\n\n" \
               f"Phone No: {mobile_number}\n\n" \
               f"Thanks & Regards,\n" \
               f"Sinewave Team."

        # Email configuration
        sender_email = "crm@sinewave.co.in"
        receiver_email = email
        subject = "Taxbase License Verification"

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject

        # Attach plain text content to the email
        message.attach(MIMEText(body, 'plain'))

        # Send the email
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login('crm@sinewave.co.in', 'fzjv eaaj kdcv svqr')
                text = message.as_string()
                server.sendmail(sender_email, receiver_email, text)
                return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            






from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class SendEmailAPIHTML2(APIView):
    def get(self, request, *args, **kwargs):
        # Get parameters from the URL query parameters 
        email = request.query_params.get('email')
        id = request.query_params.get('id')
        
        # Email content with formatting for the 'id' parameter
        email_content = f"""
       <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>My Taxbase App Information</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #444;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}

                .container {{
                    max-width: 600px;
                    margin: 20px auto;
                    background-color: #fff;
                    border-radius: 8px;
                    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
                    padding: 30px;
                }}

                h1 {{
                    text-align: left;
                    color: #333;
                }}

                p {{
                    margin-bottom: 15px;
                    text-align: left;
                }}

                ul {{
                    margin-bottom: 20px;
                    padding-left: 20px;
                }}

                li {{
                    margin-bottom: 5px;
                }}

                a {{
                    color: #007bff;
                    text-decoration: none;
                }}

                a:hover {{
                    text-decoration: underline;
                }}

                .signature {{
                    font-style: italic;
                    text-align: left;
                    color: #888;
                    margin-top: 30px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>My Taxbase App Information</h1>
                <p>Dear Sir/Madam,</p>
                <p>We are pleased to provide you with information about the My Taxbase App.</p>
                <p>To download the app for iOS or Android, please use the following links:</p>
                <ul>
                    <li><strong>Android:</strong> <a href="https://play.google.com/store/apps/details?id=com.sinewave.mytaxbase">Download from Google Play Store</a></li>
                    <li><strong>iOS:</strong> <a href="https://apps.apple.com/in/app/my-taxbase/id6451190735">Download from App Store</a></li>
                </ul>
                <p>After downloading and installing the app, you will be prompted to enter your Tax Professional ID. Please use the following details:</p>
                <p><strong>Tax Professional ID:</strong> {id}</p>
                <p>Once you've entered your mobile number and submitted, an OTP for mobile verification will be sent. Enter the OTP to create your login password for the My Taxbase App. You can then add a member by providing Name, Email ID, PAN, and ITD Password.</p>
                <p>After saving your information, you can access features such as the ITR Dashboard, Refund Status, e-Proceeding & Intimation, and check your Tax Calculation from the app's menu.</p>
                <p class="signature">Best Regards,
            </div>
        </body>
        </html>


        """
    
        # Email configuration
        sender_email = "crm@sinewave.co.in"
        receiver_email = email
        subject = "For Change Password On Sinewave Portel"
        
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject

        # Attach HTML content to the email
        message.attach(MIMEText(email_content, 'html'))

        # Send the email
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login('crm@sinewave.co.in', 'fzjv eaaj kdcv svqr')
                text = message.as_string()
                server.sendmail(sender_email, receiver_email, text)
                return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class CSCRegisterEmail(APIView):
     def post(self, request, *args, **kwargs):
        # Get parameters from the JSON request body
        email = request.data.get('email')
        name = request.data.get('name')
        mobile_number = request.data.get('mobile_number')

        # Check if any parameter is None
        if email is None or name is None or mobile_number is None:
            return Response({"error": "One or more parameters are missing"}, status=status.HTTP_400_BAD_REQUEST)

        # Construct the email body
        body = f"Subject: Confirmation of Individual DSC Registration for Customer: {name}\n\n" \
               f"Dear Rutuja,\n\n" \
               f"I hope this email finds you well.\n\n" \
               f"I am pleased to inform you that we have successfully registered {name} for an Individual Digital Signature Certificate (DSC). Below are the details of the registration:\n\n" \
               f"Customer's Name: {name}\n" \
               f"Mobile Number: {mobile_number}\n" \
               f"Email Address: {email}\n\n" \
               f"Thank you for your attention to this matter.\n" \
               f"Sinewave Team."

        # Email configuration
        sender_email = "crm@sinewave.co.in"
        receiver_email = "rutuja.s@sinewave.in"

        # Send the email
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login('crm@sinewave.co.in', 'fzjv eaaj kdcv svqr')
                server.sendmail(sender_email, receiver_email, body)
                return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import smtplib

class PaymentReminderEmail(APIView):
    def post(self, request, *args, **kwargs):
        # Get parameters from the JSON request body
        email = request.data.get('email')
        amount = request.data.get('amount')
        url = request.data.get('url')
        product = request.data.get('product')
        customer_name = request.data.get('customer_name')   
        customer_id = request.data.get('customer_id')
        customer_alias = request.data.get('customer_alias')

        # Construct the email body
        body = f"Subject: Product Payment \n\n" \
               f"Dear {customer_name},\n\n" \
               f"Kindly click on the link below to make a payment of Rs.{amount}/- to {product}.\n\n" \
               f"For your reference, this payment is being made against Customer ID {customer_id} ({customer_alias}).\n\n" \
               f"{url}\n\n" \
               f"Sinewave Team."





        # Email configuration
        sender_email = "crm@sinewave.co.in"
        receiver_email = email

        # Send the email
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login('crm@sinewave.co.in', 'fzjv eaaj kdcv svqr')
                server.sendmail(sender_email, receiver_email, body)
                return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class Paymentmailtosanjay(APIView):
    def post(self, request, *args, **kwargs):
        # Check if the request data is not None
        if not request.data:
            return Response({"error": "Request body is empty or not properly formatted."}, status=status.HTTP_400_BAD_REQUEST)

        # Get customer name from the JSON request body
        customer_name = request.data.get('customer_name')
        email = request.data.get('email')

        if not customer_name:
            return Response({"error": "Customer name is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Construct the email body
        body = f"Subject: Incorrect Contact Information\n\n" \
               f"Dear M/S Sanjay,\n\n" \
               f"The Email Id/Mobile number provided by you for {customer_name}, is incorrect. Kindly correct the same and retry."

        # Email configuration
        sender_email = "crm@sinewave.co.in"
        receiver_email = email  # Replace with actual receiver email

        # Send the email
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, 'fzjv eaaj kdcv svqr')
                server.sendmail(sender_email, receiver_email, body)
                return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        







class SendEmailTeamControlCredentialsAPI(APIView):
    def post(self, request, *args, **kwargs):
        # Get parameters from the URL query parameters
        employee_name = request.query_params.get('employee_name')
        email = request.query_params.get('email')
        company_name = request.query_params.get('company_name')
        url = request.query_params.get('url')
        login_id = request.query_params.get('login_id')
        password = request.query_params.get('password')
        company_code = request.query_params.get('company_code')

        # Email configuration
        sender_email = "crm@sinewave.co.in"
        receiver_email = email
        subject = "About Team Control Credentials"

        # Construct the email body
        body = (
            f"Dear {employee_name},\n\n"
            f"Your Credentials for {company_name} Team Control are as following:\n"
            f"URL: {url}\n"
            f"Company Code: {company_code}\n"
            f"Username: {login_id}\n"
            f"Password: {password}\n\n"
            f"Thanking you,\nYour truly,\nAdministrator,\n{company_name}"
        )

        # Gmail SMTP server and port
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        # Your Gmail account credentials
        username = "crm@sinewave.co.in"
        password = "fzjv eaaj kdcv svqr" 

        # Create the email message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        # Connect to the SMTP server and send the email
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(username, password)
                server.sendmail(sender_email, [receiver_email], message.as_string())

            return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class SendEmailAPIHTML3(APIView):
    def post(self, request, *args, **kwargs):
        # Get parameters from the URL query parameters
        name = request.query_params.get('name')
        email = request.query_params.get('email')
        Product = request.query_params.get('Product')
        Invoice_No = request.query_params.get('Invoice_No')
        Invoice_Date = request.query_params.get('Invoice_Date')
        Invoice_Amount = request.query_params.get('Invoice_Amount')
        details_url = request.query_params.get('details_url')  # Get URL parameter
        
        # New Email content with the AUC Fees acknowledgment template
        email_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Acknowledgment of AUC Fees</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    color: #333;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    width: 90%;
                    max-width: 600px;
                    margin: 0 auto;
                    background-color: #ffffff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    border: 3px solid #4CAF50;
                }}
                .header {{
                    background-color: #4CAF50;
                    color: white;
                    text-align: center;
                    padding: 15px 0;
                    border-radius: 8px 8px 0 0;
                }}
                .content {{
                    padding: 20px 0;
                }}
                .content p {{
                    margin: 10px 0;
                    line-height: 1.6;
                    color: #333;
                }}
                .content ol {{
                    margin: 10px 0;
                    padding-left: 20px;
                }}
                .content ol li {{
                    margin: 5px 0;
                }}
                .product-table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                }}
                .product-table th, .product-table td {{
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: left;
                }}
                .product-table th {{
                    background-color: #4CAF50;
                    color: white;
                }}
                .footer {{
                    background-color: #f1f1f1;
                    padding: 20px;
                    text-align: left;
                    border-radius: 0 0 8px 8px;
                    font-size: 14px;
                    color: #777;
                }}
                .footer-box {{
                    background-color: #4CAF50;
                    color: white;
                    padding: 15px;
                    border-radius: 8px;
                    text-align: center;
                }}
                .footer-box p {{
                    margin: 5px 0;
                }}
                .footer-box .contact-info {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    font-size: 14px;
                    flex-wrap: wrap;
                }}
                .footer-box .contact-info div {{
                    flex: 1;
                    text-align: center;
                    padding: 5px;
                }}
                
                /* Media Queries for Responsiveness */
                @media only screen and (max-width: 600px) {{
                    .container {{
                        width: 95%;
                        padding: 10px;
                    }}
                    .product-table th, .product-table td {{
                        padding: 5px;
                        font-size: 12px;
                    }}
                    .header {{
                        font-size: 18px;
                        padding: 10px;
                    }}
                    .content p {{
                        font-size: 14px;
                    }}
                    .footer-box .contact-info {{
                        flex-direction: column;
                        text-align: center;
                    }}
                    .footer-box .contact-info div {{
                        margin-bottom: 10px;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2>Acknowledgment of AUC Fees Received</h2>
                </div>
                <div class="content">
                    <p>Dear {name},</p>

                    <p>Thank you for being a part of the Sinewave family by trusting us and becoming a valued customer.</p>
                    <p>We hope things are going great. In case you need any help, you are requested to:</p>
                    <ol>
                        <li>Call our Customer Support at <strong>020-49091000</strong> and raise a ticket for your issue.</li>
                        <li>Email us at: <a href="mailto:crm@sinewave.co.in" style="color: #4CAF50;">crm@sinewave.co.in</a></li>
                    </ol>
                    <p>We assure you that we will resolve any issues as soon as possible.</p>

                    <p>We acknowledge receipt of the AUC fees. Please find the attached tax invoice for your records. <a href="{details_url}" style="color: #4CAF50;">Click Here</a>.</p>

                    <table class="product-table">
                        <tr>
                            <th>Sr. No</th>
                            <th>Product</th>
                            <th>Invoice No</th>
                            <th>Invoice Date</th>
                            <th>Invoice Amount</th>
                        </tr>
                        <tr>
                            <td>1</td>
                            <td>{Product}</td>
                            <td>{Invoice_No}</td>
                            <td>{Invoice_Date}</td>
                            <td>{Invoice_Amount}</td>
                        </tr>
                    </table>

                    <p>Should you have any questions or require further information, feel free to contact us.</p>

                    <p>Thank you for your prompt payment.</p>

                    <p>In case of any queries, kindly revert back to this email.</p>

                    <br>
                </div>
                <div class="footer">
                    <div class="footer-box">
                        <div class="contact-info">
                            <div><strong>Email</strong><br>crm@sinewave.co.in</div>
                            <div><strong>Contact</strong><br>020- 49091000</div>
                            <div><strong>Visit Us At</strong><br>www.sinewave.co.in</div>
                        </div>
                        <p>Address: T-22, Third Floor, Super Mall, Salunke Vihar Road, Wanowrie, Pune - 411 040.</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """

        # Email configuration
        sender_email = "accounts@sinewave.co.in"
        receiver_email = email
        subject = "Acknowledgment of AUC Fees Received"
        
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject

        # Attach HTML content to the email
        message.attach(MIMEText(email_content, 'html'))

        # Send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login('accounts@sinewave.co.in', 'nuag qypq xuwi rqev')  # Make sure to replace this with your actual password
            text = message.as_string()
            server.sendmail(sender_email, receiver_email, text)
            return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)


class SendLicenseEmailAPI(APIView):
    def post(self, request, *args, **kwargs):
        # Get parameters from the URL query parameters
        name = request.query_params.get('name')
        internal_customer_id = request.query_params.get('internal_customer_id')
        product_name = request.query_params.get('product_name')
        user_code = request.query_params.get('user_code')
        key_code = request.query_params.get('key_code')
        password = request.query_params.get('password')
        email = request.query_params.get('email')

        # Email configuration
        sender_email = "crm@sinewave.co.in"
        receiver_email = email
        subject = "License Information for In-house Testing"

        # Construct the email body
        body = (
            f"Dear {name},\n\n"
            f"Here are your license details for testing purposes:\n\n"
            f"Internal Customer ID: {internal_customer_id}\n"
            f"Product Name: {product_name}\n"
            f"User Code: {user_code}\n"
            f"Key Code: {key_code}\n"
            f"Password: {password}\n\n"
            f"This license is for in-house employees for testing purposes.\n\n"
            f"Thank you,\nAdministrator"
        )

        # Gmail SMTP server and port
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        # Your Gmail account credentials
        username = "crm@sinewave.co.in"
        email_password = "fzjv eaaj kdcv svqr"  # Ensure to secure your password

        # Create the email message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        # Connect to the SMTP server and send the email
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(username, email_password)
                server.sendmail(sender_email, [receiver_email], message.as_string())

            return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class webinar_2(APIView):
    def get(self, request, *args, **kwargs):
        # Get parameters from URL query params instead of JSON body
        customer_name = request.query_params.get('customer_name')
        print("customer_name:", customer_name)
        email = request.query_params.get('email')
        webinar_subject = request.query_params.get('webinar_subject', 'Our Webinar')  # Default value if not provided
        c_value = request.query_params.get('c')  # Retrieve C value
        w_value = request.query_params.get('w')  # Retrieve W value

        # Validate the required parameters
        if not customer_name or not email:
            return Response({"error": "Customer name and email are required."}, status=status.HTTP_400_BAD_REQUEST)
        if not c_value or not w_value:
            return Response({"error": "C and W values are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Construct the feedback link using C and W values
        feedback_link = f'https://crm.sinewave.co.in/Existinguser/Webinar-feedback.aspx?C={c_value}&W={w_value}'

        # Construct the new email body with HTML content
        body = f"""
        <html>
            <body>
                <p>Dear {customer_name},</p>
                <p>Thank you for attending our webinar: {webinar_subject}.</p>
                <p>We always strive to ensure you understand our application and have all your doubts clarified.<br>
                We also improve our software based on your valuable inputs.</p>
                <p>So please fill out the feedback form with your rating and training expectations.<br>
                <a href="{feedback_link}">Click here to provide feedback</a></p>
                <p>Thanks & Regards,<br>
                Sinewave Team.</p>
            </body>
        </html>
        """

        # Email configuration
        sender_email = "crm@sinewave.co.in"
        receiver_email = email

        # Send the email with HTML content
        try:
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart

            msg = MIMEMultipart("alternative")
            msg["Subject"] = "Thank You for Attending Our Webinar"
            msg["From"] = sender_email
            msg["To"] = receiver_email

            # Attach the HTML body to the email
            msg.attach(MIMEText(body, "html"))

            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, 'fzjv eaaj kdcv svqr')  # Be sure to use a valid app password
                server.sendmail(sender_email, receiver_email, msg.as_string())
                return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)






class Helpline_Feedback(APIView):
    def get(self, request, *args, **kwargs):
        # Get customer name and email from query parameters only
        customer_name = request.query_params.get('customer_name')
        email = request.query_params.get('email')
        feedback_link = request.query_params.get('feedback_link')

        if not customer_name or not email:
            return Response({"error": "Customer name and email are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Construct the new email body
        body = f"""Subject: We Value Your Feedback\n
                Dear {customer_name},\n
                Thank you for contacting us. We hope your query has been resolved successfully and that you are happy with the solution provided.\n
                Your valuable feedback helps us improve our services and software.\n
                Kindly click on the link below to submit your valuable suggestions:\n
                {feedback_link}\n
                Thanks & Regards,\n
                Sinewave Team.
                """

        # Email configuration
        sender_email = "crm@sinewave.co.in"
        receiver_email = email

        # Send the email
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, 'fzjv eaaj kdcv svqr')  # Be sure to use a valid app password
                server.sendmail(sender_email, receiver_email, body)
                return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class Helpline_Feedback_New(APIView):
    def get(self, request, *args, **kwargs):
        # Get customer name, email, and feedback link from query parameters
        email = request.query_params.get('email')
        feedback_link = request.query_params.get('feedback_link')

        if not email or not feedback_link:
            return Response({"error": "email, and feedback link are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Construct the HTML email body with user-defined feedback link
        body = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Feedback Email</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
            color: #333;
        }}
        .email-container {{
            max-width: 600px;
            margin: 20px auto;
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }}
        .email-header {{
            background-color: #007bff;
            color: #ffffff;
            padding: 20px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
        }}
        .email-body {{
            padding: 20px;
            line-height: 1.6;
        }}
        .email-footer {{
            background-color: #f1f1f1;
            text-align: center;
            padding: 15px;
            font-size: 14px;
            color: #666;
        }}
        .feedback-button {{
            display: inline-block;
            margin-top: 20px;
            padding: 10px 20px;
            background-color: #007bff;
            color: #ffffff;
            text-decoration: none;
            border-radius: 5px;
            font-size: 16px;
        }}
        .feedback-button:hover {{
            background-color: #0056b3;
        }}
        @media screen and (max-width: 600px) {{
            .email-container {{
                width: 90%;
            }}
            .email-header {{
                font-size: 20px;
            }}
            .feedback-button {{
                font-size: 14px;
                padding: 8px 16px;
            }}
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="email-header">
            Dear Customer,
        </div>
        <div class="email-body">
            <p>Thank you for contacting us. We hope your query has been resolved successfully and to your utmost satisfaction.</p>
            <p>We would appreciate your valuable feedback to help us serve you better. Please click the link below to provide your feedback:</p>
            <a href="{feedback_link}" class="feedback-button">Give Feedback</a>
            <p>Thanks,<br>The Sinewave Team</p>
        </div>
        <div class="email-footer">
            &copy; 2024 Sinewave Team. All Rights Reserved.
        </div>
    </div>
</body>
</html>
"""

        # Email configuration
        sender_email = "crm@sinewave.co.in"
        receiver_email = email
        subject = "We Value Your Feedback"
        message = f"Subject: {subject}\nContent-Type: text/html\n\n{body}"

        # Send the email
        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, 'fzjv eaaj kdcv svqr')  # Use a valid app password
                server.sendmail(sender_email, receiver_email, message)
                return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


