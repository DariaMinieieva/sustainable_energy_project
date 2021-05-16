import math
from math import radians, cos, sin, atan2, pi, asin, degrees
import folium
from pyowm.utils import timestamps, formatting
from datetime import datetime, timedelta, timezone
from pyowm import OWM
from map_creator.linkedlist import LinkedList
from map_creator.adt_realization import SolarPanels, WindTurbine
from map_creator.key import api_key
from global_land_mask import globe
from tabulate import tabulate


def get_lat_long(central_lat: float, central_long: float, distance: int) -> list:
    '''
    Create list of tuples with latitude and longtitude in the given area
    '''
    earth_radius = 6378.1
    bearing = 0  # direction

    distance_start = distance

    if globe.is_land(central_lat, central_long):
        res = [(central_lat, central_long)]
    else:
        res = []

    for _ in range(4):
        for __ in range(4):
            latitute_1 = radians(central_lat)
            longtitute_1 = radians(central_long)

            latitute_2 = asin(sin(latitute_1)*cos(distance_start/earth_radius) +
                              cos(latitute_1)*sin(distance_start/earth_radius)*cos(bearing))

            longtitute_2 = longtitute_1 + atan2(sin(bearing)*sin(distance_start/earth_radius)*cos(latitute_1),
                                                cos(distance_start/earth_radius)-sin(latitute_1)*sin(latitute_2))

            latitute_2 = degrees(latitute_2)
            longtitute_2 = degrees(longtitute_2)
            if globe.is_land(latitute_2, longtitute_2):
                res.append((latitute_2, longtitute_2))

            bearing += pi/2

        distance_start = distance_start/(2**0.5)
        if bearing == 2*pi:
            bearing = pi/4
        else:
            bearing = 0

    return res


def map_generator(locations: list, start_location: tuple, max_value: list):
    '''
    Generates map with markers
    '''

    locations.pop(max_value[0])

    gen_map = folium.Map(location=start_location)

    marker_layer = folium.FeatureGroup(name="Markers with locations")

    if max_value[1][1]:
        text = f"The best option\nEfficiency: {max_value[1][0]}\nRecomended turbine direction: {max_value[1][1]}"
    else:
        text = f"The best option\nEfficiency: {max_value[1][0]}\n"

    folium.Marker(location=max_value[0], popup=text, icon=folium.Icon(
        color='red', icon='plus')).add_to(marker_layer)

    try:
        central = locations.pop(start_location)
        if central[1]:
            text = f"Efficiency: {central[0]}\nRecomended turbine direction: {central[1]}"
        else:
            text = f"Efficiency: {central[0]}"

        folium.Marker(location=start_location, popup=text, icon=folium.Icon(
            color='green', icon='plus')).add_to(marker_layer)
    except:
        pass

    for loc in locations:
        if locations[loc][1]:
            text = f"Efficiency: {locations[loc][0]}\nRecomended turbine direction: {locations[loc][1]}"
        else:
            text = f"Efficiency: {locations[loc][0]}"
        folium.Marker(location=loc, popup=text).add_to(marker_layer)

    # folium.Marker(location=start_location, popup="You are here!",
    #               icon=folium.Icon(color='green', icon='plus')).add_to(marker_layer)

    marker_layer.add_to(gen_map)

    gen_map.add_child(folium.LayerControl())

    gen_map.save("templates/map.html")


def get_historical_data(latitude: float, longitude: float, energy_source: str) -> LinkedList:
    '''
    Get historical weather data for the last three days
    '''
    owm = OWM(api_key)
    mgr = owm.weather_manager()

    res = []

    for i in range(3, 0, -1):
        three_days_ago_epoch = int(
            (datetime.now() - timedelta(days=i)).replace(tzinfo=timezone.utc).timestamp())

        one_call_three_days_ago = mgr.one_call_history(
            lat=latitude, lon=longitude, dt=three_days_ago_epoch)

        res_list = []
        for i in one_call_three_days_ago.forecast_hourly:
            temp = i.__dict__
            temp["ref_time"] = datetime.utcfromtimestamp(
                temp["ref_time"]).strftime('%Y-%m-%d %H:%M:%S')
            res_list.append(temp)
        res.append(res_list)

    lst = LinkedList()

    if energy_source == "solar":
        for i in res:
            temp = SolarPanels()
            temp.set_sunrise(i[0]["srise_time"])
            temp.set_sunset(i[0]["sset_time"])
            temp.set_temperature(i[0]["temp"]["temp"] - 273.15)

            lst.add(temp)

    else:
        for i in res:
            temp = WindTurbine()
            temp.set_wnd_degree(i[0]["wnd"]["deg"])
            temp.set_wnd_speed(i[0]["wnd"]["speed"])

            lst.add(temp)

    return lst


def get_forecast_data(latitude: float, longtitute: float, energy_source: str) -> LinkedList:
    '''
    Get forecast weather data for the next seven days
    '''
    owm = OWM(api_key)
    mgr = owm.weather_manager()

    one_call = mgr.one_call(lat=latitude,
                            lon=longtitute, units="metric")

    res_list_2 = []
    for i in one_call.forecast_daily:
        temp = i.__dict__
        temp["ref_time"] = datetime.utcfromtimestamp(
            temp["ref_time"]).strftime('%Y-%m-%d %H:%M:%S')
        temp["srise_time"] = datetime.utcfromtimestamp(
            temp["srise_time"]).strftime('%Y-%m-%d %H:%M:%S')
        temp["sset_time"] = datetime.utcfromtimestamp(
            temp["sset_time"]).strftime('%Y-%m-%d %H:%M:%S')
        res_list_2.append(temp)

        lst = LinkedList()

    if energy_source == "solar":
        for i in res_list_2:
            temp = SolarPanels()
            temp.set_sunrise(i["srise_time"])
            temp.set_sunset(i["sset_time"])
            temp.set_temperature(i["temp"]["day"])

            lst.add(temp)

    else:
        for i in res_list_2:
            temp = WindTurbine()
            temp.set_wnd_degree(i["wnd"]["deg"])
            temp.set_wnd_speed(i["wnd"]["speed"])

            lst.add(temp)

    return lst


def calculate_efficiency(linked_lst: LinkedList, energy_source: str) -> tuple:
    '''
    Return tuple with average efficiency rate and direction of wind turbine(optional)
    '''
    average = 0
    turbine_direction = None

    if energy_source == "solar":
        for i in linked_lst:
            i.data.calculate_power()
            i.data.temperature_impact()
            average += i.data.get_power()
    else:
        for i in linked_lst:
            i.data.wind_efficiency()
            turbine_direction = i.data.direction_to_rotate()
            average += i.data._wind_efficiency_level

    return (average/len(linked_lst), turbine_direction)


def all_average_efficiency(locations: list, energy_source: str, type_of_data: str):
    '''
    Return tuple with a dictionary of latitudes and longtitudes as keys and efficiency as values
    '''
    data = {}
    max_value = [[0, 0], [0]]
    if type_of_data == "forecast":
        for i in locations:
            temp = get_forecast_data(i[0], i[1], energy_source)
            eff = calculate_efficiency(temp, energy_source)

            if max_value[1][0] < eff[0]:
                max_value = (i, eff)

            data[i] = eff
    else:
        for i in locations:
            temp = get_historical_data(i[0], i[1], energy_source)
            data[i] = calculate_efficiency(temp, energy_source)

            if max_value[1][0] < eff[0]:
                max_value = (i, eff)

            data[i] = eff

    return data, max_value


def create_txt(locations: tuple, energy_source: str, path: str):
    '''
    Create a txt file with a table of all points and their efficiency as a table
    '''
    location = locations[0]
    if energy_source == "solar":
        table = [[locations[1][0][0], locations[1][0][1], locations[1][1][0]]]
        for i in location:
            table.append([i[0], i[1], location[i][0]])
            table = sorted(table, key=lambda x: x[2])
            table.reverse()
        text_to_write = tabulate(table, headers=[
            'Latitute', 'Longtitute', "Efficiency"], tablefmt='orgtbl')

        with open(path, "w", encoding="utf-8") as output_file:
            output_file.write(text_to_write)

    else:
        table = [[locations[1][0][0], locations[1][0][1],
                  locations[1][1][0], locations[1][1][1]]]
        for i in location:
            table.append([i[0], i[1], location[i][0], location[i][1]])
            table = sorted(table, key=lambda x: x[2])
            table.reverse()
        text_to_write = tabulate(table, headers=[
            'Latitute', 'Longtitute', "Efficiency", "Wind direction"], tablefmt='orgtbl')

        with open(path, "w", encoding="utf-8") as output_file:
            output_file.write(text_to_write)


if __name__ == "__main__":
    lat, longt = 49.930971741581864, 25.365576302473254
    # lat, longt = 50.4501, 30.5234
    # lat, longt = 41.8719, 12.5674

    # lst = get_forecast_data(lat, longt, "solar")
    # calculate_efficiency(lst, "solar")

    # for i in lst:
    #     print(i)

    locations = get_lat_long(lat, longt, 3000)

    locs = all_average_efficiency(locations, "solar", "forecast")

    # map_generator(locs[0], (lat, longt), locs[1])
    create_txt(locs, "solar", "test.txt")
