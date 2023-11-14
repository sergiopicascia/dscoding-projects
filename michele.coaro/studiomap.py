import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

temp = pd.read_csv("DFtoImport.csv")
u_temp = temp.drop_duplicates(subset='City', keep='first')
token = open('token.txt').read() # you will need your own toke
temp = temp.dropna()
temp.sort_values(by=['dt'], inplace=True)
temp['new_size'] = temp['AverageTemperature'] + abs(temp['AverageTemperature'].min())  + 2
fig = px.scatter_mapbox(temp, lat='Latitude',
                        lon='Longitude',
                        animation_frame='dt',
                        animation_group='City',
                        center=dict(lat=0, lon=180),
                        zoom=1,
                        size= 'new_size',
                        mapbox_style="stamen-terrain",
                        hover_name= temp['City'],
                        hover_data = {'dt' : False,
                                       'City' : False,
                                        'AverageTemperature' : True,
                                        'Latitude' : False,
                                        'Longitude' : False,
                                        'new_size' : False},
                        title = 'Average Temperature in Global Major Cities',
                        color_continuous_scale=px.colors.cyclical.IceFire,color='AverageTemperature',
                        range_color=(temp['AverageTemperature'].min(), temp['AverageTemperature'].max()))
fig.update_layout(mapbox_style="dark", mapbox_accesstoken = token)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.write_html("attempt.html")
