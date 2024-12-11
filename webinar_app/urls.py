from django.urls import path
from webinar_app.views import SendEmailAPI, SendEmailAPIHTML, SendEmailTeamControl, SendEmailTaxbaseLicenseVerification, ForgotPassword, FetchDataAPIView, OfficePhoneRequestEmail, SendEmailAPIHTML2, CSCRegisterEmail, PaymentReminderEmail, Paymentmailtosanjay, SendEmailTeamControlCredentialsAPI, SendEmailAPIHTML3 , SendLicenseEmailAPI, webinar_2, Helpline_Feedback, Helpline_Feedback_New


urlpatterns = [
    path('send-email/', SendEmailAPI.as_view(), name='send_email'),
    path('send-email-HTML/', SendEmailAPIHTML.as_view(), name='send_email-HTML'),
    path('send-email-teamcontrol/', SendEmailTeamControl.as_view(), name='send-email-teamcontrol'),
    path('send-email-license/', SendEmailTaxbaseLicenseVerification.as_view(), name='send-email-license'),
    path('forgot-password/', ForgotPassword.as_view(), name='forgot-password'),
    path('fetch-data/', FetchDataAPIView.as_view(), name='fetch-data'),
    path('office-phone-request/', OfficePhoneRequestEmail.as_view(), name='office-phone-request'),
    path('send-email-HTML_2/', SendEmailAPIHTML2.as_view(), name='send-email-HTML_2'),
    path('DSC/', CSCRegisterEmail.as_view(), name='DSC'),
    path('PaymentReminderEmail/', PaymentReminderEmail.as_view(), name='PaymentReminderEmail'),
    path('Paymentmailtosanjay/', Paymentmailtosanjay.as_view(), name='Paymentmailtosanjay'),
    path('team-control-credentials/', SendEmailTeamControlCredentialsAPI.as_view(), name='team-control-credentials'),
    path('send-email-HTML_3/', SendEmailAPIHTML3.as_view(), name='send-email-HTML_3'),
    path('SendLicenseEmailAPI/', SendLicenseEmailAPI.as_view(), name='SendLicenseEmailAPI'),
    path('webinar_2/', webinar_2.as_view(), name='webinar_2'),
    path('Helpline_Feedback/', Helpline_Feedback.as_view(), name='Helpline_Feedback'),
    path('Helpline_Feedback_New/', Helpline_Feedback_New.as_view(), name='Helpline_Feedback_New'),
]