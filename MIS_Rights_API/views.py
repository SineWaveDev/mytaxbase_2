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

        # Evaluate conditions using extracted data
        def evaluate_expression(expression):
            """
            Evaluates a logical expression with mlevel and mDept values.
            """
            # Replace variable placeholders with their actual values
            expression = expression.replace('mLevel', str(mlevel))
            expression = expression.replace("mDept", f"'{mDept}'")

            # Use regex to replace equality checks for string matches to proper Python conditions
            expression = re.sub(r"strDepttype\s*==\s*\"([^\"]+)\"", lambda match: f"'{mDept}' == '{match.group(1)}'", expression)

            try:
                # Evaluate the expression safely (basic check)
                result = eval(expression)
                return result
            except Exception as e:
                return False

        # Split and handle complex conditions with '||' and '&&'
        conditions = re.split(r'\|\||&&', input_condition)
        condition_met = False

        # Handle logical operations based on condition structure
        or_conditions = input_condition.split('||')
        for or_condition in or_conditions:
            and_conditions = or_condition.split('&&')
            if all(evaluate_expression(and_cond.strip()) for and_cond in and_conditions):
                condition_met = True
                break

        # Return the result based on condition evaluation
        if condition_met:
            return Response({"result": "true"}, status=status.HTTP_200_OK)
        else:
            return Response({"result": "false"}, status=status.HTTP_200_OK)



# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# import re

# class CheckDeptLevelAPI(APIView):
#     def post(self, request):
#         # Extract JSON data from the request body
#         input_condition = request.data.get('input', None)
#         mDept = request.data.get('mDept', None)
#         mlevel = request.data.get('mlevel', None)

#         # Ensure mlevel is an integer for comparison
#         if isinstance(mlevel, int):
#             # mlevel is already an integer
#             pass
#         elif isinstance(mlevel, str) and mlevel.isdigit():
#             # Convert valid string representations of numbers
#             mlevel = int(mlevel)
#         else:
#             return Response({"error": "mlevel must be a number"}, status=status.HTTP_400_BAD_REQUEST)

#         # Extract department conditions and mlevel conditions using regex
#         if input_condition:
#             # Extract mDept conditions
#             dept_pattern = re.compile(r"strDepttype\s*==\s*\"([^\"]+)\"")
#             extracted_depts = dept_pattern.findall(input_condition)

#             # Extract mlevel conditions
#             mlevel_pattern = re.compile(r"intlevel\s*(<=|<|>|>=|==)\s*(\d+)")
#             extracted_levels = [(match[0], int(match[1])) for match in mlevel_pattern.findall(input_condition)]
#         else:
#             extracted_depts = []
#             extracted_levels = []

#         # Check if mDept, mlevel, and input_condition are valid
#         if input_condition and mDept is not None and mlevel is not None:
#             # Evaluate conditions based on the extracted rules
#             condition_met = False

#             # Check mlevel conditions
#             for operator, value in extracted_levels:
#                 if operator == "<" and mlevel < value:
#                     condition_met = True
#                 elif operator == "<=" and mlevel <= value:
#                     condition_met = True
#                 elif operator == ">" and mlevel > value:
#                     condition_met = True
#                 elif operator == ">=" and mlevel >= value:
#                     condition_met = True
#                 elif operator == "==" and mlevel == value:
#                     condition_met = True

#             # Check mDept conditions
#             if mDept in extracted_depts:
#                 condition_met = True

#             # Final evaluation of all conditions
#             if condition_met:
#                 return Response({"result": "true"}, status=status.HTTP_200_OK)
#             else:
#                 return Response({"result": "false"}, status=status.HTTP_200_OK)
#         else:
#             return Response({"error": "Invalid input"}, status=status.HTTP_400_BAD_REQUEST)
