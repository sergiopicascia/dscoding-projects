import pandas as pd
import plotly.express as px
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import numpy as np
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler
import toml 

class Visualize:
    def __init__(self, data):
        self.data = data
        self.data['dt'] = pd.to_datetime(self.data['dt'])
        self.data['Year'] = self.data['dt'].dt.year
        self.data.dropna(subset=['AverageTemperature'], inplace=True)
        self.data = self.data.sort_values(by='dt')
        self.data_year = self.data.groupby(['City_Country', 'Year', 'Latitude', 'Longitude']).agg(
            YearlyAverage=('AverageTemperature', 'mean'),
            AvailableMonths=('AverageTemperature', 'count'),
            MinTemp=('AverageTemperature', 'min'),
            MaxTemp=('AverageTemperature', 'max')).reset_index()
        self.data_year['YearlyAverage'] = self.data_year['YearlyAverage'].round(2)
        self.clean_data()
        self.calculate_annual_uncertainty()
        self.get_theme() 

    def calculate_annual_uncertainty(self):
        annual_uncertainty = self.data.groupby(["Year", 'City_Country'])['AverageTemperatureUncertainty'].apply(lambda x: (x ** 2).sum() ** 0.5)
        self.data_year = pd.merge(self.data_year, annual_uncertainty.reset_index(name='AverageTemperatureUncertainty'), on=['Year', 'City_Country'])

    def clean_data(self):
        self.data.sort_values(by='dt', inplace=True)
        complete_years = self.data_year[self.data_year['AvailableMonths'] == 12][['City_Country', 'Year']]
        self.data = pd.merge(self.data, complete_years, how='inner', on=['City_Country', 'Year'])
        self.data_year = self.data_year[self.data_year['AvailableMonths'] == 12]
        self.data_year.sort_values(by='Year', inplace=True)
        self.data_year.drop(columns=['AvailableMonths'], inplace=True)

    def get_theme(self):
        config = toml.load('.streamlit/config.toml')
        self.primaryColor = config['theme']['primaryColor']
        self.backgroundColor = config['theme']['backgroundColor']
        self.secondaryBackgroundColor = config['theme']['secondaryBackgroundColor']
        self.textColor = config['theme']['textColor']

    def fig_layout(self,fig):
        fig.update_layout({'paper_bgcolor': self.backgroundColor},
                          width=1300,
                          height=800,
                          margin={"r":0,"t":0,"l":0,"b":0},
                          font=dict(color=self.primaryColor),
                          updatemenus=[dict(bgcolor=self.secondaryBackgroundColor)]
                          )
        fig.update_mapboxes(bounds_east=180, bounds_west=-180, bounds_north=90, bounds_south=-70)
        return fig
    
    def show_locations(self):
        city = self.data.groupby("City").first().reset_index()
        fig = px.scatter_mapbox(city,
                    lat='Latitude',
                    lon='Longitude',
                    hover_name="City",mapbox_style="open-street-map",zoom=1)
        fig.update_geos(
            visible=True, resolution=50,
            showcountries=True, countrycolor="RebeccaPurple"
        )
        return self.fig_layout(fig,'General Map')
    
    def show_city(self, city_country):
        filtered_data = self.data[self.data['City_Country'] == city_country].groupby(['City_Country', 'Latitude', 'Longitude']).first().reset_index()
        filtered_data['Size'] = [20]
        fig = px.scatter_mapbox(filtered_data,
                                lat='Latitude',
                                lon='Longitude',
                                hover_name="City_Country",
                                mapbox_style="open-street-map",
                                zoom=7,
                                center={"lat": filtered_data['Latitude'].iloc[0], "lon": filtered_data['Longitude'].iloc[0]},
                                size="Size",
                                hover_data={
                                    "City_Country": False,
                                    "Latitude": False,
                                    "Longitude": False,
                                    "Size": False
                                })
        fig.update_geos(
            visible=True,
            resolution=50,
            showcountries=True,
            countrycolor="RebeccaPurple"
        )
        return  self.fig_layout(fig)
    

    def heatmap(self):
        fig = px.density_mapbox(self.data_year,
                                lat='Latitude',
                                lon='Longitude',
                                z='YearlyAverage',
                                radius=5,
                                center=dict(lat=0, lon=0),
                                range_color=[],
                                zoom=0.4,
                                animation_frame = 'Year',
                                hover_name="City_Country",
                                mapbox_style="open-street-map", 
                                animation_group="City_Country",
                                color_continuous_scale=px.colors.diverging.Portland,opacity=0.8,template='plotly_dark',
                                hover_data={
                                    "YearlyAverage": True,
                                    "City_Country": False,
                                    "Year": False,
                                    "Latitude": False,
                                    "Longitude": False,
                                })
        return self.fig_layout(fig)

    def line_year(self,city_country,year):
        city_data = self.data[(self.data['City_Country'] == city_country) & (self.data['Year'] == year)]
        fig = px.line(city_data, x='dt', y='AverageTemperature', markers=True, color_discrete_sequence=[self.primaryColor])
        return self.fig_layout(fig)

    def line(self, city_country):
        city_data = self.data_year[(self.data_year['City_Country'] == city_country)]
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=city_data['Year'],
            y=city_data['YearlyAverage'] - city_data['AverageTemperatureUncertainty'],
            marker=dict(color=self.primaryColor),
            line=dict(width=0),
            mode='lines',
            showlegend=False,
            name='Lower bound'
        ))
        fig.add_trace(go.Scatter(
            x=city_data['Year'],
            y=city_data['YearlyAverage'] + city_data['AverageTemperatureUncertainty'],
            mode='lines',
            marker=dict(color=self.primaryColor),
            line=dict(width=0),
            fill='tonexty',
            fillcolor=self.secondaryBackgroundColor,
            showlegend=False,
            name='Upper bound'
        ))
        fig.add_trace(go.Scatter(
            x=city_data['Year'],
            y=city_data['YearlyAverage'],
            mode='lines',
            name='Average Temperature',
            line=dict(color=self.primaryColor)
        ))
        return self.fig_layout(fig)
        
    def bubble_range(self, n=None):
        df = self.data_year.copy()
        df["Range"] = (df['MaxTemp'] - df['MinTemp']).round(2)
        scaler = MinMaxScaler()
        df["Size"] =  scaler.fit_transform(df[['Range']])
        if n is not None:
            df = df.groupby('Year').apply(lambda x: x.nlargest(n, 'Range')).reset_index(drop=True)
        min = df['Range'].min()
        max = df['Range'].max()
        fig = px.scatter_mapbox(df,
                                lat='Latitude',
                                lon='Longitude',
                                color="Range",
                                size="Size",
                                color_continuous_scale=px.colors.diverging.Portland,
                                zoom=1,
                                animation_frame='Year',
                                hover_name="City_Country",
                                mapbox_style="open-street-map", 
                                range_color=(min, max),
                                template='plotly_dark',
                                hover_data={
                                    "Range": True,
                                    "City_Country": False,
                                    "Year": False,
                                    "Latitude": False,
                                    "Longitude": False,
                                    "YearlyAverage": False,
                                    "Size": False
                                })
        fig.update_mapboxes(bounds_east=180, bounds_west=-180, bounds_north=90, bounds_south=-70)
        return self.fig_layout(fig)

    def bubble(self,n=None):
        df = self.data_year.copy()
        min = df['YearlyAverage'].min()
        max = df['YearlyAverage'].max()
        if n is not None:
            df = df.groupby('Year').apply(lambda x: x.nlargest(n, 'YearlyAverage')).reset_index(drop=True)
        bubble_counts = df['Year'].value_counts()
        df['Size'] = df['Year'].apply(lambda x: 1000 / np.log((bubble_counts[x]) + 1))
        fig = px.scatter_mapbox(df,
                                lat='Latitude',
                                lon='Longitude',
                                color="YearlyAverage",
                                hover_name="City_Country",
                                size="Size",
                                zoom=1,
                                animation_frame="Year",
                                mapbox_style="open-street-map",
                                range_color=(min,max),
                                color_continuous_scale=px.colors.diverging.Portland,
                                template='plotly_dark',
                                hover_data={
                                    "YearlyAverage": True,
                                    "City_Country": False,
                                    "Year": False,
                                    "Latitude": False,
                                    "Longitude": False,
                                    "Size":False
                                })
        return self.fig_layout(fig)
    
    def predict_city_temperature(self,city_country):
        city_data = self.data_year[(self.data_year['City_Country'] == city_country)]
        years = city_data['Year'].values.reshape(-1, 1)
        temperatures = city_data['YearlyAverage'].values
        poly_reg = PolynomialFeatures(degree=4)
        years_poly = poly_reg.fit_transform(years)
        lin_reg_poly = LinearRegression()
        lin_reg_poly.fit(years_poly, temperatures)
        range = np.arange(years.max(), years.max()+50)
        future_years = range.reshape(-1, 1)
        future_years_poly = poly_reg.transform(future_years)
        predicted_temperatures = lin_reg_poly.predict(poly_reg.transform(years))
        future_predicted_temperatures = lin_reg_poly.predict(future_years_poly)
        fig = px.scatter(x=years.flatten(),
                         y=temperatures,
                         color_discrete_sequence=[self.secondaryBackgroundColor],
                         labels={'x': 'Year', 'y': 'Temperature'}
                         )
        fig.add_scatter(x=years.flatten(),
                        y=predicted_temperatures,
                        mode='lines',
                        line=dict(color=self.primaryColor),
                        name='Polynomial Regression'
                        )
        fig.add_scatter(x=range,
                        y=future_predicted_temperatures,
                        mode='lines', 
                        line=dict(color='red'),
                        name='Future Prediction'
                        )
        fig.update_layout(xaxis_title='Year', yaxis_title='Temperature')
        return self.fig_layout(fig)
    
    def additional_statistics(self):
        city_stats = self.data_year.groupby('City_Country').agg(
            AverageTemperature=('YearlyAverage', 'mean'),
            MinTemperature=('YearlyAverage', 'min'),
            MaxTemperature=('YearlyAverage', 'max'),
            Uncertainty=('AverageTemperatureUncertainty','mean')).round(2)
        return city_stats
    
    def boxplot(self,city_country):
        df = self.data[self.data['City_Country'] == city_country]
        df['Month'] = df['dt'].dt.month
        df['Year'] = df['dt'].dt.year  
        df['Month_Name'] = df['dt'].dt.strftime('%B')  
        colors = px.colors.qualitative.Dark24
        fig = go.Figure()
        df.sort_values(by='Month', inplace=True)
        for month in range(1, 13):
            month_data = df[df['Month'] == month]
            month_temperatures = month_data['AverageTemperature']
            position = np.random.normal(month, 0.1, len(month_temperatures)) 
            month_name = month_data['Month_Name'].iloc[0]
            fig.add_box(x=month_data['Month'], 
                        y=month_temperatures, 
                        name=month_name, 
                        marker_color=colors[month-1], 
                        hovertemplate='Temperature: %{y}<br>Year: %{text}', 
                        text=month_data['Year']
                        )
            fig.add_scatter(x=position, 
                            y=month_temperatures, 
                            mode='markers', 
                            name=month_name, 
                            marker=dict(color=colors[month-1], size=5, opacity=0.3),
                            showlegend=False,
                            hovertemplate='Temperature: %{y}<br>Year: %{text}', 
                            text=month_data['Year']
                            )  
        fig.update_layout(xaxis={'tickmode': 'array',
                                 'tickvals':df['Month'].unique(),
                                 'ticktext': df['Month_Name'].unique()})
        fig.update_traces(line=dict(width=2))
        return self.fig_layout(fig)

    