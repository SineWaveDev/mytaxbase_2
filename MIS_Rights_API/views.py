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

        # Validate input_condition presence
        if not input_condition:
            return Response({"error": "Invalid input: 'input' condition missing"}, status=status.HTTP_400_BAD_REQUEST)

        # Additional logic: Check if the mLevel or mDept match certain conditions
        def evaluate_condition():
            # Check if mlevel < 10 or if mDept matches any of the specified departments
            if mlevel < 10:
                return True  # True if mlevel is less than 10
            elif mDept in ['A/C', 'H/R', 'DSC', 'ASS', 'SAL', 'COL', 'CRM']:
                return True  # True if mDept is one of the listed departments
            return False

        # Check if the input_condition matches the logic of mLevel or mDept
        if evaluate_condition():
            return Response({"result": "true"}, status=status.HTTP_200_OK)

        # Replace '||' with 'or' and '&&' with 'and' for Python evaluation
        input_condition = input_condition.replace('||', 'or').replace('&&', 'and')
        
        # Replace variable placeholders with actual values
        input_condition = input_condition.replace('mlevel', str(mlevel))
        input_condition = input_condition.replace("mDept", f"'{mDept}'")

        try:
            # Safely evaluate the condition using eval()
            condition_met = eval(input_condition)
            if condition_met:
                return Response({"result": "true"}, status=status.HTTP_200_OK)
            else:
                return Response({"result": "false"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"Invalid input condition: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
