import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import geopandas as gpd

image_url = "https://github.com/muditaindah/KualitasUdara/blob/main/dashboard/beijing.jpg"
st.write("<h1 style='text-align: center; color: #3498db'>Air Quality Analysis of Beijing</h1>", unsafe_allow_html=True)
st.image("image_url", use_column_width=True)

big_df = pd.read_csv('compilation_data.csv')
big_df_clean = big_df.drop_duplicates()

st.write(f"<h2 style='text-align:center; font-size: 28px; color: #3498db'>Average Air Quality Index of {'station'} from 2013 - 2016</h2>", unsafe_allow_html=True)
st.write("<h2 style='text-align:center; font-size:24px; color: #3498db'>Select a city</h2>", unsafe_allow_html=True)
city = st.selectbox('', big_df_clean['station'].unique())

mean_pm25 = big_df_clean.groupby('station')['PM2.5'].mean().reset_index()
mean_pm10 = big_df_clean.groupby('station')['PM10'].mean().reset_index()
mean_so2 = big_df_clean.groupby('station')['SO2'].mean().reset_index()
mean_no2 = big_df_clean.groupby('station')['NO2'].mean().reset_index()
mean_co = big_df_clean.groupby('station')['CO'].mean().reset_index()
mean_o3 = big_df_clean.groupby('station')['O3'].mean().reset_index()


def get_air_quality_category(pollutant_name, value):
    if pollutant_name == "PM2.5":
        if value < 25:
            return "Good", "green"
        elif value < 50:
            return "Fair", "yellow"
        elif value < 100:
            return "Poor", "orange"
        else:
            return "Very Poor", "red"
    
    elif pollutant_name == "PM10":
        if value < 40:
            return "Good", "green"
        elif value < 80:
            return "Fair", "yellow"
        elif value < 120:
            return "Poor", "orange"
        else:
            return "Very Poor", "red"
    
    elif pollutant_name == "SO2":
        if value < 100:
            return "Good", "green"
        elif value < 200:
            return "Fair", "yellow"
        elif value < 300:
            return "Poor", "orange"
        else:
            return "Very Poor", "red"
    
    elif pollutant_name == "NO2":
        if value <= 50:
            return "Good", "green"
        elif value <= 100:
            return "Fair", "yellow"
        else:
            return "Very Poor", "red"
    
    elif pollutant_name == "CO":
        if value <= 100:
            return "Good", "green"
        else:
            return "Poor", "red"
    
    elif pollutant_name == "O3":
        if value <= 50:
            return "Good", "green"
        elif value <= 85:
            return "Moderate", "yellow"
        else:
            return "Poor", "red"

def display_pollutant_value(pollutant_name, value):
    category, color = get_air_quality_category(pollutant_name, value)
    st.write(
        f"""
        <div style="text-align: center; background-color: {color}; padding: 5px; border-radius: 5px; margin: 10px 0;">
            <h2 style="color: black;">{pollutant_name}</h2>
            <h3 style="color: black;">{value:.1f} ({category})</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

if city in mean_pm25['station'].values:
    pm25_value = mean_pm25.loc[mean_pm25['station'] == city, 'PM2.5'].values[0]
    display_pollutant_value("PM2.5", pm25_value)

if city in mean_pm10['station'].values:
    pm10_value = mean_pm10.loc[mean_pm10['station'] == city, 'PM10'].values[0]
    display_pollutant_value("PM10", pm10_value)

if city in mean_so2['station'].values:
    so2_value = mean_so2.loc[mean_so2['station'] == city, 'SO2'].values[0]
    display_pollutant_value("SO2", so2_value)

if city in mean_no2['station'].values:
    no2_value = mean_no2.loc[mean_no2['station'] == city, 'NO2'].values[0]
    display_pollutant_value("NO2", no2_value)

if city in mean_co['station'].values:
    co_value = mean_co.loc[mean_co['station'] == city, 'CO'].values[0]
    display_pollutant_value("CO", co_value)

if city in mean_o3['station'].values:
    o3_value = mean_o3.loc[mean_o3['station'] == city, 'O3'].values[0]
    display_pollutant_value("O3", o3_value)

stations = big_df_clean['station'].unique()
pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
colors = [
    '#FF0000',
    '#0000FF',
    '#00FF00',
    '#FFA500',
    '#800080',
    '#00FFFF',
    '#FF00FF',
    '#FFFF00',
    '#8B4513',
    '#FFC0CB',
    '#006400',
    '#00008B'
]

st.write(f"<h2 style='text-align:center; font-size: 28px; color: #3498db'>Time Series & Geo Spatial Analysis</h2>", unsafe_allow_html=True)


def plot_pollutant(pollutant):
    plt.figure(figsize=(10, 7))
    for i, station in enumerate(stations):
        data_station = big_df_clean[big_df_clean['station'] == station]
        if pollutant in data_station.columns:
            data_jam = data_station.groupby('hour')[pollutant].mean()
            plt.plot(data_jam.index, data_jam, label=station, color=colors[i % len(colors)])
    plt.title(f'Concentration of {pollutant} in 12 cities')
    plt.xlabel('Hour')
    plt.ylabel('Concentration')
    plt.legend(title='Station', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    st.pyplot(plt)

st.write("<h2 style='text-align:center; font-size:24px; color: #3498db'>Select pollutant to display</h2>", unsafe_allow_html=True)
selected_pollutant = st.selectbox('', pollutants)
plot_pollutant(selected_pollutant)


coordinates = {
    'Aotizhongxin': (40.003, 116.407),
    'Changping': (40.195, 116.230),
    'Dingling': (40.286, 116.170),
    'Dongsi': (39.952, 116.434),
    'Guanyuan': (39.942, 116.361),
    'Gucheng': (39.928, 116.22),
    'Huairou': (40.394, 116.644),
    'Nongzhanguan': (39.972, 116.473),
    'Shunyi': (40.144, 116.720),
    'Tiantan': (39.874, 116.434),
    'Wanliu': (39.98944, 116.28972),
    'Wanshouxigong': (39.867, 116.366)
}

china_data = gpd.read_file(r'.\peta\chn_admbnda_adm1_ocha_2020.shp')
beijing_data = china_data[china_data['ADM1_EN'] == 'Beijing Municipality']
from shapely.geometry import Point
pollutants = ['PM2.5', 'PM10', 'CO', 'O3', 'NO2', 'SO2']

def plot_map(selected_pollutant):
    mean_pollutant = big_df_clean.groupby('station')[selected_pollutant].mean().reset_index()
    mean_pollutant['lat'] = mean_pollutant['station'].map(lambda x: coordinates[x][0])
    mean_pollutant['lon'] = mean_pollutant['station'].map(lambda x: coordinates[x][1])
    geometry = [Point(lon, lat) for lon, lat in zip(mean_pollutant['lon'], mean_pollutant['lat'])]
    geo_df = gpd.GeoDataFrame(mean_pollutant, geometry=geometry)

    fig, ax = plt.subplots(figsize=(12, 10))
    beijing_data.plot(ax=ax, color='lightgreen', linewidth=2, label='Batas')
    geo_df.plot(column=selected_pollutant, cmap="OrRd", legend=True, ax=ax, markersize=100)

    for x, y, label in zip(mean_pollutant['lon'], mean_pollutant['lat'], mean_pollutant['station']):
        ax.text(x, y, label, fontsize=8, ha="right", va='bottom')

    ax.set_title(f'Mean Concentration of {selected_pollutant} in 12 cities')
    plt.tight_layout()
    st.pyplot(fig)

plot_map(selected_pollutant)
