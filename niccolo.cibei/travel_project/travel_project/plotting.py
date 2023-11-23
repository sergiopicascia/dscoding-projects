"""
Methods for plotting data using Plotly Express.
"""

import plotly.express as px
import pandas as pd
import plotly.graph_objects as go


class Plotting:
    def __init__(self, df):
        """
        Initialize the Plotting class.

        Parameters
        ----------
        df : pd.DataFrame
            The DataFrame containing city information.
        """
        self.df = df

    def plot_population_by_country(self):
        """
        Divides the population by country and plots the result using Plotly Express.

        Returns
        -------
        Plot of the population for the top 10 most populous countries.
        """
        if 'population' not in self.df.columns or 'country' not in self.df.columns:
            raise ValueError("The DataFrame must contain the columns 'population' e 'country'.")

        population_by_country = self.df.groupby('country')['population'].sum().reset_index()

        population_by_country = population_by_country.sort_values(by='population', ascending=False)[:10]

        fig = px.bar(population_by_country, x='country', y='population', title='Population per country',
                     labels={'population': 'Population', 'country': 'Country'},
                     template='plotly_dark')
        return fig

    def plot_population_by_continent(self):
        """
        Divides the population by continent and plots the result using Plotly Express.

        Returns
        -------
        Plot of the population by continent.
        """

        population_by_continent = self.df.groupby('continent')['population'].sum().reset_index()

        population_by_continent = population_by_continent.sort_values(by='population', ascending=False)

        fig = px.bar(population_by_continent, x='continent', y='population', title='Population per continent',
                     labels={'population': 'Population', 'continent': 'Continent'},
                     template='plotly_dark')
        return fig

    def plot_density_map(self):
        """
        Creates a density map using Plotly Express with a color scale.

        Returns
        -------
        fig
            Plotly Express figure representing the density map.
        """

        self.df['text_info'] = self.df['city_ascii'] + '<br>Population: ' + self.df['population'].astype(str)

        fig = px.scatter_mapbox(self.df,
                                text='text_info',  # Use the new 'text_info' column
                                lat='lat',
                                lon='lng',
                                size='population',
                                color='population',
                                color_continuous_scale=px.colors.sequential.Viridis,
                                size_max=50,
                                zoom=2,
                                title='Density map',
                                labels={'population': 'Population'},
                                template='plotly_dark')

        fig.update_layout(mapbox_style="carto-darkmatter")
        return fig

    def plot_top_countries(self, n=10):
        """
        Plot the top N countries with the most cities using Plotly Express.

        Parameters
        ----------
        n : int, optional
            Number of top countries to plot, by default 10.

        Returns
        -------
        fig
            Plotly Express figure representing the bar chart.
        """
        if 'country' not in self.df.columns:
            raise ValueError("The DataFrame must contain the 'country' column.")

        cities_per_country = self.df['country'].value_counts().reset_index()
        cities_per_country.columns = ['country', 'city_count']

        top_countries = cities_per_country.head(n)

        fig = px.bar(top_countries, x='country', y='city_count', title=f'Top {n} Countries with the Most Cities',
                     labels={'city_count': 'Number of Cities', 'country': 'Country'},
                     template='plotly_dark')
        return fig

    def map_3d(self, cities_path):
        """
        Generates a 3D globe map showing a path of cities.

        Parameters
        ----------
        cities_path : list
            List of city IDs representing the visit order.

        Returns
        -------
        fig
            Plotly figure representing the 3D globe map with the specified path.
        """
        if cities_path is None:
            raise ValueError("The visit list is empty.")
        else:
            coordinates = [self.df.loc[self.df['city_ascii'] == city_id, ['lat', 'lng', 'city_ascii']].iloc[0] for
                           city_id in cities_path]

            path = go.Scattergeo(
                lon=[coord['lng'] for coord in coordinates],
                lat=[coord['lat'] for coord in coordinates],
                mode="lines+markers",
                line=dict(width=2, color="black"),
                marker=dict(
                    size=15,
                    color=["black" if i == 0 else "red" if i == len(coordinates) - 1 else "orange" for i in
                           range(len(coordinates))]
                ),
                text=[f"City: {coord['city_ascii']}" for coord in coordinates]
            )

            layout = go.Layout(
                geo=dict(
                    showframe=False,
                    showcoastlines=False,
                    showcountries=True,
                    showland=True,
                    showocean=True,
                    landcolor="forestgreen",
                    countrycolor="rgb(204, 204, 204)",
                    countrywidth=0.5,
                    oceancolor="lightblue",
                    projection=dict(
                        type="orthographic",
                        scale=2
                    )
                )
            )

            fig = go.Figure(data=[path], layout=layout)

            fig.update_layout(height=900, margin={"r": 0, "t": 0, "l": 0, "b": 0})

            return fig
