"""
Methods for plotting data using Plotly Express.
"""

import plotly.express as px


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
        fig.show()

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
        fig.show()

    def create_density_map(self):
        """
        Creates a density map using Plotly Express with a color scale.
        """
        df_cleaned = self.df.dropna(subset=['city_ascii', 'lat', 'lng', 'population'])

        fig = px.scatter_mapbox(df_cleaned,
                                text={'city_ascii': 'city name'},
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
        fig.show()

    def plot_top_countries(self, n=10):
        """
        Plot the top N countries with the most cities using Plotly Express.

        Parameters
        ----------
        n : int, optional
            Number of top countries to plot, by default 10.
        """
        if 'country' not in self.df.columns:
            raise ValueError("The DataFrame must contain the 'country' column.")

        cities_per_country = self.df['country'].value_counts().reset_index()
        cities_per_country.columns = ['country', 'city_count']

        top_countries = cities_per_country.head(n)

        fig = px.bar(top_countries, x='country', y='city_count', title=f'Top {n} Countries with the Most Cities',
                     labels={'city_count': 'Number of Cities', 'country': 'Country'},
                     template='plotly_dark')
        fig.show()

    def plot_shortest_path_map(self, shortest_path):
        """
        Create a map using Plotly Express with markers for each city in the shortest path.

        Parameters
        ----------
        shortest_path : list
            List of city names representing the shortest path.

        Returns
        -------
        None
        """
        if 'lat' not in self.df.columns or 'lng' not in self.df.columns or 'city_ascii' not in self.df.columns:
            raise ValueError("The DataFrame must contain the 'lat', 'lng', and 'city_ascii' columns.")

        locations = self.df[self.df['city_ascii'].isin(shortest_path)][['lat', 'lng', 'city_ascii']]

        fig = px.scatter_mapbox(locations,
                                lat='lat',
                                lon='lng',
                                text='city_ascii',
                                title='Shortest Path Map',
                                mapbox_style='carto-darkmatter',
                                zoom=3)  # Adjust the zoom level

        if not locations.empty:
            line_trace = px.line_mapbox(locations,
                                        lat='lat',
                                        lon='lng',
                                        line_group='city_ascii',
                                        color_discrete_sequence=['rgba(0, 0, 255, 0.7)']).update_traces(
                showlegend=False)

            for trace in line_trace.data:
                fig.add_trace(trace)

        fig.show()
