from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import utils as ut
import pandas as pd
import calendar
"""
-- Documentation --
    The class "Map" used to create maps.
"""


class Map:
    def __init__(self, ds, dw):
        """
        Initializes a Map object.

        Parameters:
        - `ds`: Geopandas DataFrame with city data, including information such as latitude, longitude, average temperature, city name, and date.
        - `dw`: Geopandas DataFrame with world map data.
        """
        self.ds = ds  # geopandas dataframe with city data
        self.dw = dw  # geopandas dataframe with world map data

    def create_map(self, legend=False, date =""):
        """
        Creates a map showing the position of the cities in the dataset
        Parameters:
        - legend: parameter to decide if showing the legend or not
        - date: parameter to decide if choosing a date or not
        """
        # create a world map
        axis = self.dw.plot(color='grey', edgecolor='black')
        self.ds.plot(column='AverageTemperature', ax=axis, markersize=80, legend=legend, legend_kwds={'shrink': 0.3})
        plt.title('Average Temperatures in World Major Cities C°', fontsize=15)
        fig = plt.gcf()
        fig.set_size_inches(20, 16)
        plt.show()

    def create_map_date(self, date):
        """
        Show the average temperatures of the major cities in a given date
        Parameters:
        - date: the chosen date
        """
        filtered_ds = self.ds[self.ds['dt'] == date]

        if not filtered_ds.empty:
            self.ds = filtered_ds
            self.create_map(True)
            print("Map of " + date)
        else:
            print('Data not available for the given date.')

    def create_map_gif(self, dates):
        """
        Creates an animated GIF displaying temperature changes over a sequence of dates.
        Parameters:
        - `dates`: List of dates for creating the animation.
        """
        fig, ax = plt.subplots(figsize=(20, 16))
        axis = self.dw.plot(ax=ax, color='grey', edgecolor='black')
        dates.sort()

        def update(frame):
            current_date = dates[frame]
            filtered_cities = self.ds[self.ds['dt'] == current_date]
            scatter = filtered_cities.plot(column='AverageTemperature', ax=axis, markersize=80)
            plt.title(f'Average Temperatures in World Major Cities C° ({current_date})', fontsize=25)
            return scatter

        def init():
            # create an empty colorbar with the appropriate colormap and normalization
            sm = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=-40, vmax=40))
            sm.set_array([])    # empty array for the data range
            # add the colorbar to the figure
            cbar = plt.colorbar(sm, ax=ax, fraction=0.02, pad=0.04)
            cbar.ax.tick_params(labelsize=14)
            return cbar

        animation = FuncAnimation(fig, update, frames=len(dates), interval=250, init_func=init)
        animation.save('temperature_animation_dates.gif', fps=1)

    def date_map_gif(self, min_date, max_date):
        """
        Creates an animated GIF displaying temperature changes within a date range.

        Parameters:
        - `min_date`: Start date for the animation.
        - `max_date`: End date for the animation.
        """
        panda_dates = self.ds[(self.ds['dt'] >= min_date) & (self.ds['dt'] <= max_date)]
        dates = panda_dates['dt'].unique().tolist()
        self.create_map_gif(dates)

    def create_map_range(self, start_date, end_date):
        """
        Creates a world map highlighting the top 5 cities with the highest temperature range within a specified date range.

        Parameters:
        - `start_date`: Start date for filtering the dataset.
        - `end_date`: End date for filtering the dataset.
        """
        # filter data within the specified date range
        filtered_data = self.ds[(self.ds['dt'] >= start_date) & (self.ds['dt'] <= end_date)]
        # calculate temperature range for each city within the specified date range
        city_temperature_ranges = filtered_data.groupby('City')['AverageTemperature'].agg(['min', 'max']).apply(
            lambda x: (x['min'], x['max']), axis=1)
        # get top 5 cities with the highest temperature difference within the specified date range
        top_cities = city_temperature_ranges.apply(lambda x: x[1] - x[0]).nlargest(5).index
        # filter data for top 5 cities within the specified date range
        top_cities_data = filtered_data[filtered_data['City'].isin(top_cities)]

        # create a world map
        axis = self.dw.plot(color='grey', edgecolor='black')
        # plot top 5 cities with the highest temperature range within the specified date range
        top_cities_data.plot(column='AverageTemperature', ax=axis, markersize=80)

        # annotate the map with city names and temperature ranges
        i = -80
        for idx, (city, (min_temp, max_temp)) in enumerate(city_temperature_ranges[top_cities].items()):
            plt.text(0, i, f'{city}: {round(min_temp, 1)}°C to {round(max_temp, 1)}°C: {round(max_temp - min_temp, 1)}C°',
                     fontsize=24, horizontalalignment='center')
            i = i - 9
        plt.title('Top 5 Cities with Highest Temperature Range\n{} to {}'.format(start_date, end_date), fontsize=15)
        fig = plt.gcf()
        fig.set_size_inches(20, 16)
        plt.show()

    def best_route_obj(self, date, start_city, target_city):
        """
        Finds the best route from a starting city to a target city based on both distance and temperature.
        ! Be aware that the function.py module must be accessible !

        Parameters:
        - `date`: Date for filtering the dataset.
        - `start_city`: Name of the starting city.
        - `target_city`: Name of the target city.

        Returns:
        - List representing the best route from the `start_city` to the `target_city`.
        """
        path = ut.best_route(self.ds, '2001-04-01', 'Peking', 'Los Angeles')
        return path

    def avg_temperature_graph(self, city, month):
        """
        Plots the average temperature for a specific city over the specified month and save it as a png file.

        Parameters:
        - `city`: Name of the city for which the average temperature will be plotted.
        - `month`: Numeric representation of the month (1 to 12).
        """
        self.ds['dt'] = pd.to_datetime(self.ds['dt'])
        filtered_ds = self.ds[(self.ds['City'] == city) & (self.ds['dt'].dt.month == month)]
        # get the month name using the calendar module
        month = calendar.month_name[month]
        # plotting
        plt.figure(figsize=(10, 6))
        plt.plot(filtered_ds['dt'], filtered_ds['AverageTemperature'], color='red', marker='o')
        plt.title(
            f'Average Temperature (C°) in {city} for {month}- from {filtered_ds["dt"].dt.year.min()} to {filtered_ds["dt"].dt.year.max()}',
            fontsize=15)
        plt.xlabel('Year')
        plt.ylabel('Average Temperature')
        plt.grid(True)
        plt.savefig('average_temperature_years.png')




