import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from modules.utils import convert_to_decimal

def plot_data(avg_temperatures):
    merged_data = avg_temperatures.merge(avg_temperatures[['City', 'Latitude', 'Longitude']], on='City', how='left')

    merged_data.drop_duplicates(subset='City', inplace=True)

    merged_data['Latitude'] = merged_data['Latitude'].apply(convert_to_decimal)
    merged_data['Longitude'] = merged_data['Longitude'].apply(convert_to_decimal)

    gdf = gpd.GeoDataFrame(merged_data, geometry=gpd.points_from_xy(merged_data.Longitude, merged_data.Latitude))

    world = gpd.read_file(gpd.datasets.get_path('ne_110m_admin_0_countries.shp'))
    ax = world.plot(color='lightgrey', edgecolor='black', figsize=(15, 10))

    gdf.plot(ax=ax, marker='o', color='red', markersize=50, alpha=0.5)

    plt.title("Average Temperature for Cities")
    plt.show()


def annotate_countries(ax, world):
    for x, y, label in zip(world.geometry.centroid.x, world.geometry.centroid.y, world['ADMIN']):
        ax.annotate(label, xy=(x, y), xytext=(3, 3), textcoords="offset points", fontsize=8)


def plot_temperature_trends(df):
    df_copy = df.copy()
    df_copy['Latitude'] = df_copy['Latitude'].apply(convert_to_decimal)
    df_copy['Longitude'] = df_copy['Longitude'].apply(convert_to_decimal)

    temp_ranges = df_copy.groupby('City').apply(lambda x: x['AverageTemperature'].max() - x['AverageTemperature'].min())
    df_copy['TempRange'] = df_copy['City'].map(temp_ranges)

    gdf = gpd.GeoDataFrame(df_copy, geometry=gpd.points_from_xy(df_copy.Longitude, df_copy.Latitude))

    world = gpd.read_file('ne_110m_admin_0_countries\\ne_110m_admin_0_countries.shp')
    ax = world.plot(color='lightgrey', edgecolor='black', figsize=(15, 10))

    gdf.plot(ax=ax, marker='o', color='red', markersize=df_copy['TempRange'] * 10, alpha=0.5)

    annotate_countries(ax, world)

    plt.title("Cities with Largest Temperature Ranges")
    plt.show()


def plot_city_temperature_trend(data, city):
    df = data[data['City'] == city].copy()
    df['dt'] = pd.to_datetime(df['dt'])
    df['Latitude'] = df['Latitude'].apply(convert_to_decimal)
    df['Longitude'] = df['Longitude'].apply(convert_to_decimal)

    plt.figure(figsize=(15, 7))
    plt.plot(df['dt'], df['AverageTemperature'], label=city)
    plt.title(f"Temperature Trend for {city}")
    plt.xlabel("Year")
    plt.ylabel("Average Temperature")
    plt.legend()
    plt.grid(True)
    plt.show()