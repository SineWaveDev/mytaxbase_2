from django.db import models


class WebinarRegistration(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    webinar_subject = models.CharField(max_length=255)
    webinar_date = models.DateField()
    webinar_time = models.TimeField()
    webinar_url = models.URLField()

    def __str__(self):
        return self.name
