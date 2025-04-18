"""
Django settings for tax_calculation_api project.

Generated by 'django-admin startproject' using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-b0k-2l=0$e7pduf5$&)sqfdi*+enq&qm0wo7@3(t$1+*y^_t-='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    # Add other allowed origins if needed
]

CORS_ALLOW_CREDENTIALS = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'drf_yasg',
    'tax_calculator',
    'Tax_Calculation_Mobile',
    'emailotp',
    'technical_api',
    'Support_calling_chart',
    'portfolio_chart',
    'pdftoexcel',
    'schema_json_compare',
    'Portfolio_Return',
    'portfolio_return_chart',
    'json_creation_api',
    'Digest_code',
    'portfolio_optimization',
    'Dividend_Data',
    'callback_whatsapp_message',
    'Combined_API_For_ITR1',
    'version_zip_download',
    'sinewave_APP_API',
    'sinewave_app_callback_register',
    'sinewave_update_profile_api',
    'sinewave_app_webinar_registration_api',
    'sinewave_app_product_list_api',
    'sinewave_app_get_profile_details',
    'AIS_PDF_Read',
    'pan_verification_api',
    'TDS_Validate_Challan_API',
    'Customer_Membership',
    'MIS_Rights_API',
    'request_type',
    'corsheaders',
    'angel_one',
    'groww',
    'icici_direct',
    'Zerodha_Kite',
    'Taxbase_Login_API',
    'user_status_Teams_calling_system',
    'mos_ratio_api',
    'internal_Testing_API',
    'MIS_OTP_Verify',
    'Filed_Returns_Logs',
    'CRM_Software_data_API',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'tax_calculation_api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'tax_calculation_api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}




# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATIC_URL = '/static/'
SMS_AUTH_KEY = '392201AlyhiZV47EU640b26edP1'
SMS_TEMPLATE_ID = '641e8b0fd6fc050b00051942'
SMS_TEMPLATE_ID_2 = '641e8b0fd6fc050b00051942'
SMS_SENDER_ID = 'SINEWV'
# Default primary key field t


SWAGGER_SETTINGS = {
    'DEFAULT_INFO': 'tax_calculator.swagger_info.info',
    # Other Swagger settings...
}
