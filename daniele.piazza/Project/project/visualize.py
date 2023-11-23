import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
import toml 
import pycountry_convert as pc
from abc import abstractmethod

"""
This class is used to visualize the data. It contains methods to create the following visualizations:
- Line Chart Year (line_year): a line chart with the average temperature of a selected city/country in each month
- Line Chart (line): a line chart with the average temperature of a selected city/country in each year
- Temperature Range Heatmap (range): a heatmap with the range of temperatures for each city/country for each year
- Average Temperature Heatmap (temperature): a heatmap with the average temperature for each city/country for each year
- Predicted Temperatures (predict_temperature): a line chart with the predicted temperatures for the next 50 years for a selected city/country
- Additional Statistics (statistics): a dataframe with additional statistics about the dataset
- Temperature Boxplot (boxplot): a boxplot and scatterplot with the distribution of temperatures for a selected city/country during each month

It also contains the following methods that should be implemented by the subclasses:
- _range_figure: a bubble map with the range of temperatures for each city/country for each year
- _temperature_figure: a bubble map with the average temperature for each city/country
"""
class Visualize:
    """
    Initialize the class with the data and calculate the yearly average temperature.

    Parameters
    ----------
    label : str
        The label of the cities/countries
    group : list
        The list of columns to be grouped by

    Attributes
    ----------
    data : pandas.DataFrame
        The original input data
    data_year : pandas.DataFrame
        Processed data with yearly averages and other statistics
    primaryColor : str
        Primary color for visualization theme
    backgroundColor : str
        Background color for visualization theme
    secondaryBackgroundColor : str
        Secondary background color for visualization theme
    textColor : str
        Text color for visualization theme
    """
    def __init__(self, label, group):
        self.label = label
        self.data.dropna(subset = [self.label], inplace = True)
        self.data.dropna(subset = ['AverageTemperature'], inplace = True)
        self.data['Year'] = self.data['dt'].dt.year
        self.data = self.data.sort_values(by = 'dt')
        self.data_year = self.data.groupby(group).agg(
            YearlyAverage = ('AverageTemperature', 'mean'), 
            AvailableMonths = ('AverageTemperature', 'count'), 
            MinTemp = ('AverageTemperature', 'min'), 
            MaxTemp = ('AverageTemperature', 'max'), 
            Std = ('AverageTemperature', 'std')).reset_index()
        self.data_year['YearlyAverage'] = self.data_year['YearlyAverage'].round(2)
        self._clean_data()
        self._calculate_annual_uncertainty()
        self._get_theme() 

    """
    Calculate the annual uncertainty for each city/country and save it in the data_year dataframe as a new column.
    Using the formula: sqrt(sum(uncertainty^2))
    """
    def _calculate_annual_uncertainty(self):
        annual_uncertainty = self.data.groupby(['Year', self.label])['AverageTemperatureUncertainty'].apply(lambda x: (x ** 2).sum() ** 0.5)
        self.data_year = pd.merge(self.data_year,
                                annual_uncertainty.reset_index(name = 'AverageTemperatureUncertainty'),
                                on = ['Year', self.label]
                                )

    """
    Clean the data by removing incomplete years.
    """
    def _clean_data(self):
        self.data.sort_values(by = 'dt', inplace = True)
        complete_years = self.data_year[self.data_year['AvailableMonths'] == 12][[self.label, 'Year']]
        self.data = pd.merge(self.data, complete_years, how = 'inner', on = [self.label, 'Year'])
        self.data_year = self.data_year[self.data_year['AvailableMonths'] == 12]
        self.data_year.sort_values(by = 'Year', inplace = True)
        self.data_year.drop(columns = ['AvailableMonths'], inplace = True)

    """
    Get the theme from the streamlit config file.

    Attributes
    ----------
    primaryColor : str
        Primary color for visualization theme
    backgroundColor : str
        Background color for visualization theme
    secondaryBackgroundColor : str
        Secondary background color for visualization theme
    textColor : str
        Text color for visualization theme
    """
    def _get_theme(self):
        config = toml.load('.streamlit/config.toml')
        self.primaryColor = config['theme']['primaryColor']
        self.backgroundColor = config['theme']['backgroundColor']
        self.secondaryBackgroundColor = config['theme']['secondaryBackgroundColor']
        self.textColor = config['theme']['textColor']

    """
    Set the layout for the figure.

    Parameters
    ----------
    fig : plotly.graph_objects.Figure
        The figure to be updated

    Returns
    -------
    fig : plotly.graph_objects.Figure
        The updated figure
    """
    def _fig_layout(self, fig):
        fig.update_layout({'paper_bgcolor': self.backgroundColor}, 
                          width = 1300, 
                          height = 700, 
                          margin = {'r':0, 't':0, 'l':0, 'b':0}, 
                          font = dict(color = self.primaryColor), 
                          updatemenus = [dict(bgcolor = self.secondaryBackgroundColor)]
                          )
        fig.update_mapboxes(bounds_east = 180, bounds_west = -180, bounds_north = 90, bounds_south = -70)
        fig.update_geos(
            resolution = 110, 
            showcountries = True, 
            countrycolor = 'Black', 
            lataxis = dict(range = [-90, 90]),
            lonaxis = dict(range = [-180, 180]), 
            showocean = True,
            oceancolor = self.backgroundColor, 
            showframe = False, 
            showcoastlines = False, 
        )
        return fig
    

    """
    Show a line chart with the average temperature of a selected city/country in each month for a selected year
    relative to the average temperature of the country/continent.

    Parameters
    ----------
    selected : str
        The name of the city/country to be shown
    year : int
        The year to be shown
    upper : str
        The label of "Country" or "Continent" to be shown in the chart

    Returns
    -------
    fig : plotly.graph_objects.Figure
        The figure with the line chart
    """
    def line_year(self, selected, year, upper):
        place = self.data[(self.data[self.label] == selected) & (self.data['Year'] == year)]
        up = self.data[(self.data[upper] == place[upper].iloc[0]) & (self.data['Year'] == year)]
        up = up.groupby(up['dt'].dt.month)['AverageTemperature'].mean().round(2).reset_index()
        month = place['dt'].dt.month
        fig = go.Figure()
        fig.add_trace(go.Scatter(x = month,
                                y = up['AverageTemperature'],
                                mode = 'lines+markers',
                                name = place[upper].iloc[0],
                                line = dict(color = self.secondaryBackgroundColor)
                                ))
        fig.add_trace(go.Scatter(x = month,
                                 y = place['AverageTemperature'].round(2),
                                 mode = 'lines+markers',
                                 name = selected,
                                 line = dict(color = self.primaryColor)
                                 ))
        fig.update_xaxes(title_text = 'Month', showgrid = False)
        fig.update_layout(xaxis = {'tickmode': 'array', 
                                'tickvals':month.unique(), 
                                'ticktext': place['dt'].dt.strftime('%B').unique()
                                })
        fig.update_yaxes(showgrid = False, zeroline = False)
        return self._fig_layout(fig)

    """
    Show a line chart with the average temperature of a selected city/country in each year and it's uncertainty.

    Parameters
    ----------
    selected : str
        The name of the city/country to be shown

    Returns
    -------
    fig : plotly.graph_objects.Figure
        The figure with the line chart
    """
    def line(self, selected):
        place = self.data_year[(self.data_year[self.label] == selected)]
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x = place['Year'], 
            y = place['YearlyAverage'] - place['AverageTemperatureUncertainty'], 
            marker = dict(color = self.primaryColor), 
            line = dict(width = 0), 
            mode = 'lines', 
            showlegend = False, 
            name = 'Lower bound'
        ))
        fig.add_trace(go.Scatter(
            x = place['Year'], 
            y = place['YearlyAverage'] + place['AverageTemperatureUncertainty'], 
            mode = 'lines', 
            marker = dict(color = self.primaryColor), 
            line = dict(width = 0), 
            fill = 'tonexty', 
            fillcolor = self.secondaryBackgroundColor, 
            showlegend = False, 
            name = 'Upper bound'
        ))
        fig.add_trace(go.Scatter(
            x = place['Year'], 
            y = place['YearlyAverage'], 
            mode = 'lines', 
            name = 'Average Temperature', 
            line = dict(color = self.primaryColor)
        ))
        fig.update_xaxes(showgrid = False)
        fig.update_yaxes(showgrid = False, zeroline = False)
        fig.update_layout(hovermode = "x")
        return self._fig_layout(fig)
        
    """
    Show a bubble map with the range of temperatures for each city/country for each year.
    Subclass should implement range_figure method.

    Parameters
    ----------
    n : int
        The number of cities to be shown (not supported for countries)

    Returns
    -------
    fig : plotly.graph_objects.Figure
        The figure with the bubble map
    """
    def range(self, n = None):
        df = self.data_year.copy()
        scaler = MinMaxScaler()
        df['Range'] = (df['MaxTemp'] - df['MinTemp']).round(2)
        min = df['Range'].min()
        max = df['Range'].max()
        df['Size'] =  scaler.fit_transform(df[['Range']])
        if n is not None:
            df = df.groupby('Year').apply(lambda x: x.nlargest(n, 'Range')).reset_index(drop = True)
        return self._range_figure(df, min, max)

    """
    Show a bubble map with the average temperature for each city/country for each year.
    Subclass should implement temperature_figure method.

    Parameters
    ----------
    n : int
        The number of cities to be shown (not supported for countries)
    high : bool
        Whether to show the cities with the highest or lowest temperatures (not supported for countries)

    Returns
    -------
    fig : plotly.graph_objects.Figure
        The figure with the bubble map
    """
    def temperature(self, n = None, high = False):
        df = self.data_year.copy()
        min = df['YearlyAverage'].min()
        max = df['YearlyAverage'].max()
        if n is not None:
            if high:
                df = df.groupby('Year').apply(lambda x: x.nlargest(n, 'YearlyAverage')).reset_index(drop = True)
            else:
                df = df.groupby('Year').apply(lambda x: x.nsmallest(n, 'YearlyAverage')).reset_index(drop = True)
        bubble_counts = df['Year'].value_counts()
        df['Size'] = df['Year'].apply(lambda x: 1000 / np.log((bubble_counts[x]) + 1))
        return self._temperature_figure(df, min, max)


    """
    Predict the temperatures for the next 50 years using polynomial regression and show them in a line chart.

    Parameters
    ----------
    selected : str
        The name of the city/country to be shown
    next : int
        The number of years to predict

    Returns
    -------
    fig : plotly.graph_objects.Figure
        The figure with the line chart
    """
    def predict_temperature(self, selected, next = 50):
        place = self.data_year[(self.data_year[self.label] == selected)]
        years = place['Year'].values.reshape(-1, 1)
        temperatures = place['YearlyAverage'].values
        poly_reg = PolynomialFeatures(degree = 4)
        years_poly = poly_reg.fit_transform(years) 
        lin_reg_poly = LinearRegression()
        lin_reg_poly.fit(years_poly, temperatures)
        future_years = np.arange(years.max(), years.max() + next + 1).reshape(-1, 1)
        future_years_poly = poly_reg.transform(future_years)
        predicted_temperatures = lin_reg_poly.predict(poly_reg.transform(years))
        future_predicted_temperatures = lin_reg_poly.predict(future_years_poly)
        fig = px.scatter(x = years.flatten(), 
                         y = temperatures, 
                         color_discrete_sequence = [self.secondaryBackgroundColor], 
                         labels = {'x': 'Year', 'y': 'Temperature'}
                         )
        fig.add_scatter(x = years.flatten(), 
                        y = predicted_temperatures, 
                        mode = 'lines', 
                        line = dict(color = self.primaryColor), 
                        name = 'Polynomial Regression'
                        )
        fig.add_scatter(x = future_years.flatten(), 
                        y = future_predicted_temperatures, 
                        mode = 'lines', 
                        line = dict(color = 'red'), 
                        name = 'Future Prediction'
                        )
        fig.update_layout(xaxis_title = 'Year', yaxis_title = 'Temperature')
        fig.update_xaxes(showgrid = False)
        fig.update_yaxes(showgrid = False, zeroline = False)
        return self._fig_layout(fig)
    

    """
    Calculate general statistics about the dataset: average, minimum, maximum and standard deviation of the temperatures for each city/country.

    Returns
    -------
    stats : pandas.DataFrame
        The dataframe with the statistics
    """
    def statistics(self):
        stats = self.data.groupby(self.label).agg(
            AverageTemperature = ('AverageTemperature', 'mean'), 
            MinTemperature = ('AverageTemperature', 'min'), 
            MaxTemperature = ('AverageTemperature', 'max'), 
            Std = ('AverageTemperature', 'std')).round(2)
        return stats
    
    """
    Show a boxplot and scatterplot with the distribution of temperatures for a selected city/country during each month of the years.

    Parameters
    ----------
    selected : str
        The name of the city/country to be shown

    Returns
    -------
    fig : plotly.graph_objects.Figure
        The figure with the boxplot and scatterplot
    """
    def boxplot(self, selected):
        df = self.data[self.data[self.label] == selected].copy()
        df['Month'] = df['dt'].dt.month
        df['Year'] = df['dt'].dt.year  
        df['Month_Name'] = df['dt'].dt.strftime('%B')  
        colors = px.colors.qualitative.Dark24
        fig = go.Figure()
        df.sort_values(by = 'Month', inplace = True)
        for month in range(1, 13):
            month_data = df[df['Month'] == month]
            month_temperatures = month_data['AverageTemperature']
            position = np.random.normal(month, 0.1, len(month_temperatures)) 
            month_name = month_data['Month_Name'].iloc[0]
            fig.add_box(x = month_data['Month'], 
                        y = month_temperatures, 
                        name = month_name, 
                        marker_color = colors[month-1], 
                        hovertemplate = 'Temperature: %{y}<br>Year: %{text}', 
                        text = month_data['Year']
                        )
            fig.add_scatter(x = position, 
                            y = month_temperatures, 
                            mode = 'markers', 
                            name = month_name, 
                            marker = dict(color = colors[month-1], size = 5, opacity = 0.3), 
                            showlegend = False, 
                            hovertemplate = 'Temperature: %{y}<br>Year: %{text}', 
                            text = month_data['Year']
                            )  
        fig.update_layout(xaxis = {'tickmode': 'array', 
                                 'tickvals':df['Month'].unique(), 
                                 'ticktext': df['Month_Name'].unique()}
                         )
        fig.update_traces(line = dict(width = 2))
        fig.update_xaxes(showgrid = False)
        fig.update_yaxes(showgrid = False, zeroline = False)
        return self._fig_layout(fig)

    """
    Show a map with the range of temperatures for each city/country for each year.

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe with the data to be shown
    min : float
        The minimum value for the range
    max : float
        The maximum value for the range

    Returns
    -------
    fig : plotly.graph_objects.Figure
        The figure with the map
    """
    @abstractmethod
    def _range_figure(self, df, min, max):
        pass

    """
    Show a map with the average temperatures for each city/country for each year.

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe with the data to be shown
    min : float
        The minimum value for the temperature
    max : float
        The maximum value for the temperature

    Returns
    -------
    fig : plotly.graph_objects.Figure
        The figure with the map
    """
    @abstractmethod
    def _temperature_figure(self, df, min, max):
        pass



"""
This class is used to visualize the data for cities. It inherits from the Visualize class and implements the following methods:
- _range_figure: a bubble map with the range of temperatures for each city for each year
- _temperature_figure: a bubble map with the average temperature for each city for each year
- heatmap: a heatmap with the average temperature of each city for each year
- show_locations: a map with all the cities in the dataset
- show_city: a map with the city of choice
"""
class City(Visualize):
    """
    Initialize the class with the data and calculate the yearly average temperature.
    See the Visualize class for more details.

    Parameters
    ----------
    data : pandas.DataFrame
        The original input data
    """
    def __init__(self, data):
        self.data = data.copy()
        group = ['City_Country', 'Year', 'Latitude', 'Longitude', 'Country']
        super().__init__('City_Country', group)

    #Implement abstract method
    def _range_figure(self, df, min, max):
        fig = px.scatter_mapbox(df, 
                                lat = 'Latitude', 
                                lon = 'Longitude', 
                                color = 'Range', 
                                size = 'Size', 
                                color_continuous_scale = px.colors.diverging.Portland, 
                                zoom = 1, 
                                animation_frame = 'Year', 
                                hover_name = 'City_Country', 
                                mapbox_style = 'open-street-map', 
                                range_color = (min, max), 
                                template = 'plotly_dark', 
                                hover_data = {
                                    'Range': True, 
                                    'City_Country': False, 
                                    'Year': False, 
                                    'Latitude': False, 
                                    'Longitude': False, 
                                    'YearlyAverage': False, 
                                    'Size': False}
                                )
        return self._fig_layout(fig)
    
    #Implement abstract method
    def _temperature_figure(self, df, min, max):
        fig = px.scatter_mapbox(df, 
                                lat = 'Latitude', 
                                lon = 'Longitude', 
                                color = 'YearlyAverage', 
                                hover_name = 'City_Country', 
                                size = 'Size', 
                                zoom = 1, 
                                animation_frame = 'Year', 
                                mapbox_style = 'open-street-map', 
                                template = 'plotly_dark', 
                                range_color = (min, max), 
                                color_continuous_scale = px.colors.diverging.Portland, 
                                hover_data = {
                                    'YearlyAverage': True, 
                                    'City_Country': False, 
                                    'Year': False, 
                                    'Latitude': False, 
                                    'Longitude': False, 
                                    'Size':False}
                                )
        return self._fig_layout(fig)
    
    """
    Show a heatmap with the average temperature of each city for each year.

    Returns
    -------
    fig : plotly.graph_objects.Figure
        The figure with the heatmap
    """
    def heatmap(self):
        fig = px.density_mapbox(self.data_year, 
                                lat = 'Latitude', 
                                lon = 'Longitude', 
                                z = 'YearlyAverage', 
                                radius = 15, 
                                center = dict(lat = 0, lon = 0), 
                                range_color = [], 
                                zoom = 0.4, 
                                animation_frame = 'Year', 
                                hover_name = 'City_Country', 
                                mapbox_style = 'open-street-map', 
                                animation_group = 'City_Country', 
                                color_continuous_scale = px.colors.diverging.Portland, opacity = 0.8, 
                                template = 'plotly_dark', 
                                hover_data = {
                                    'YearlyAverage': True, 
                                    'City_Country': False, 
                                    'Year': False, 
                                    'Latitude': False, 
                                    'Longitude': False}
                                )
        return self._fig_layout(fig)
    
    """
    Show a map with all the cities in the dataset.

    Returns
    -------
    fig : plotly.graph_objects.Figure
        The figure with the map
    """
    def show_locations(self):
        city = self.data.groupby('City').first().reset_index()
        fig = px.scatter_mapbox(city, 
                                lat = 'Latitude', 
                                lon = 'Longitude', 
                                hover_name = 'City', 
                                mapbox_style = 'open-street-map', 
                                zoom = 1
                                )
        fig.update_geos(
            visible = True, resolution = 50, 
            showcountries = True, countrycolor = 'RebeccaPurple'
        )
        return self._fig_layout(fig)
    
    """
    Show a map with the city of choice.

    Parameters
    ----------
    city_country : str
        The name of the city to be shown

    Returns
    -------
    fig : plotly.graph_objects.Figure
        The figure with the map
    """
    def show_city(self, city_country):
        filtered_data = self.data[self.data['City_Country'] == city_country].groupby(['City_Country', 'Latitude', 'Longitude']).first().reset_index()
        filtered_data['Size'] = [20]
        fig = px.scatter_mapbox(filtered_data, 
                                lat = 'Latitude', 
                                lon = 'Longitude', 
                                hover_name = 'City_Country', 
                                mapbox_style = 'open-street-map', 
                                zoom = 7, 
                                center = {'lat': filtered_data['Latitude'].iloc[0], 
                                        'lon': filtered_data['Longitude'].iloc[0]}, 
                                size = 'Size', 
                                hover_data = {
                                    'City_Country': False, 
                                    'Latitude': False, 
                                    'Longitude': False, 
                                    'Size': False}
                                )
        fig.update_geos(
            visible = True, 
            resolution = 50, 
            showcountries = True, 
            countrycolor = 'RebeccaPurple'
        )
        return  self._fig_layout(fig)
    



"""
This class is used to visualize the data for countries. It inherits from the Visualize class and implements the following methods:
- _range_figure: a bubble map with the range of temperatures for each country for each year
- _temperature_figure: a bubble map with the average temperature for each country for each year
- country_to_continent: a function to get the continent of a country
"""
class Country(Visualize):
    """
    Initialize the class with the data and calculate the yearly average temperature.
    Sets the continent for each country and removes countries with no continent.
    For some countries, the continent is not available in the pycountry_convert library, so it is manually set.
    See the Visualize class for more details.

    Parameters
    ----------
    path : str
        Path of the CSV file

    Attributes
    ----------
    data : pandas.DataFrame
        The original input data
    data_year : pandas.DataFrame
        Processed data with yearly averages and other statistics
    primaryColor : str
        Primary color for visualization theme
    backgroundColor : str
        Background color for visualization theme
    secondaryBackgroundColor : str
        Secondary background color for visualization theme
    textColor : str
        Text color for visualization theme
    """
    def __init__(self, path):
        self.data = pd.read_csv(path, index_col = False)
        self.data = self.data[self.data['Country'] != 'Denmark']
        self.data['Country'] = self.data['Country'].str.replace('Burma', 'Myanmar')
        self.data.loc[self.data['Country'] == 'Denmark (Europe)', 'Country'] = 'Denmark'
        self.data.loc[:, 'Continent'] = self.data['Country'].apply(self.country_to_continent)
        self.data.loc[(self.data['Country'] == "Congo (Democratic Republic Of The)") | (self.data['Country'] == "Côte D'Ivoire"), 'Continent'] = 'Africa'
        self.data.loc[self.data['Country'] == 'Bosnia And Herzegovina', 'Continent'] = 'Europe'
        self.data.dropna(subset = ['Continent'], inplace = True)
        self.data['dt'] = pd.to_datetime(self.data['dt'])
        self.data['Year'] = self.data['dt'].dt.year
        group = ['Country', 'Year', 'Continent']
        super().__init__('Country', group)

    """
    Get the continent of a country.

    Parameters
    ----------
    country_name : str
        The name of the country

    Returns
    -------
    country_continent_name : str
        The name of the continent
    """
    def country_to_continent(self, country_name):
        try:
            country_alpha2 = pc.country_name_to_country_alpha2(country_name)
            country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
            country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
        except:
            country_continent_name = None
        return country_continent_name

    #Implement abstract method
    def _temperature_figure(self, df, min, max):
        fig = px.choropleth(df, 
                            locations = 'Country', 
                            locationmode = 'country names', 
                            color = 'YearlyAverage', 
                            hover_name = 'Country', 
                            animation_frame = 'Year', 
                            range_color = [min, max], 
                            color_continuous_scale = px.colors.diverging.Portland, 
                            hover_data = {
                                'YearlyAverage': True, 
                                'Country': False, 
                                'Year': False}
                            )
        fig.update_layout(dragmode = False)
        return self._fig_layout(fig)
    
    #Implement abstract method
    def _range_figure(self, df, min, max):
        fig = px.choropleth(df, 
                            locations = 'Country', 
                            locationmode = 'country names', 
                            color = 'Range', 
                            color_continuous_scale = px.colors.diverging.Portland, 
                            animation_frame = 'Year', 
                            hover_name = 'Country', 
                            range_color = (min, max), 
                            hover_data = {
                                'Country': False, 
                                'Year': False, 
                                'YearlyAverage': False}
                            )
        fig.update_layout(dragmode = False)
        return self._fig_layout(fig)
    
