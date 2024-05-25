from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import hmac
import base64

JSON_PATH = r"C:\Users\Sinewave#2022\Downloads"
JSON_FILE_NAME = "ITR 3_2024-2025_ITR3 sample 1.json"
JSON_FILE_PATH = os.path.join(JSON_PATH, JSON_FILE_NAME)
ALGORITHM = "sha256"
VALUES = {"SW20000297": ["HeRWGR9kDHyLAOZT", "1790"]}

@csrf_exempt
def generate_digest(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')

        dig_index = data.index("Digest")

        if (
            data[dig_index + 6] != '"'
            or data[dig_index + 7] != ":"
            or data[dig_index + 8] != '"'
        ):
            return JsonResponse({"error": "Invalid Digest key detected"})

        swc_index = data.index("SWCreatedBy")
        sw_created_by = data[swc_index + 14 : swc_index + 24]

        if not sw_created_by.startswith("SW") or len(sw_created_by) != 10:
            return JsonResponse({"error": "Invalid SWCreatedBy"})

        digest_bef = data[: dig_index + 9]
        dig_value_colon_end_index = data.index('"', dig_index + 9)
        digest_aft = data[dig_value_colon_end_index :]

        hash_to_gen_for = digest_bef + "-" + digest_aft

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
