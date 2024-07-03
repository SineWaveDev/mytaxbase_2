"""tax_calculation_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
# from django.urls import path

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]
from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('tax_calculator.urls')),
    path('api/', include('Tax_Calculation_Mobile.urls')),
    path('api/', include('webinar_app.urls')),
    path('api/', include('emailotp.urls')),
    path('api/', include('technical_api.urls')),
    # path('api/', include('renko_chart.urls')),
    path('api/', include('Support_calling_chart.urls')),
    path('api/', include('portfolio_chart.urls')),
    path('api/', include('tax_cal_backend_api.urls')),
    path('api/', include('whatsapp_api.urls')),
    path('api/', include('pdftoexcel.urls')),
    path('api/', include('schema_json_compare.urls')),
    path('api/', include('Portfolio_Return.urls')),
    path('api/', include('portfolio_return_chart.urls')),
    path('api/', include('json_creation_api.urls')),
    path('api/', include('Digest_code.urls')),
    path('api/', include('Dividend_Data.urls')),
    path('api/', include('portfolio_optimization.urls')),
    path('api/', include('callback_whatsapp_message.urls')),
    path('api/', include('Combined_API_For_ITR1.urls')),
    path('api/', include('Whatsapp_API_Error_Control.urls')),
    path('api/', include('version_zip_download.urls')),
    path('api/', include('sinewave_APP_API.urls')),
    path('api/', include('sinewave_app_callback_register.urls')),
]
