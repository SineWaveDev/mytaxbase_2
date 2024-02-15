from django.urls import path
from webinar_app.views import SendEmailAPI, SendEmailAPIHTML, SendEmailTeamControl, SendEmailTaxbaseLicenseVerification

urlpatterns = [
    path('send-email/', SendEmailAPI.as_view(), name='send_email'),
    path('send-email-HTML/', SendEmailAPIHTML.as_view(), name='send_email-HTML'),
    path('send-email-teamcontrol/', SendEmailTeamControl.as_view(), name='send-email-teamcontrol'),
    path('send-email-license/', SendEmailTaxbaseLicenseVerification.as_view(), name='send-email-license'),
]
