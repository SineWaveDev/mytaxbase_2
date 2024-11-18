from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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

        # Function to evaluate the specific conditions as per your requirements
        def evaluate_condition():
            # Condition 1: If mlevel < 10, it's true regardless of mDept, or if mDept is 'A/C', it's true regardless of mlevel
            if mlevel < 10 or mDept == 'A/C':
                return True
            # Condition 2: If mDept is 'H/R' and mlevel < 25, it's true
            if mDept == 'H/R' and mlevel < 25:
                return True
            return False

        # Check if any of the specific conditions match
        if evaluate_condition():
            return Response({"result": "true"}, status=status.HTTP_200_OK)

        # Replace '||' with 'or' and '&&' with 'and' for Python evaluation
        input_condition = input_condition.replace('||', 'or').replace('&&', 'and')
        
        # Handle inconsistent capitalization
        input_condition = input_condition.replace('mdept', 'mDept')
        input_condition = input_condition.replace('mLevel', 'mlevel')

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
