# Generated by Django 5.0.1 on 2024-11-16 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UploadedFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf_file', models.FileField(upload_to='uploads/')),
                ('excel_file', models.FileField(upload_to='uploads/')),
            ],
        ),
    ]
