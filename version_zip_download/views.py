import requests
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from io import BytesIO

class DownloadZipView(APIView):
    def get(self, request):
        url = request.query_params.get('url')
        if not url:
            return Response({"error": "URL is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            response = requests.get(url)
            response.raise_for_status()

            zip_file = BytesIO(response.content)
            response = HttpResponse(zip_file.getvalue(), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename=downloaded_file.zip'
            return response
        except requests.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
