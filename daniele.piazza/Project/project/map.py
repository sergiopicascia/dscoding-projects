import pandas as pd
# install nbformat
import plotly.express as px
from dash import Dash, dcc, html
import pandas as pd
class Map:
    def __init__(self, data):
        self.data = data
        self.data['dt'] = pd.to_datetime(self.data['dt'])
        self.data['Year'] = self.data['dt'].dt.year


    def _create_app(self,fig):
        fig.update_layout(height=650, margin={"r":0,"t":0,"l":0,"b":0})
        app = Dash()
        app.layout = html.Div([
            dcc.Graph(figure=fig)
        ])
        app.run_server(debug=True, use_reloader=False) 


    def show_locations(self):
        self.data.groupby("City").first().reset_index()
        fig = px.scatter_mapbox(self.data,
                    lat='Latitude',
                    lon='Longitude',
                    hover_name="City",mapbox_style="carto-positron",zoom=1)
        fig.update_geos(
            visible=True, resolution=50,
            showcountries=True, countrycolor="RebeccaPurple"
        )
        self._create_app(fig)
        

    def heatmap(self):
        color = px.colors.cyclical.IceFire
        city_mean = self.data.groupby(['City','Country' ,'Year','Latitude','Longitude'])['AverageTemperature'].mean().reset_index()
        city_mean = city_mean.sort_values(by=['Year'])
        city_mean.dropna(inplace=True)
        fig = px.density_mapbox(city_mean, lat='Latitude', lon='Longitude', z='AverageTemperature', radius=30,
                                center=dict(lat=0, lon=0),range_color=[city_mean['AverageTemperature'].min()-10,city_mean['AverageTemperature'].max()], zoom=0.4, animation_frame = 'Year',hover_name="City",
                                mapbox_style="open-street-map", animation_group="City",color_continuous_scale=color,opacity=0.8,template='plotly_dark')
        self._create_app(fig)

    def bubble(self):
        result = self.data.groupby(['City','Country' ,'Year','Latitude','Longitude'])['AverageTemperature'].mean().reset_index()
        min_temp = result['AverageTemperature'].min()
        result['Size'] = result['AverageTemperature'] + abs(min_temp) + 5
        result = result.sort_values(by=['Year'])
        unique_cities = result['City'].unique()
        unique_years = result['Year'].unique()
        city_year = pd.MultiIndex.from_product([unique_cities, unique_years], names=['City', 'Year'])
        cartesian_product = pd.DataFrame(index=city_year).reset_index()
        result = cartesian_product.merge(result, on=['City', 'Year'], how='left').fillna({'Size': 0})
        result[['Country', 'Latitude', 'Longitude']] = result.groupby('City')[['Country', 'Latitude', 'Longitude']].transform('first') 
        result = result.sort_values(by=['Year'])
        map = px.scatter_geo(result, lat='Latitude',lon='Longitude', color="Country", hover_name="City", size="Size",size_max=10 ,opacity = 0.8, animation_frame="Year", projection="natural earth", title='Avarage Temperature Change')
        self._create_app(map)


'''
fig = px.scatter_mapbox(df,
lat='Latitude',
lon='Longitude',
hover_name="City",mapbox_style = 'open-street-map',zoom=1)
'''
