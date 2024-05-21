from rest_framework import serializers
from .models import UploadedFiles

class UploadedFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFiles
        fields = ('pdf_file', 'excel_file')
