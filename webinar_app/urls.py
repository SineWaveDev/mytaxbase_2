from django.urls import path
from webinar_app.views import SendEmailAPI, SendEmailAPIHTML, SendEmailTeamControl, SendEmailTaxbaseLicenseVerification, ForgotPassword, FetchDataAPIView, OfficePhoneRequestEmail, SendEmailAPIHTML2

urlpatterns = [
    path('send-email/', SendEmailAPI.as_view(), name='send_email'),
    path('send-email-HTML/', SendEmailAPIHTML.as_view(), name='send_email-HTML'),
    path('send-email-teamcontrol/', SendEmailTeamControl.as_view(), name='send-email-teamcontrol'),
    path('send-email-license/', SendEmailTaxbaseLicenseVerification.as_view(), name='send-email-license'),
    path('forgot-password/', ForgotPassword.as_view(), name='forgot-password'),
    path('fetch-data/', FetchDataAPIView.as_view(), name='fetch-data'),
    path('office-phone-request/', OfficePhoneRequestEmail.as_view(), name='office-phone-request'),
    path('send-email-HTML_2/', SendEmailAPIHTML2.as_view(), name='send-email-HTML_2'),
]