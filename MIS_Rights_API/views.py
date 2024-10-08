from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class CheckDeptLevelAPI(APIView):
    def post(self, request):
        # Extract input parameters from the request
        input_condition = request.data.get('input', None)
        mDept = request.data.get('mDept', None)
        mlevel = request.data.get('mlevel', None)
        
        # Assuming input is in the format (mDept == 'H/R' or mlevel <= 10)
        if input_condition and mDept is not None and mlevel is not None:
            # Parse input
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

