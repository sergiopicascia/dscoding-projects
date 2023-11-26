
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

class Mappe:
    def __init__(self, data):
        self.data = data
    
    # The following method creates a graph of the complete time series of yearly mean 
    # temperature values (AverageTemperature variable).
    # If the country dataset is used, the average yearly temperature trend based on country 
    # temperatures is displayed, whereas if the major dataset is used, the average yearly 
    # temperature trend calculated as the average of the temperatures of the country's major 
    # cities is displayed
    def GlobalYearlyTemperaturePlotter(self):
        self.data['Year'] = self.data['dt'].dt.year

        # calculate the average world temperature
        yearly_avg_temp = self.data.groupby('Year')['AverageTemperature'].mean().reset_index()

        fig = go.Figure()

        fig.add_trace(go.Scatter(x=yearly_avg_temp['Year'], y=yearly_avg_temp['AverageTemperature'], mode='lines'))

        fig.update_layout(title_text="Global Yearly Average Temperature", paper_bgcolor='rgba(0,0,0,0)')

        # range slider
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(count=5, label="5y", step="year", stepmode="backward"),
                        dict(count=10, label="10y", step="year", stepmode="backward"),
                        dict(count=20, label="20y", step="year", stepmode="backward"),
                        dict(count=50, label="50y", step="year", stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(visible=True),
                type="date"
            )
        )

        return fig
    
    # AVERAGE TEMPERATURE PLOTTERS
    # this method creates a map in which the average temperatures for a given period are plotted 
    # for each country, where the period consists of a number of years of your 
    # choice (via the period_interval argument)
    def AvgTemp_Period_country(self, period_interval):
        # with the following operation, each year is assigned to the period in which it falls 
        # (observe that the interval 'Period' takes the name of the lower bound)
        self.data['Period'] = (self.data['dt'].dt.year - self.data['dt'].dt.year.min()) // period_interval * period_interval + self.data['dt'].dt.year.min() 
        
        # the average temperatures of each country for each period are calculated, 
        # and then the periods are sorted in temporal order
        period_avg_temp = self.data.groupby(['Country', 'Period'])['AverageTemperature'].mean().reset_index()
        period_avg_temp.sort_values(by='Period', inplace=True)

        # we create the minimum and maximum value that the colour scale must take, so that it 
        # remains constant for each period, so that it is comparable
        color_scale_min = period_avg_temp['AverageTemperature'].min()
        color_scale_max = period_avg_temp['AverageTemperature'].max()
        
        fig = px.choropleth(
            period_avg_temp,
            locations='Country',
            locationmode='country names',
            color='AverageTemperature',
            animation_frame='Period',
            labels={'AverageTemperature': 'Average Temperature', 'Period': 'Period'},
            color_continuous_scale='temps',
            range_color=[color_scale_min, color_scale_max] 
        )
        fig.update_geos(projection_type="natural earth", showocean=True, oceancolor="#a8d8ff")
        fig.update_layout(width=1200, height=700, margin={"r": 0, "t": 0, "l": 0, "b": 0}, geo=dict(bgcolor='rgba(0,0,0,0)'))
        return fig
    
    
    # The following method does the same thing, but for a dataset containing cities, 
    # for which latitude and longitude must therefore be used
    def AvgTemp_Period_City(self, period_interval):
        self.data['Period'] = (self.data['dt'].dt.year - self.data['dt'].dt.year.min()) // period_interval * period_interval + self.data['dt'].dt.year.min()
        period_avg_temp = self.data.groupby(['City','Latitude','Longitude', 'Period'])['AverageTemperature'].mean().reset_index()
        period_avg_temp.sort_values(by='Period', inplace=True)
        color_scale_min = period_avg_temp['AverageTemperature'].min()
        color_scale_max = period_avg_temp['AverageTemperature'].max()

        fig = px.scatter_geo(
            period_avg_temp,
            lat='Latitude',
            lon='Longitude',
            color='AverageTemperature',
            animation_frame='Period',
            labels={'AverageTemperature': 'Average Temperature', 'Period': 'Period'},
            color_continuous_scale='temps',
            range_color=[color_scale_min, color_scale_max],
            title='Average Temperature by City (Periods)'
        )

        fig.update_geos(projection_type="natural earth", showocean=True, oceancolor="#a8d8ff")
        fig.update_layout(width=1200, height=700, margin={"r": 0, "t": 0, "l": 0, "b": 0}, geo=dict(bgcolor='rgba(0,0,0,0)'))
        return fig
    

    # TEMPERATURE VARIATION
    # This method calculates the change in average temperature for each period (for each country) 
    # compared to the previous period, with the intention of emphasising climate change 
    # (the increase in average temperatures)
    def TempVar_Period_country(self, period_interval):
        self.data['Period'] = (self.data['dt'].dt.year - self.data['dt'].dt.year.min()) // period_interval * period_interval + self.data['dt'].dt.year.min()
        period_avg_temp = self.data.groupby(['Country', 'Period'])['AverageTemperature'].mean().reset_index()
        period_avg_temp.sort_values(by='Period', inplace=True)
        period_avg_temp['TemperatureVariation'] = period_avg_temp.groupby('Country')['AverageTemperature'].diff()
        color_scale_min = period_avg_temp['TemperatureVariation'].min()
        color_scale_max = period_avg_temp['TemperatureVariation'].max()
        
        fig = px.choropleth(
            period_avg_temp,
            locations='Country',
            locationmode='country names',
            color='TemperatureVariation',
            animation_frame='Period',
            labels={'TemperatureVariation': 'Temperature Variation', 'Period': 'Period'},
            color_continuous_scale='temps',
            range_color=[color_scale_min, color_scale_max] 
        )
        fig.update_geos(projection_type="natural earth", showocean=True, oceancolor="#a8d8ff")
        fig.update_layout(width=1200, height=700, margin={"r": 0, "t": 0, "l": 0, "b": 0}, geo=dict(bgcolor='rgba(0,0,0,0)'))
        return fig
    
    # this method does the same as the previous one but for cities
    def TempVar_Period_City(self, period_interval):
        self.data['Period'] = (self.data['dt'].dt.year - self.data['dt'].dt.year.min()) // period_interval * period_interval + self.data['dt'].dt.year.min()

        period_avg_temp = self.data.groupby(['City','Latitude','Longitude', 'Period'])['AverageTemperature'].mean().reset_index()
        period_avg_temp.sort_values(by='Period', inplace=True)
        period_avg_temp['TemperatureVariation'] = period_avg_temp.groupby('City')['AverageTemperature'].diff()
        

        color_scale_min = period_avg_temp['TemperatureVariation'].min()
        color_scale_max = period_avg_temp['TemperatureVariation'].max()

        fig = px.scatter_geo(
            period_avg_temp,
            lat='Latitude',
            lon='Longitude',
            color='TemperatureVariation',
            animation_frame='Period',
            labels={'TemperatureVariation': 'Temperature Variation', 'Period': 'Period'},
            color_continuous_scale='temps',
            range_color=[color_scale_min, color_scale_max]
        )

        fig.update_geos(projection_type="natural earth", showocean=True, oceancolor="#a8d8ff")
        fig.update_layout(width=1200, height=700, margin={"r": 0, "t": 0, "l": 0, "b": 0}, geo=dict(bgcolor='rgba(0,0,0,0)'))
        return fig
    
    # This method calculates the maximum temperature variation occurring within a year for a country
    def TempVar_Year_Country(self):
        # for each country for each year, the difference between the maximum recorded 
        # value (month) and the minimum value is calculated:
        yearly_temp_variation = self.data.groupby(['Country', self.data['dt'].dt.year])['AverageTemperature'].apply(lambda x: x.max() - x.min()).reset_index()
        yearly_temp_variation.sort_values(by="dt", inplace=True)
        
        fig = px.choropleth(
            yearly_temp_variation,
            locations='Country',
            locationmode='country names',
            color='AverageTemperature',
            animation_frame='dt',
            labels={'AverageTemperature': 'Temperature Variation', 'dt': 'Year'},
            color_continuous_scale='temps'
        )
        fig.update_geos(projection_type="natural earth", showocean=True, oceancolor="#a8d8ff")
        fig.update_layout(width=1200, height=700, margin={"r": 0, "t": 0, "l": 0, "b": 0}, geo=dict(bgcolor='rgba(0,0,0,0)'))
        return fig
    
    # this method does the same as the previous one but for cities
    def TempVar_Year_City(self):
        yearly_temp_variation = self.data.groupby(['City','Latitude','Longitude', self.data['dt'].dt.year])['AverageTemperature'].apply(lambda x: x.max() - x.min()).reset_index()
        yearly_temp_variation.sort_values(by="dt", inplace=True)

        fig = px.scatter_geo(
            yearly_temp_variation,
            lat='Latitude',
            lon='Longitude',
            color='AverageTemperature',
            animation_frame='dt',
            labels={'AverageTemperature': 'Temperature Variation', 'dt': 'Year'},
            color_continuous_scale='temps',
        )

        fig.update_geos(projection_type="natural earth", showocean=True, oceancolor="#a8d8ff")
        fig.update_layout(width=1200, height=700, margin={"r": 0, "t": 0, "l": 0, "b": 0}, geo=dict(bgcolor='rgba(0,0,0,0)'))
        return fig

    