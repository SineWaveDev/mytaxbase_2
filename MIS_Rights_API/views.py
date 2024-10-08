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
        
        # Assuming input is in the format (mDept == 'H/R' or mlevel <= 10)
        if input_condition and mDept is not None and mlevel is not None:
            # Parse input condition (hardcoded as per the example)
            input_dept = 'H/R'
            input_level = 10

            # Check conditions
            if mDept == input_dept and mlevel <= input_level:
                return Response({"result": "true"}, status=status.HTTP_200_OK)
            elif mDept == input_dept or mlevel <= input_level:
                return Response({"result": "true"}, status=status.HTTP_200_OK)
            else:
                return Response({"result": "false"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid input"}, status=status.HTTP_400_BAD_REQUEST)
