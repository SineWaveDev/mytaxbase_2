import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser

class SendCampaignAPIView(APIView):
    parser_classes = [JSONParser]

    def post(self, request):
        mobile_number = request.data.get('mobile_number')

        if not mobile_number:
            return Response({"error": "Mobile number is required"}, status=status.HTTP_400_BAD_REQUEST)

        payload = {
            "apiKey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjY0ZGRmMmM4MGMzZjY5MGU4MTY3Nzc3OSIsIm5hbWUiOiJTaW5ld2F2ZSBDb21wdXRlciBzZXJ2aWNlcyIsImFwcE5hbWUiOiJBaVNlbnN5IiwiY2xpZW50SWQiOiI2NGRkZjJjODBjM2Y2OTBlODE2Nzc3NzQiLCJhY3RpdmVQbGFuIjoiTk9ORSIsImlhdCI6MTY5MjI2NzIwOH0.r5cHWBFTMs_4F70F4z3bb6MGTmkfSN1oOOM5PSaOUT0",
            "campaignName": "DSCMassage",
            "destination": mobile_number,
            "userName": "Sagar",
            "media": {
                "url": "https://sinewavedb.s3.ap-south-1.amazonaws.com/WhatsAppImageDSC.jpeg",
                "filename": "png"
            }
        }

        response = requests.post("https://backend.api-wa.co/campaign/smartping/api", json=payload)

        if response.status_code == 200:
            return Response({"message": "Campaign sent successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Failed to send campaign"}, status=status.HTTP_400_BAD_REQUEST)
