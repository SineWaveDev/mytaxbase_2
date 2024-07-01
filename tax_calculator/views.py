import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from knox.models import AuthToken
from .services import itd_login, send_sms
import pyotp
import base64
from tax_calculation_api.settings import SMS_TEMPLATE_ID
import requests


@api_view(['GET'])
def get_otp(request):
    data = request.query_params.dict()
    
    # Correcting the key access for 'mobile'
    mobile = data.get('mobile')
    if not mobile:
        return Response({"status": False, "message": "Mobile number is required."}, status=400)
    
    key = base64.b32encode(mobile.encode())
    otp = pyotp.TOTP(key, digits=6, interval=180)
    otp_str = otp.now()
    
    if data.get('template_id'):
        template_id = data['template_id']
        sms_data = {"otp": otp_str}
    else:
        template_id = SMS_TEMPLATE_ID
        sms_data = {"otp": otp_str, "appname": "MIS"}

    print(otp_str)
    send_sms("91" + mobile, sms_data, template_id)
    return Response({
        "status": True,
        "message": "An SMS was sent to your registered mobile number. Please enter the one-time password it contains."
    })


@api_view(['GET'])
def verify_otp(request):
    data = request.query_params.dict()
    mobile = data['mobile']
    otp_str = data['otp']
    key = base64.b32encode(mobile.encode())
    otp = pyotp.TOTP(key, digits=6, interval=180)
    if otp.verify(otp_str):
        set_pass_key = base64.b32encode((mobile + otp_str).encode())
        set_pass_token = pyotp.TOTP(set_pass_key, digits=6, interval=180).now()
        return Response({"status": True, "message": "Verification successful", "data": {"pass_token": set_pass_token}})
    else:
        return Response({"status": False,
                         "message": "Incorrect OTP. This might be expired please generate a new one and try again"})
