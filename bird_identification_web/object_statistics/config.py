# This module is a static config for object_statistics statistics view

from django.utils.translation import gettext_noop, gettext_lazy as _
from datetime import datetime

# Set default values
default_timespan = "week"
default_data_view = "temperature"

# Timespans define the time range used in charts and how data should be grouped
timespans = {
    'day': {
        'verbose_name': _("Day"),
        'delta': {'days': 1}, # To be passed to relativedelta
        'group_by': 'hour',
        'input_type': 'date',
        'input_format': '%Y-%m-%d',
        'time_axis_format': 't',
        'title_format': "DATE_FORMAT"
    },
    'week': {
        'verbose_name': _("Week"),
        'delta': {'weeks': 1},
        'group_by': 'day',
        'child_timespan': 'day',
        'input_type': 'week',
        'input_format': '%Y-W%W',
        'input_decoder': lambda d: datetime.strptime(d + '-1', '%Y-W%W-%w'), # Week number is not enough to generate a date, see https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
        # Translators: Time axis format for the 'week' timespan
        'time_axis_format': gettext_noop('cccc, D'),
        # Translators: Title time format for the 'week' timespan
        'title_format': gettext_noop('\W\e\e\k W, Y')
    },
    'month': {
        'verbose_name': _("Month"),
        'delta': {'months': 1},
        'group_by': 'day',
        'child_timespan': 'day',
        'input_type': 'month',
        'input_format': '%Y-%m',
        'time_axis_format': 'D',
        # Translators: Title time format for the 'month' timespan
        'title_format': gettext_noop('F Y')
    },
    'year': {
        'verbose_name': _("Year"),
        'delta': {'years': 1},
        'group_by': 'month',
        'child_timespan': 'month',
        'input_type': 'number',
        'input_format': '%Y',
        # Translators: Time axis format for the 'year' timespan
        'time_axis_format': gettext_noop('LLLL y'),
        # Translators: Title time format for the 'year' timespan
        'title_format': gettext_noop('Y')
    }
}
