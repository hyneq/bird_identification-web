import json
from os import path
from copy import deepcopy
from datetime import datetime
from dateutil.relativedelta import relativedelta

from django.shortcuts import render
from django.utils.translation import get_language, to_locale, gettext as _

from .. import config
from ..models import LoggedObject

chart_config_base = {
    'label': None,
    'type': None,
    'data':{
        'datasets': []
    },
    'options': {
        'responsive': True,
        'maintainAspectRatio': False,
        'scales': {
            'x': {
                'type': 'time',
                'time': {}, # To be filled from the timespan config
                'adapters': {
                    'date': {
                        'locale': None, # To be filled with the current locale name
                    }
                },
                'stacked': True,
            },
            'y': {
                'stacked': True,
            }
        },
        'plugins': {
            'tooltip': {
                'enabled': True,
                # To be replaced in the browser with callback functions
                'callbacks': {
                    'title': None,
                    'label': None
                },
                # Variables for the callback functions
                'callbackVariables': {
                    'timeFormat': None, # To be filled from the timespan config
                }
            }
        },
        'interaction': {
            'mode': 'point',
        },
        # To be replaced in the browser with functions
        'onHover': None,
        'onClick': None
    }
}

# Retrieves data from the database according to the arguments and renders the page using a template
def index(request, timespan_name=config.default_timespan, time_input='recent'):
    
    # Get timespan config
    timespan_name = timespan_name.lower()
    timespan = config.timespans[timespan_name]
    
    # Get child timespan (used for navigation from the chart)
    child_timespan_name = timespan.get('child_timespan')
    child_timespan = config.timespans.get(child_timespan_name)

    # Process time input
    if time_input == 'recent':
        time = None
    else:
        time_decoder = timespan.get('input_decoder')
        if time_decoder is None:
            time = datetime.strptime(time_input, timespan['input_format']) # decode the time using the format string in config
        else:
            time = time_decoder(time_input) # decode the time using the decoder function in config

    # Set for how long time the data should be retrieved and what time unit they should be grouped by
    delta = relativedelta(**timespan['delta'])
    group_by = timespan['group_by']

    # Retrieve the data from the database
    queryset = LoggedObject.query(window_start=time, group_unit=group_by)

    # Get a set of class names from queryset
    class_names = sorted(set(entry['class_name'] for entry in queryset.values('class_name') if entry['class_name'])) + [None]

    # Initialize chart datasets
    chart_datasets = {}
    for class_name in class_names:
        chart_datasets[class_name] = {
            'label': class_name or 'not_recognized',
            'data': []
        }

    # Specify child input format (for navigation from the chart)
    if child_timespan:
        child_input_format = child_timespan['input_format']
    else:
        child_input_format = ""
    
    # Populate the datasets
    for entry in queryset:

        data = chart_datasets[entry['class_name']]['data']
        time = entry['time']
        count = entry['count']
        
        data.append({
            'x': time,
            'y': count,
            'inputTime': time.strftime(child_input_format)
        })
    
    # Convert chart datasets
    chart_datasets = list(chart_datasets.values())

    # Copy the chart data base
    chart_config = deepcopy(chart_config_base)
    
    # Set values in chart_config
    chart_config['label'] = _('Occurence of bird species')
    chart_config['type'] = 'bar'

    # Put the datasets with the actual data to chart_config
    chart_config['data']['datasets'] = chart_datasets

    # Set x_axis_options
    x_axis_options = chart_config['options']['scales']['x']
    
    # Set time options
    x_axis_options['time'] = {
        'unit': group_by,
        'displayFormats': {
            group_by: timespan['time_axis_format']
        }
    }

    # Set the locale
    x_axis_options['adapters']['date']['locale'] = get_language()

    # Enable offset
    x_axis_options['offset'] = True

    
    # Prepare tooltip variables
    tooltip_variables = chart_config['options']['plugins']['tooltip']['callbackVariables']
    tooltip_variables['timeFormat'] = _(timespan['time_axis_format'])


    # Prepare variables for the menu
    
    # Get minimum and maximum times that are allowed for the time input
    (min_time, max_time) = LoggedObject.get_time_range()

    # Set default time for the time input
    if time_input == 'recent':
        default_time = datetime.now()
    else:
        default_time = time

    # Prepare available timespans
    timespans_available = {}
    for name, cnf in config.timespans.items():
        time_input_format = cnf['input_format']
        timespans_available[name] = {
            'name': name,
            'verbose_name': cnf['verbose_name'],
            'input_type': cnf['input_type'],
            'default_time': default_time.strftime(time_input_format),
            'min_time': min_time.strftime(time_input_format),
            'max_time':  max_time.strftime(time_input_format),
            'title_format': _(cnf['title_format']),
            'child_timespan': cnf.get('child_timespan')
        }
    
    # Select the current timespan data from timespans_available
    current_timespan = timespans_available[timespan_name]

    # Construct the template context
    template_context = {
        'timespans_available': timespans_available,
        'current_timespan': current_timespan,
        'time_input': time_input,
        'time': time,
        'chart_config': chart_config
    }

    # Render the template with the context and return the response
    return render(request, 'object_statistics/index.html', template_context)
