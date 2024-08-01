import fitz  # PyMuPDF
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class PDFToJsonView(APIView):
    def post(self, request):
        folder_path = request.data.get('folder_path')

        if not folder_path or not os.path.exists(folder_path):
            return Response({"error": "Invalid folder path"}, status=status.HTTP_400_BAD_REQUEST)
        
        pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
        if not pdf_files:
            return Response({"error": "No PDF files found in the specified folder"}, status=status.HTTP_404_NOT_FOUND)

        # Assuming we are processing the first PDF found in the folder
        pdf_path = os.path.join(folder_path, pdf_files[0])
        
        try:
            pdf_document = fitz.open(pdf_path)
            pdf_text = []

            for page_num in range(pdf_document.page_count):
                page = pdf_document.load_page(page_num)
                pdf_text.append(page.get_text("text"))

            json_output = {"pages": pdf_text}
            return Response(json_output, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
