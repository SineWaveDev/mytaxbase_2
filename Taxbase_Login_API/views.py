import json
import asyncio
import aiohttp
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View

# Make sure to update Django settings to support async views
# Ensure the ASGI server (like Daphne or Uvicorn) is being used instead of WSGI server

@csrf_exempt
async def run_multiple_apis(request):
    """
    This Django view receives input data via POST (JSON format) from Postman,
    uses the input to dynamically call multiple APIs concurrently, and returns the results.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Only POST method is allowed"}, status=405)

    try:
        # Parse JSON input from Postman
        input_data = json.loads(request.body)
    except Exception as e:
        return JsonResponse({"error": "Invalid JSON format", "details": str(e)}, status=400)

    # Define the API details with updated names
    api_requests = [
        {
            "name": "Version Number",
            "url": "http://SwAPI.sinewave.co.in/api/Common/GetCurrentVersion",
            "method": "POST",
            "input_key": "version_number_payload",  # Input key expected in input_data
        },
        {
            "name": "Get Setup Path",
            "url": "http://SwAPI.sinewave.co.in/api/Common/GetSetupDownloadPath",
            "method": "POST",
            "input_key": "setup_path_payload",  # Input key expected in input_data
        },
        {
            "name": "Version Number of ONS",
            "url": "http://SwAPI.sinewave.co.in/api/Common/GetCurrentVersion",
            "method": "POST",
            "input_key": "ons_version_payload",  # Input key expected in input_data
        },
        {
            "name": "Outstanding",
            "url": "http://SwAPI.sinewave.co.in/api/Common/GetOutStandingAmt",
            "method": "GET",
            "input_key": "outstanding_params",  # Input key expected in input_data
        },
        {
            "name": "Usage Info",
            "url": "http://SwAPI.sinewave.co.in/api/Common/CustomerUsageInfo",
            "method": "GET",
            "input_key": "usage_info_params",  # Input key expected in input_data
        },
        {
            "name": "Get Domain",
            "url": "https://taxapi.sinewave.co.in/API/TaxCalculator/GetDomainNames",
            "method": "POST",
            "input_key": "domain_payload",  # Input key expected in input_data
        },
        {
            "name": "DMS Folder",
            "url": "https://taxapi.sinewave.co.in/API/CRM/GetDMSFolderDetails",
            "method": "POST",
            "input_key": "dms_folder_payload",  # Input key expected in input_data
        },
        {
            "name": "Authentication",
            "url": "https://taxapi.sinewave.co.in/API/CRM/GetAuthentication",
            "method": "POST",
            "input_key": "authentication_payload",  # Input key expected in input_data
        },
    ]

    async def fetch(api):
        api_input = input_data.get(api["input_key"], {})
        async with aiohttp.ClientSession() as session:
            try:
                if api["method"] == "POST":
                    async with session.post(api["url"], json=api_input) as response:
                        return {
                            "API": api["name"],
                            "StatusCode": response.status,
                            "Response": await response.json() if response.status == 200 else await response.text()
                        }
                elif api["method"] == "GET":
                    async with session.get(api["url"], params=api_input) as response:
                        return {
                            "API": api["name"],
                            "StatusCode": response.status,
                            "Response": await response.json() if response.status == 200 else await response.text()
                        }
                else:
                    return {
                        "API": api["name"],
                        "Error": f"Unsupported HTTP method: {api['method']}"
                    }
            except Exception as e:
                return {
                    "API": api["name"],
                    "Error": str(e)
                }

    # Run all requests concurrently
    responses = await asyncio.gather(*[fetch(api) for api in api_requests])

    return JsonResponse({"responses": responses}, status=200)
