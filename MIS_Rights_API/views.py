from django.http import JsonResponse
from django.views import View
from urllib.parse import unquote
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class ConditionEvaluatorView(View):
    def get(self, request):
        # Retrieve query parameters
        condition = request.GET.get('input')
        mdept = request.GET.get('mDept')
        mlevel = request.GET.get('mlevel')

        try:
            # Convert mlevel to integer
            mlevel = int(mlevel) if mlevel else None

            # Safely evaluate the condition
            # Using eval with limited context for safety
            safe_context = {'mlevel': mlevel, 'mdept': mdept}
            condition = unquote(condition)  # Decode the condition string
            result = eval(condition, {"__builtins__": None}, safe_context)

            return JsonResponse({"result": result})

        except Exception as e:
            return JsonResponse({"error": f"Error evaluating condition: {e}"}, status=400)
