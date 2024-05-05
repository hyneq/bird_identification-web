from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.db import models
from django.db.models import Count, Min, Max
from django.db.models.functions import Trunc

from django.utils.translation import gettext_noop

ALLOWED_GROUP_UNITS = [
        'year',
        'month',
        'day',
        'hour',
        'minute',
        'second'
    ]

DEFAULT_GROUP_UNIT = 'day'

DEFAULT_DURATION = relativedelta(weeks=1)

class LoggedObject(models.Model):
    class_name = models.CharField(max_length=100, verbose_name=gettext_noop("Class name"), null=True)
    start_time = models.DateTimeField(verbose_name=gettext_noop("Start time"))
    end_time = models.DateTimeField(verbose_name=gettext_noop("End time"))

    @classmethod
    def query(cls, window_start=None, window_end=None, window_duration=None, group_unit=DEFAULT_GROUP_UNIT):
        # Determine time window
        if window_duration:
            if window_start and window_end:
                pass
            elif window_start:
                window_end = window_start + window_duration
            elif window_end:
                window_start = window_end - window_duration
            else:
                window_start = datetime.now() - window_duration
        
        # Truncate start_time to the specified time unit
        if not group_unit in ALLOWED_GROUP_UNITS:
            raise ValueError("Invalid time unit")
        trunc_func = Trunc('start_time', group_unit)
        
        # Filter data within the specified time window
        queryset = cls.objects.all()
        if window_start:
            queryset = queryset.filter(start_time__gte=window_start)
        if window_end:
            queryset = queryset.filter(start_time__lt=window_end)
        
        # Group by truncated start_time and class_name, and annotate with count
        queryset = queryset.values(
            'start_time', 'class_name'
        ).annotate(
            time=trunc_func
        ).values(
            'time', 'class_name'
        ).annotate(
            count=Count('id')
        ).order_by('time', 'class_name')
        
        return queryset
    
    @classmethod
    def get_time_range(cls):

        queryset = cls.objects.all().values('start_time')

        vals = queryset.aggregate(
            min_time=Min('start_time'),
            max_time=Max('start_time')
        )

        return vals['min_time'], vals['max_time']
