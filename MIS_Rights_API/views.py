from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import re

class CheckDeptLevelAPI(APIView):
    def post(self, request):
        # Extract query parameters from the URL
        input_condition = request.query_params.get('input', None)
        mDept = request.query_params.get('mDept', None)
        mlevel = request.query_params.get('mlevel', None)
        
        # Ensure mlevel is an integer for comparison
        try:
            mlevel = int(mlevel)
        except (ValueError, TypeError):
            return Response({"error": "mlevel must be a number"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Extract department values from input_condition dynamically using regex
        if input_condition:
            dept_pattern = re.compile(r"mDept\s*==\s*'([^']+)'")
            extracted_depts = dept_pattern.findall(input_condition)
        else:
            extracted_depts = []

        # Check if mDept, mlevel, and input_condition are valid
        if input_condition and mDept is not None and mlevel is not None:
            # Check conditions: if mlevel < 10 or mDept is in the extracted departments
            if mlevel < 10 or mDept in extracted_depts:
                return Response({"result": "true"}, status=status.HTTP_200_OK)
            else:
                return Response({"result": "false"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid input"}, status=status.HTTP_400_BAD_REQUEST)
