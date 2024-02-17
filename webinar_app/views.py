from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


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
    def get(self, request, *args, **kwargs):
         # Get parameters from the JSON request body
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

