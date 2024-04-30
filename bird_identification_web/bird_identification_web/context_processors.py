# (C) Hynek V. Svobodny, 2024

# This context processor adds the current season name to every template context
# Used by the base template to specify the seasonal stylesheet

#Based on the Weather Station project (https://github.com/hyneq/rpi-weather-station-www/)

import datetime, json
from django.conf import settings

def season(request):
    seasons_path = settings.BASE_DIR / 'seasons.json'
    with open(seasons_path) as f:
        seasons = json.load(f)
    
    current_month = datetime.datetime.now().month
    for season in seasons.items():
        name = season[0]
        start_month = season[1][0]
        end_month = season[1][1]
        if (start_month < end_month and start_month <= current_month <= end_month) or (start_month > end_month and (current_month >= start_month or current_month <= end_month)):
            return {'season': name}