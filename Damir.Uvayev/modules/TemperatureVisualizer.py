import geopandas as gpd
import matplotlib.pyplot as plt
from modules.utils import convert_to_decimal

class TemperatureVisualizer:
    def __init__(self, data):
        self.data = data

    def annotate_countries(self, ax, world):
        for x, y, label in zip(world.geometry.centroid.x, world.geometry.centroid.y, world['ADMIN']):
            ax.annotate(label, xy=(x, y), xytext=(3, 3), textcoords="offset points", fontsize=8)

    def plot_temperature_trends(self):
        df_copy = self.data.copy()
        df_copy['Latitude'] = df_copy['Latitude'].apply(convert_to_decimal)
        df_copy['Longitude'] = df_copy['Longitude'].apply(convert_to_decimal)

        temp_ranges = df_copy.groupby('City').apply(lambda x: x['AverageTemperature'].max() - x['AverageTemperature'].min())
        df_copy['TempRange'] = df_copy['City'].map(temp_ranges)

        gdf = gpd.GeoDataFrame(df_copy, geometry=gpd.points_from_xy(df_copy.Longitude, df_copy.Latitude))

        world = gpd.read_file('ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp')
        ax = world.plot(color='lightgrey', edgecolor='black', figsize=(15, 10))
        self.annotate_countries(ax, world)
        gdf.plot(ax=ax, column='TempRange', cmap='coolwarm', legend=True, markersize=10)
        plt.show()
