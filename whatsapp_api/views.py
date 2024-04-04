from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
import json

@api_view(['POST'])
def send_whatsapp_message(request):
    to_number = request.data.get('to_number')
    if not to_number:
        return Response({'error': 'Please provide a valid "to_number" in the request data.'}, status=400)
    
    url = "https://apis.aisensy.com/project-apis/v1/project/64ddf2c80c3f690e81677779/messages"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "X-AiSensy-Project-API-Pwd": "8e60e08b21b55216a85d7"
    }
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to_number,
        "type": "template",
        "template": {
            "name": "training_massage_11",
            "language": {
                "code": "en_US"
            },
            "components": [
                {
                    "type": "CAROUSEL",
                    "cards": [
                        {
                            "card_index": 0,
                            "components": [
                                {
                                    "type": "HEADER",
                                    "parameters": [
                                        {
                                            "type": "IMAGE",
                                            "image": {
                                                "link": "https://sinewavedb.s3.ap-south-1.amazonaws.com/Training.png"
                                            }
                                        }
                                    ]
                                },
                                {
                                    "type": "BUTTON",
                                    "sub_type": "URL",
                                    "index": "0",
                                    "parameters": [
                                        {
                                            "type": "PAYLOAD",
                                            "payload": "https://crm.sinewave.co.in/existingUser/default.aspx?utm_source=Sinewave+Active+Customers+21.01.2022&utm_campaign=33ce526b36-EMAIL_CAMPAIGN_2023_08_COPY_01&utm_medium=email&utm_term=0_-5a5bcb33ec-%5BLIST_EMAIL_ID%5D"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    return Response(response.json())
