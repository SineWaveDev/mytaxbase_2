from rest_framework.decorators import api_view
from rest_framework.response import Response
# from knox.models import AuthToken
import pyotp
import base64


@api_view(['GET'])
def verify_otp_mis(request):
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
