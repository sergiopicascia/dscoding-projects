import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import kurtosis, skew, norm
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


class Statistiche:
    def __init__(self, data):
        self.data = data
    
    # this method reports the descriptive statistics of the dataset
    def descriptive_stats(self):
        return self.data[['dt', 'AverageTemperature']].describe()

    # this method plots the mean temperature histogram against the normal distribution, 
    # and calculates the symmetry and kurtosis
    def Distribution(self, column):
        plt.figure(figsize=(12, 6), facecolor ='none')

        # histogram
        plt.hist(self.data[column], bins=40, color='violet', edgecolor='black', density=True, alpha=0.7)

        # adding the normal distribution
        xmin, xmax = plt.xlim()
        x = np.linspace(xmin, xmax, 100)
        p = norm.pdf(x, self.data[column].mean(), self.data[column].std())
        plt.plot(x, p, 'k', linewidth=2)

        plt.title(f'Distribution of {column}')
        plt.xlabel(column)
        plt.ylabel('Frequency')

        # skewness and kurtosis
        skewness = skew(self.data[column].dropna())
        kurt = kurtosis(self.data[column].dropna())

        plt.axvline(self.data[column].mean(), color='black', linestyle='dashed', linewidth=2,
                    label=f'Mean ({self.data[column].mean():.2f})\nSkewness: {skewness:.2f}\nKurtosis: {kurt:.2f}')

        plt.legend()

        return plt
    
    # this method creates a graph showing the frequency distribution of temperatures for a 
    # country/city/state of  choice
    def plot_temperature_distribution(self, location_type, location_name):
        if location_type == 'Country':
            location_data = self.data[self.data['Country'] == location_name]['AverageTemperature']
        elif location_type == 'City':
            location_data = self.data[self.data['City'] == location_name]['AverageTemperature']
        elif location_type == 'State':
            location_data = self.data[self.data['State'] == location_name]['AverageTemperature']
        else:
            raise ValueError("Invalid location_type. Choose from 'Country', 'City', or 'State'.")

        fig = px.histogram(location_data, x=location_data, histnorm='probability density', nbins=30, opacity=0.5)
        fig.update_traces(marker=dict(color='skyblue'), selector=dict(type='histogram'))

        fig.update_layout(title=f"Temperature Distribution in {location_name}",
                          xaxis_title="Average Temperature",
                          yaxis_title="Density",
                          paper_bgcolor='rgba(0,0,0,0)')
        fig.update_layout(width=1300, height=600)
        return fig
    
    # this method compares boxplots (for the variable AverageTemperature) of 
    # countries/cities (depending on the dataset) of your choice 
    def BoxplotCreator(self, selection, is_country=True):
        # in this way, the method can be used for both datasets with cities and datasets 
        # with countries (since latitude and longitude do not come into play)
        if is_country:
            selected_data = self.data[self.data['Country'].isin(selection)]
        else:
            selected_data = self.data[self.data['City'].isin(selection)]

        # rainbow-based colours
        c = ['hsl(' + str(h) + ',50%,50%)' for h in np.linspace(0, 360, len(selection))]

        fig = go.Figure()

        for i, item in enumerate(selection):
            y_data = selected_data[selected_data['Country' if is_country else 'City'] == item]['AverageTemperature']
            fig.add_trace(go.Box(
                y=y_data,
                name=item,
                boxpoints='all',
                jitter=0.5,
                whiskerwidth=0.01,
                fillcolor=c[i],
                marker=dict(color=c[i], size=1.2),
                line=dict(color='grey'),
                line_width=1)
            )

        fig.update_layout(
            title='Boxplot',
            yaxis=dict(
                autorange=True,
                showgrid=True,
                zeroline=True,
                dtick=5,
                gridcolor='rgb(255, 255, 255)',
                gridwidth=1,
                zerolinecolor='rgb(255, 255, 255)',
                zerolinewidth=2,
            ),
            margin=dict(
                l=40,
                r=30,
                b=80,
                t=100,
            ),
            paper_bgcolor='rgb(0,0,0,0)',
            plot_bgcolor='rgb(0,0,0,0)',
            showlegend=False
        )

        fig.update_layout(width=1300, height=600)

        return fig
    
    # this method creates a graph in which the average monthly temperatures of 
    # two countries/cities of choice are compared (via bands)
    def TemperatureComparisonHistogram(self, location_1, location_2, is_country=True):
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        fig = go.Figure()
        colors = ['#EB89B5', '#330C73']

        for i, location in enumerate([location_1, location_2]):
            location_data = self.data[self.data['Country' if is_country else 'City'] == location]
            monthly_avg_temps = [location_data[location_data['dt'].dt.month == month]['AverageTemperature'].mean() for month in range(1, 13)]
            fig.add_trace(go.Bar(x=months, y=monthly_avg_temps, name=location, marker_color=colors[i], opacity=0.75))

        location_type = 'Country' if is_country else 'City'
        fig.update_layout(
            barmode='group',
            xaxis_title='Months',
            yaxis_title='Average Temperature',
            title=f'Comparison of Average Monthly Temperatures - {location_type}',
            paper_bgcolor='rgba(0,0,0,0)'
        )

        fig.update_layout(width=1300, height=600)

        return fig
    

    # this is a method that creates boxplots specifically for the State dataset: based on the 
    # selected country, the boxplots of all the states that are part of the selected country 
    # are plotted in the same graph (for comparison)
    def StateBoxPlotter(self, selected_country):
        country_data = self.data[self.data['Country'] == selected_country]

        unique_states = country_data['State'].unique()
        N = len(unique_states)  
        c = ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 360, N)]

        fig = go.Figure(data=[go.Box(
            y=country_data[country_data['State'] == country]['AverageTemperature'],
            name=country,
            marker_color=c[i]
        ) for i, country in enumerate(unique_states)])

        fig.update_layout(
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(zeroline=False, gridcolor='white'),
            paper_bgcolor='rgb(233,233,233)',
            plot_bgcolor='rgb(233,233,233)',
            title=f'Boxplots of Average Temperature by State in {selected_country}'
        )
        fig.update_layout(width=1300, height=600)
        return fig
    
    # this method creates a graph where bands are displayed for each city/country representing 
    # the maximum temperature variation that the city/country experiences
    # the bands are shown in ascending order and are coloured according to their percentage 
    # position
    def TempRange(self, location_type):
        # calculates the width of each band for each city (country) and then sorts them in ascending order
        city_widths = self.data.groupby(location_type)['AverageTemperature'].apply(lambda x: x.max() - x.min()).reset_index()
        city_widths = city_widths.sort_values(by='AverageTemperature', ascending=False)

        fig, ax = plt.subplots(figsize=(12, 8))
        fig.set_facecolor('none')
        cmap = sns.color_palette("viridis", as_cmap=True)

        for city in city_widths[location_type]:
            city_data = self.data[self.data[location_type] == city]

            min_temp = city_data['AverageTemperature'].min()
            max_temp = city_data['AverageTemperature'].max()
            bar_width = max_temp - min_temp

            # percentage position of the band with respect to the total range:
            # (city_min - general_min) / (general_max - general_min)
            position_percent = (min_temp - self.data['AverageTemperature'].min()) / (
                self.data['AverageTemperature'].max() - self.data['AverageTemperature'].min()
            )

            # creation of the bar (for each city/country), coloured according to its percentage position
            ax.barh(city, width=bar_width, left=min_temp, color=cmap(position_percent))

        # removing city names from the y-axis:
        ax.set_yticks([])

        # colormap legend bar:
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=self.data['AverageTemperature'].min(), vmax=self.data['AverageTemperature'].max())) 
        plt.colorbar(sm, label='Average Temperature', ax=ax)

        ax.set_title(f'Temperature Range by {location_type}')
        ax.set_xlabel('Average Temperature')
        ax.set_ylabel(f'{location_type}')

        # Visualizza il grafico
        return plt

    # this method does the same as the previous one but only for the 4 cities/countries with the 
    # highest variation and for the 4 with the lowest variation
    def TopTempRange(self, location_type):
        city_widths = self.data.groupby(location_type)['AverageTemperature'].apply(lambda x: x.max() - x.min()).reset_index()
        city_widths = city_widths.sort_values(by='AverageTemperature', ascending=False)

        fig, ax = plt.subplots(figsize=(12, 8))
        fig.set_facecolor('none')
        cmap = sns.color_palette("viridis", as_cmap=True)

        top_cities_max_range = city_widths.head(4)[location_type]
        top_cities_min_range = city_widths.tail(4)[location_type]

        for i, city in enumerate(top_cities_min_range):

            city_data = self.data[self.data[location_type] == city]

            min_temp = city_data['AverageTemperature'].min()
            max_temp = city_data['AverageTemperature'].max()
            bar_width = max_temp - min_temp

            position_percent = (min_temp - self.data['AverageTemperature'].min()) / (
                self.data['AverageTemperature'].max() - self.data['AverageTemperature'].min()
            )
            ax.barh(i, width=bar_width, left=min_temp, color=cmap(position_percent), height=0.2)

        for i, city in enumerate(top_cities_max_range):

            city_data = self.data[self.data[location_type] == city]

            min_temp = city_data['AverageTemperature'].min()
            max_temp = city_data['AverageTemperature'].max()
            bar_width = max_temp - min_temp

            position_percent = (min_temp - self.data['AverageTemperature'].min()) / (
                self.data['AverageTemperature'].max() - self.data['AverageTemperature'].min()
            )
            ax.barh(i + len(top_cities_min_range), width=bar_width, left=min_temp, color=cmap(position_percent), height=0.3)

        # setting city/country names on y-axis
        ax.set_yticks(list(range(0, 8)))
        ax.set_yticklabels(list(top_cities_min_range) + list(top_cities_max_range), fontsize=8)

        sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=self.data['AverageTemperature'].min(), vmax=self.data['AverageTemperature'].max()))
        plt.colorbar(sm, label='Average Temperature', ax=ax)

        ax.set_title(f'Top 4 {location_type} with Max and Min Temperature Ranges')
        ax.set_xlabel('Average Temperature')
        ax.set_ylabel(f'{location_type}')

        return plt
    
    # this method creates a scatterplot to highlight the negative correlation present 
    # between temperature variation and average temperature (correlation noted in the graph above)
    def ScatterPlot(self, location_type):
        variation_results = []

        for country in self.data[location_type].unique():
            country_data = self.data[self.data[location_type] == country]

            max_temp = country_data['AverageTemperature'].max()
            min_temp = country_data['AverageTemperature'].min()
            variation = max_temp - min_temp
            avg_temp = country_data['AverageTemperature'].mean()

            variation_results.append({
                'Country': country,
                'Avg Temp': avg_temp,
                'VariationTemperature': variation
            })

        variation_df = pd.DataFrame(variation_results)

        fig = px.scatter(
            variation_df,
            x='Avg Temp',
            y='VariationTemperature',
            text='Country',
            title='Average Temperature vs Variation Temperature by Country'
        )

        fig.update_traces(
            marker=dict(size=12, opacity=0.8, line=dict(width=0.5, color='DarkSlateGrey')),
            selector=dict(mode='markers+text')
        )

        fig.update_layout(
            xaxis=dict(title='Average Temperature'),
            yaxis=dict(title='Variation Temperature'),
            hovermode='closest'
        )
        fig.update_layout(width=1300, height=600)

        return fig