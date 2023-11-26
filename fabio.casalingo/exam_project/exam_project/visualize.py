import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import folium


class MapHandler:
    def __init__(self, dataset_path='C:/Uni/Coding/python/worldcities.xlsx'):
        self.dataset = pd.read_excel(dataset_path)

    def map_2d(self, visit, flag):
        """
        Show with a 2d map the path of the input travel path.

        Parameters
        ----------
        visit: list[]
            The IDs associated to the cities visited in the travel path.

        Returns
        -------
        map: folium.folium.Map
            A folium map containing the graphical travel path.
        """
        zoom = self.dataset[(self.dataset['id'] == visit[0])][['lat', 'lng']].values[0]
        map = folium.Map(location=zoom, zoom_start=2)
        icon_url = 'C:/Uni/Coding/python/exam_project/exam_project/custom_marker.png'
        folium.TileLayer('cartodbdark_matter').add_to(map)
        for i in range(len(visit)):
            s = self.dataset[(self.dataset['id'] == visit[i])][['lat', 'lng']].values[0]
            folium.Marker(s, icon=folium.CustomIcon(icon_image=icon_url, icon_size=(25, 25)),
                          popup=self.dataset[(self.dataset['id'] == visit[i])][['city']].values[0]).add_to(map)
        locations = [(self.dataset.loc[self.dataset['id'] == visit[j], ['lat', 'lng']].values[0]) for j in
                     range(len(visit))]
        if flag:
            line = folium.PolyLine(locations=locations,
                                   color='orange',
                                   weight=6,
                                   opacity=0.3
                                   )
            line.add_to(map)
        map.save('mappa.html')
        return map

    def map_3d(self, visit):
        """
        Show with a 3d map the path of the input travel path.

        Parameters
        ----------
        visit: list[]
            The IDs associated to the cities visited in the travel path.

        Returns
        -------
        fig: plotly.graph_objs.Figure
            A 3d map that show the travel path.
        """
        coordinates = [self.dataset.loc[self.dataset['id'] == city_id, ['lat', 'lng', 'city']].iloc[0] for city_id in
                       visit]

        path = go.Scattergeo(
            lon=[coord['lng'] for coord in coordinates],
            lat=[coord['lat'] for coord in coordinates],
            mode="lines+markers",
            line=dict(width=2, color="black"),
            marker=dict(size=8,
                        color=["orange" if i == 0 else "red" if i == len(coordinates) - 1 else " #ffb84d" for i in
                               range(len(coordinates))]),
            text=[f"City: {coord['city']}" for coord in coordinates]
        )

        layout = go.Layout(
            geo=dict(
                showland=True,
                showocean=True,
                landcolor="#267326",
                countrycolor="rgb(0, 0, 0)",
                oceancolor="#80bfff",
                projection=dict(
                    type="orthographic"
                )
            )
        )

        fig = go.Figure(data=[path], layout=layout)

        fig.update_layout(
            title_text='Path on 3D Globe',
            title_x=0.5,
            title_font=dict(size=20),
            title_xanchor='center',
            plot_bgcolor="#dddddd",
            paper_bgcolor="#dddddd"
        )

        fig.update_layout(height=800, margin={"r": 0, "t": 0, "l": 0, "b": 0})
        return fig

    def population(self):
        """
        Generate a 3D choropleth map illustrating the population distribution of visited cities.

        Returns
        -------
        fig: plotly.graph_objs.Figure
            A 3D choropleth map displaying the population distribution of visited cities.
        """
        df = self.dataset.groupby('iso3')['population'].sum().reset_index()
        fig = px.choropleth(df,
                            locations='iso3',
                            color='population',
                            hover_name='iso3',
                            projection='natural earth',
                            range_color=(0, 155000000),
                            title='Population distribution',
                            color_continuous_scale='Viridis')
        fig.update_layout(
            plot_bgcolor="#dddddd",
            paper_bgcolor="#dddddd"
        )

        return fig
