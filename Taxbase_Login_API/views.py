import json
import asyncio
import aiohttp
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View

@csrf_exempt
async def run_multiple_apis(request):
    """
    Django view to handle API calls with restructured input JSON.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method is allowed"}, status=405)

    try:
        # Parse JSON input from Postman
        input_data = json.loads(request.body)
    except Exception as e:
        return JsonResponse({"error": "Invalid JSON format", "details": str(e)}, status=400)

    # Define the API details
    api_requests = [
        {
            "name": "Version Number",
            "url": "http://SwAPI.sinewave.co.in/api/Common/GetCurrentVersion",
            "method": "POST",
            "payload": {"ProdcutName": input_data.get("ProdcutName")},
        },
        {
            "name": "Get Setup Path",
            "url": "http://SwAPI.sinewave.co.in/api/Common/GetSetupDownloadPath",
            "method": "POST",
            "payload": {"ProdcutName": input_data.get("ProdcutName")},
        },
        {
            "name": "Version Number of ONS",
            "url": "http://SwAPI.sinewave.co.in/api/Common/GetCurrentVersion",
            "method": "POST",
            "payload": {"ProdcutName": input_data.get("ProdcutName_ONS")},
        },
        {
            "name": "Outstanding",
            "url": "http://SwAPI.sinewave.co.in/api/Common/GetOutStandingAmt",
            "method": "GET",
            "payload": {
                "HDKey": input_data.get("HDKey"),
                "LicKey": input_data.get("LicKey"),
                "ProductId": input_data.get("ProductId"),
                "MacID": input_data.get("MacID"),
            },
        },
        {
            "name": "Usage Info",
            "url": "http://SwAPI.sinewave.co.in/api/Common/CustomerUsageInfo",
            "method": "GET",
            "payload": {
                "custId": input_data.get("custId"),
                "ProductId": input_data.get("ProductId"),
                "Version": input_data.get("Version"),
                "HardwareKey": input_data.get("HardwareKey"),
                "IPAddress": input_data.get("IPAddress"),
                "ProdLic": input_data.get("ProdLic"),
                "Backend": input_data.get("Backend"),
                "ViewData": input_data.get("ViewData"),
                "MacID": input_data.get("MacID"),
            },
        },
        {
            "name": "Get Domain",
            "url": "https://taxapi.sinewave.co.in/API/TaxCalculator/GetDomainNames",
            "method": "POST",
            "payload": {},
        },
        {
            "name": "DMS Folder",
            "url": "https://taxapi.sinewave.co.in/API/CRM/GetDMSFolderDetails",
            "method": "POST",
            "payload": {},
        },
        {
            "name": "Authentication",
            "url": "https://taxapi.sinewave.co.in/API/CRM/GetAuthentication",
            "method": "POST",
            "payload": {
                "Skey": input_data.get("HDKey"),
                "Lkey": input_data.get("LicKey"),
            },
        },
    ]

    async def fetch(api):
        async with aiohttp.ClientSession() as session:
            try:
                if api["method"] == "POST":
                    async with session.post(api["url"], json=api["payload"]) as response:
                        return {
                            "API": api["name"],
                            "StatusCode": response.status,
                            "Response": await response.json() if response.status == 200 else await response.text(),
                        }
                elif api["method"] == "GET":
                    async with session.get(api["url"], params=api["payload"]) as response:
                        return {
                            "API": api["name"],
                            "StatusCode": response.status,
                            "Response": await response.json() if response.status == 200 else await response.text(),
                        }
                else:
                    return {
                        "API": api["name"],
                        "Error": f"Unsupported HTTP method: {api['method']}",
                    }
            except Exception as e:
                return {
                    "API": api["name"],
                    "Error": str(e),
                }

    # Run all requests concurrently
    responses = await asyncio.gather(*[fetch(api) for api in api_requests])

    return JsonResponse({"responses": responses}, status=200)
