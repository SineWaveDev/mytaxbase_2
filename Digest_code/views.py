from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import hmac
import base64
import json

ALGORITHM = "sha256"
VALUES = {"SW20000297": ["HeRWGR9kDHyLAOZT", "1790"]}

@csrf_exempt
def generate_digest(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON payload"})

        itr = data.get("ITR", {})
        itr3 = itr.get("ITR3", {})
        creation_info = itr3.get("CreationInfo", {})
        
        digest = creation_info.get("Digest", None)
        sw_created_by = creation_info.get("SWCreatedBy", None)

        if digest is None or digest != "-":
            return JsonResponse({"error": "Invalid Digest key detected"})
        
        if not sw_created_by or not sw_created_by.startswith("SW") or len(sw_created_by) != 10:
            return JsonResponse({"error": "Invalid SWCreatedBy"})

        # Create the data string for hashing
        data_str = json.dumps(data, separators=(',', ':'))
        hash_to_gen_for = data_str.replace(f'"Digest":"{digest}"', '"Digest":""')

        key_itrtns = get_key_iteration(sw_created_by)
        if not key_itrtns:
            return JsonResponse({"error": f"No key and iteration found for SWCreatedBy: {sw_created_by}"})

        key = key_itrtns[0]
        iteration = int(key_itrtns[1])

        generated_digest = generate_hash_for_string(hash_to_gen_for, iteration, key)
        return JsonResponse({"Digest": generated_digest})
    else:
        return JsonResponse({"error": "Only POST requests are allowed"})

def get_key_iteration(sw_created_by):
    return VALUES.get(sw_created_by, [])

def generate_hash_for_string(content, iteration, key):
    hmac_instance = hmac.new(key.encode("utf-8"), content.encode("utf-8"), digestmod=ALGORITHM)

    digest_value = hmac_instance.digest()

    for _ in range(iteration):
        hmac_instance = hmac.new(key.encode("utf-8"), digestmod=ALGORITHM)
        hmac_instance.update(digest_value)
        digest_value = hmac_instance.digest()

    generated_hash = base64.b64encode(digest_value).decode("utf-8")

    return generated_hash
