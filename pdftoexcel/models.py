from django.db import models

class UploadedFiles(models.Model):
    pdf_file = models.FileField(upload_to='uploads/')
    excel_file = models.FileField(upload_to='uploads/')
