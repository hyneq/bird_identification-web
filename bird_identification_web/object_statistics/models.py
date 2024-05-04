from django.db import models
from django.utils.translation import gettext_noop

class LoggedObject(models.Model):
    class_name = models.CharField(max_length=100, verbose_name=gettext_noop("Class name"), null=True)
    start_time = models.DateTimeField(verbose_name=gettext_noop("Start time"))
    end_time = models.DateTimeField(verbose_name=gettext_noop("End time"))
