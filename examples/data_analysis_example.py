'''
This module demonstrates
different python libraries
that will help to work with
weather data
'''

import json
import pandas as pd
import seaborn as sns
from rosely import WindRose
import matplotlib.pyplot as plt
import plotly.figure_factory as ff

def convert_from_json_to_csv(file_name: str):
    '''
    Convert json file from OpenWeatherMap api
    to a csv file that will be easier to analyze
    with pandas library
    '''
    with open(file_name, "r", encoding="utf-8") as input_file:
        data = json.load(input_file)

    final_data = pd.json_normalize(data)

    return final_data

def prep_data(data):
    '''
    Prepare wind data for plotting
    '''
    wind_data = data[["ref_time", "wnd.speed", "wnd.deg"]]
    wind_data["ref_time"] = pd.to_datetime(wind_data['ref_time'], format="%Y-%m-%d %H:%M:%S")

    wind_data["day"] = [d.day for d in wind_data["ref_time"]]
    wind_data["hour"] = [d.hour for d in wind_data["ref_time"]]

    to_heatmap = pd.pivot_table(wind_data, values='wnd.speed', index=["day"], columns='hour')

    return to_heatmap

def create_heatmap_seaborn(data):
    '''
    Create interactive heatmap using seaborn
    '''
    to_heatmap = prep_data(data)

    sns.heatmap(to_heatmap, cmap="YlGnBu", annot=True)
    plt.show()

def create_heatmap_plotly(data):
    '''
    Create interactive heatmap using plotly
    '''
    to_heatmap = prep_data(data)

    to_heatmap_plotly = {
        'z': to_heatmap.values,
        'x': to_heatmap.columns.to_list(),
        'y': to_heatmap.index.to_list()
    }

    fig = ff.create_annotated_heatmap(
        z=to_heatmap_plotly["z"],
        x=to_heatmap_plotly["x"],
        y=to_heatmap_plotly["y"],
        colorscale="Viridis")

    fig.show()


def create_wind_rose(data):
    '''
    Create wind rose using rosely
    '''
    data = data[["wnd.speed", "wnd.deg"]]
    data.rename(columns = {'wnd.speed':'ws'}, inplace = True)
    data.rename(columns = {'wnd.deg':'wd'}, inplace = True)

    WR = WindRose(data)
    WR.plot(
        template='seaborn', colors='Plotly3',
        title='Lviv, Ukraine', output_type='show'
    )


if __name__ == "__main__":
    # create_heatmap_seaborn(convert_from_json_to_csv("historical_data_2.json"))
    # create_heatmap_plotly(convert_from_json_to_csv("historical_data_2.json"))
    create_wind_rose(convert_from_json_to_csv("historical_data_2.json"))
