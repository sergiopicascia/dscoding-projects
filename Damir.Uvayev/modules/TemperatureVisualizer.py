import geopandas as gpd
import matplotlib.pyplot as plt
from modules.utils import convert_to_decimal
import pandas as pd


class TemperatureVisualizer:
    def __init__(self, data):
        self.data = data

    @staticmethod
    def annotate_countries(ax, world):
        
        world_projected = world.to_crs(epsg=3395)
        world_projected['centroid'] = world_projected.geometry.centroid

        
        centroids = world_projected['centroid'].to_crs(world.crs)

        
        for idx, row in world.iterrows():
            
            centroid = centroids.iloc[idx]
            
            if centroid is None or pd.isna(centroid.x) or pd.isna(centroid.y):
                continue
            x, y = centroid.x, centroid.y
            ax.annotate(row['ADMIN'], xy=(x, y), xytext=(3, 3), textcoords="offset points", fontsize=8)

    @staticmethod
    def plot_average_temperatures(avg_temperatures):
        avg_temperatures = avg_temperatures.sort_values(by='AverageTemperature')
        plt.figure(figsize=(10, 6))
        plt.bar(avg_temperatures['City'], avg_temperatures['AverageTemperature'], color='skyblue')
        plt.xlabel('City')
        plt.ylabel('Average Temperature')
        plt.title('Average City Temperatures')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_temperature_trends(self):
        df_copy = self.data.copy()
        df_copy['Latitude'] = df_copy['Latitude'].apply(convert_to_decimal)
        df_copy['Longitude'] = df_copy['Longitude'].apply(convert_to_decimal)

        temp_ranges = df_copy.groupby('City').apply(
            lambda x: x['AverageTemperature'].max() - x['AverageTemperature'].min())
        df_copy['TempRange'] = df_copy['City'].map(temp_ranges)

        gdf = gpd.GeoDataFrame(df_copy, geometry=gpd.points_from_xy(df_copy.Longitude, df_copy.Latitude))

        world = gpd.read_file('ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp')
        if world.crs is not None and world.crs.to_epsg() != 4326:
            world = world.to_crs(epsg=4326)

        
        ax = world.plot(color='lightgrey', edgecolor='black', figsize=(15, 10))

        
        gdf.plot(ax=ax, column='TempRange', cmap='coolwarm', legend=True, markersize=10)

        
        self.annotate_countries(ax, world)

        
        ax.set_xlim([-180, 180])
        ax.set_ylim([-90, 90])

        plt.show()
