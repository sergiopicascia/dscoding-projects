import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

class TempVar:
    def __init__(self, data):
        self.data = data
        self.variation_df = None
    

    # this method creates a dataset containing for each city, for each year, the maximum 
    # temperature, the minimum temperature, the average temperature and the temperature 
    # variation (max - min)
    def TemperatureVariationCalculator(self):
        # empty list to store results
        results = []

        for city in self.data['City'].unique():
            city_data = self.data[self.data['City'] == city]

            for year in city_data['dt'].dt.year.unique():
                year_data = city_data[city_data['dt'].dt.year == year]

                
                max_temp = year_data['AverageTemperature'].max()
                min_temp = year_data['AverageTemperature'].min()
                variation = max_temp - min_temp
                avg_temp = year_data['AverageTemperature'].mean()

                # filling the list
                results.append({
                    'City': city,
                    'Year': year,
                    'Temp Max': max_temp,
                    'Temp Min': min_temp,
                    'Avg Temp': avg_temp,
                    'TemperatureVariation': variation
                })

        # convert the list to dataframe
        variation_df = pd.DataFrame(results)

        # saves the dataframe as an attribute of the class
        self.variation_df = variation_df

        return variation_df
    

    # this method does the same thing me for countries 
    # (another method was created specifically to specify the name of variables)
    def CountryTemperatureVariationCalculator(self):
        results = []

        for country in self.data['Country'].unique():
            country_data = self.data[self.data['Country'] == country]

            for year in country_data['dt'].dt.year.unique():
                year_data = country_data[country_data['dt'].dt.year == year]

                max_temp = year_data['AverageTemperature'].max()
                min_temp = year_data['AverageTemperature'].min()
                variation = max_temp - min_temp
                avg_temp = year_data['AverageTemperature'].mean()

                results.append({
                    'Country': country,
                    'Year': year,
                    'Temp Max': max_temp,
                    'Temp Min': min_temp,
                    'Avg Temp': avg_temp,
                    'TemperatureVariation': variation
                })

        variation_df = pd.DataFrame(results)

        self.variation_df = variation_df

        return variation_df
    
    # this method creates a graph per variation_df (after being filtered by country/city).
    # A time series of data is created for the specific chosen city/country showing 
    # the maximum, minimum and average temperature
    def TemperatureSeriesPlotter(self):
        self.data.sort_values(by='Year', inplace=True)

        trace_max = go.Scatter(x=self.data['Year'], y=self.data['Temp Max'], mode='lines', name='Max Temperature', line=dict(color='red'))
        trace_min = go.Scatter(x=self.data['Year'], y=self.data['Temp Min'], mode='lines', name='Min Temperature', line=dict(color='blue'))
        trace_avg = go.Scatter(x=self.data['Year'], y=self.data['Avg Temp'], mode='lines', name='Avg Temperature', line=dict(color='green'))

        fill_x = self.data['Year'].tolist() + self.data['Year'].tolist()[::-1]
        fill_y = self.data['Temp Max'].tolist() + self.data['Temp Min'].tolist()[::-1]


        trace_fill = go.Scatter(
            x=fill_x,
            y=fill_y,
            mode = 'lines',
            name='Temperature Range',
            fill='toself',
            fillcolor='rgba(0,100,80,0.2)',
            line=dict(color='rgba(255,255,255,0)')
        )

        fig = go.Figure()
        fig.add_trace(trace_fill)
        fig.add_trace(trace_max)
        fig.add_trace(trace_min)
        fig.add_trace(trace_avg)

        fig.update_layout(
            title='Temperature Time Series',
            xaxis_title='Year',
            yaxis_title='Temperature',
            showlegend=True
        )
        fig.update_layout(width=1300, height=600)
        return fig
    
    # this method allows you to view the monthly time series of several countries/cities 
    # of your choice
    def GlobalMonthlyTemperaturePlotter(self, selection, is_country=True):
        if is_country:
            selected_data = self.data[self.data['Country'].isin(selection)]
        else:
            selected_data = self.data[self.data['City'].isin(selection)]

        selected_data['Month'] = selected_data['dt'].dt.month
        selected_data['Year'] = selected_data['dt'].dt.year

        fig = go.Figure()

        color_palette = px.colors.qualitative.Set1

        for i, item in enumerate(selection):
            monthly_avg_temp = selected_data[selected_data['Country' if is_country else 'City'] == item].groupby(['Year', 'Month'])['AverageTemperature'].mean().reset_index()
            monthly_avg_temp['Date'] = pd.to_datetime(monthly_avg_temp[['Year', 'Month']].assign(DAY=1))
            fig.add_trace(go.Scatter(x=monthly_avg_temp['Date'], y=monthly_avg_temp['AverageTemperature'], mode='lines', name=item, line=dict(color=color_palette[i])))

        fig.update_layout(
            title_text="Global Monthly Average Temperature",
            paper_bgcolor='rgba(0,0,0,0)'
        )

        # range slider
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=3, label="3m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(count=2, label="2y", step="year", stepmode="backward"),
                        dict(count=3, label="3y", step="year", stepmode="backward"),
                        dict(count=10, label="10y", step="year", stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(visible=True),
                type="date"
            )
        
        )
        fig.update_layout(width=1300, height=600)

        return fig