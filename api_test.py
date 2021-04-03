'''
This module tests the OpenWeatherMap API
using pyown wrapper
'''

import json
from pyowm import OWM
from pprint import pprint
from pyowm.utils import config
from geopy.geocoders import Nominatim
from pyowm.utils import timestamps, formatting
from datetime import datetime, timedelta, timezone

ADDRESS = "Lviv, Ukraine"
geolocator = Nominatim(user_agent="Weather")
location = geolocator.geocode(ADDRESS)

owm = OWM('d84c6b6db6edee8d87f4a5396c561285')
mgr = owm.weather_manager()

observation = mgr.weather_at_place(ADDRESS)
w = observation.weather

print("Status of the weather: ")
print(w.detailed_status)  # prints a detailed status

# Default unit: 'meters_sec'
wind_dict_in_meters_per_sec = observation.weather.wind()
print("Wind speed (m/s): ")
print(wind_dict_in_meters_per_sec['speed'])  # speed of wind
print("Degree of wind: ")
print(wind_dict_in_meters_per_sec['deg'])  # degree of wind

# print rain data if there is any
rain_dict = w.rain
if rain_dict:
    print("Rain data within the range of 1 hour: ")
    print(rain_dict['1h'])
    print("Rain data within the range of 3 hours: ")
    print(rain_dict['3h'])

# sunrise and sunset data for solar panels
sunrise_date = w.sunrise_time(timeformat='date')
print("Sunrise time: ")
print(sunrise_date)
sunrset_date = w.sunset_time(timeformat='date')
print("Sunset time: ")
print(sunrset_date)

with open("observation_data.txt", "w", encoding="utf-8") as output_1:
    output_1.write("Status:\n")
    output_1.write(w.detailed_status + "\n")
    output_1.write("Wind speed:\n")
    output_1.write(str(wind_dict_in_meters_per_sec['speed']) + "\n")
    output_1.write("Wind degree:\n")
    output_1.write(str(wind_dict_in_meters_per_sec['deg']) + "\n")

    if rain_dict:
        output_1.write("Rain data within the range of 1 hour:\n")
        output_1.write(str(rain_dict['1h']) + "\n")
        output_1.write("Rain data within the range of 3 hours:\n")
        output_1.write(str(rain_dict['3h']) + "\n")

    output_1.write("Sunrise time:\n")
    output_1.write(str(sunrise_date) + "\n")
    output_1.write("Sunset time:\n")
    output_1.write(str(sunrset_date) + "\n")

# allows to access historycal information
print("One call historical data(three days ago epoch):\n ")

three_days_ago_epoch = int(
    (datetime.now() - timedelta(days=3)).replace(tzinfo=timezone.utc).timestamp())

one_call_three_days_ago = mgr.one_call_history(
    lat=location.latitude, lon=location.longitude, dt=three_days_ago_epoch)
for i in one_call_three_days_ago.forecast_hourly:
    temp = i.__dict__
    temp["ref_time"] = datetime.utcfromtimestamp(
        temp["ref_time"]).strftime('%Y-%m-%d %H:%M:%S')
    pprint(temp)

    with open("historical_data.txt", "a", encoding="utf-8") as output_2:
        json.dump(temp, output_2, indent=2)

print("One call data for 7 days:\n ")
one_call = mgr.one_call(lat=location.latitude,
                        lon=location.longitude, units="metric")

for i in one_call.forecast_daily:
    temp = i.__dict__
    temp["ref_time"] = datetime.utcfromtimestamp(
        temp["ref_time"]).strftime('%Y-%m-%d %H:%M:%S')
    temp["srise_time"] = datetime.utcfromtimestamp(
        temp["srise_time"]).strftime('%Y-%m-%d %H:%M:%S')
    temp["sset_time"] = datetime.utcfromtimestamp(
        temp["sset_time"]).strftime('%Y-%m-%d %H:%M:%S')
    pprint(temp)

    with open("forecast_data.txt", "a", encoding="utf-8") as output_3:
        json.dump(temp, output_3, indent=2)
