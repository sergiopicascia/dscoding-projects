import plotly.express as px
import pandas as pd
import pycountry_convert as pc
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

#Given the country name, it returns the continent name using pyCountry_convert
def country_to_continent(country_name):
    try:
        country_alpha2 = pc.country_name_to_country_alpha2(country_name)
        country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
        country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
    except:
        country_continent_name = None
    return country_continent_name

class MyDataFrame:

    def __init__(self, path = "GlobalLandTemperaturesByMajorCity.csv"):
        self.df = pd.read_csv(path)

    #The following function is used to convert the coordinates which have the format similar to 36N 28E to purely numerical ones
    def coordinatore(self):
        def latitude(x):
            if isinstance(x, str):
                if (x[len(x) - 1] == 'N'):
                        i = float(x[:len(x) - 1])
                else:
                        i = -float(x[:len(x) - 1])
                return i
            else:
                return x


        def longitude(x):
            if isinstance(x, str):
                if (x[len(x) - 1] == 'E'):
                        i = float(x[:len(x) - 1])
                else:
                        i = -float(x[:len(x) - 1])
                return i
            else:
                return x

        #The following two lines apply the functions to the columns of the dataframe to clean it
        self.df['Latitude'] = self.df['Latitude'].apply(latitude)
        self.df['Longitude'] = self.df['Longitude'].apply(longitude)


    def data_fixer(self):

        self.df.dropna(inplace=True)

        if 'dt' in self.df.columns:
            self.df.rename(columns={'dt': 'Date'}, inplace=True)
            self.df = self.df.sort_values(by="Date")
        if 'year' in self.df.columns:
            self.df.rename(columns={'year': 'Year'}, inplace=True)
            self.df = self.df.sort_values(by="Year")
        if 'Country' in self.df.columns:
            self.df = self.df[self.df['Country'] != 'Denmark']
            self.df.loc[self.df['Country'] == 'Denmark (Europe)', 'Country'] = 'Denmark'
            if 'Continent' not in self.df.columns:
                self.df['Continent'] = self.df['Country'].apply(country_to_continent)

        self.df['Date'] = pd.to_datetime(self.df['Date'])


    #The following two functions are used to create specific columns for the year and the month, thus allowing to plot different graphs
    def data_monthly(self):
        self.df['Year']= self.df['Date'].dt.year
        self.df['Month']= self.df['Date'].dt.month

    def data_yearly(self):
        self.df['Year'] = pd.to_datetime(self.df['Date']).dt.year
        if 'Continent' in self.df.columns:
            self.df = self.df.groupby(['City', 'Latitude', 'Longitude', 'Year', 'Continent', 'Date'])['AverageTemperature'].mean().reset_index()
        else:
            self.df = self.df.groupby(['City', 'Latitude', 'Longitude', 'Year', 'Date'])['AverageTemperature'].mean().reset_index()

    #The following function is used to merge the dataframe with the one containing the continents "locations"
    def mergeoncontinents(self,Cpath = "c4country.csv"):
        continents = pd.read_csv(Cpath)
        self.df = self.df.dropna()
        self.df = self.df.merge(continents, left_on='Country', right_on='Country', how='left')
        self.df['Year'] = pd.to_datetime(self.df['Date']).dt.year

    #this function, truly didascalical, is used to save the dataframe in a csv file
    def data_saver(self, saved = "ProvaClasse.csv"):
        self.a = self.df.to_csv(saved)


#second class, implementing the plotting methods (mostly)
class Graficante:

    def __init__(self, data = None): #path = "YearlyTemp.csv")
        #self.data = pd.read_csv(path)
        self.data = data


    #used to filter data by continent and time period
    def filt_period(self, target_continent, start_year, end_year):
        # Filter by continent
        df_continent = self.data[self.data['Continent'] == target_continent]

        # Filter by time period (max 10 years)
        if start_year is not None and end_year is not None:
            self.data = df_continent[(df_continent['Year'] >= start_year) & (df_continent['Year'] <= end_year)]
        else:
            self.data = df_continent

        return self.data

    #used to create the map. Plots the average temperature and its movement across time
    def mapper(self):
        token = open('token.txt').read()
        self.data = self.data.sort_values(by="Year")
        self.data['new_size'] = (self.data['AverageTemperature'] + abs(self.data['AverageTemperature'].min()) + 2)
        # reorder temp by year from lowest to highest
        self.data.sort_values(by="Year")
        fig = px.scatter_mapbox(self.data, lat='Latitude',
                                lon='Longitude', color  = 'AverageTemperature',
                                animation_frame='Year',
                                animation_group='City',
                                center=dict(lat=30, lon=10),
                                zoom=2,
                                size='new_size',
                                mapbox_style="stamen-terrain",
                                hover_name=self.data['City'],
                                hover_data={'Year': False,
                                            'City': False,
                                            'AverageTemperature': True,
                                            'Latitude': False,
                                            'Longitude': False,
                                            'new_size': False},
                                title='Average Temperature in Global Major Cities',
                                color_continuous_scale=px.colors.cyclical.IceFire,
                                range_color=(self.data['AverageTemperature'].min(), self.data['AverageTemperature'].max()))
        fig.update_layout(mapbox_style="light", mapbox_accesstoken=token)
        #change the animation slider style
        fig.layout.sliders[0].pad.t = 50
        fig.update_layout(showlegend=False)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        fig.update_layout(coloraxis_showscale=False)
        fig.update_geos(fitbounds="locations")
        #fig.show()
        return fig

    #plots the distribution of temperatures in the selected continents, needs a list of years and a continent to work
    def ridge_plot(self):
        # Get user input for target_continent, start_year, and end_year
        target_continent = st.selectbox('Select Continent', self.data['Continent'].unique())
        start_year = st.selectbox('Select Year', np.sort(self.data['Year'].unique()))
        end_year = st.selectbox('Select End Year', np.sort(self.data[self.data['Year'] >= start_year]['Year'].unique()))

        # Obtained user input and avoided errors
        if target_continent is not None and start_year is not None and end_year is not None:
            fig = self.perform_ridge_plot(target_continent, start_year, end_year)
            st.pyplot(fig)


    #used to create the ridge plot. Plots the distribution of the average temperature and its movement across years,
    # in a simple an eye-catching way
    #most graphs are structured in the following way: two functions (plot and perform_plot), with the intention of separating
    #the logic from the actual plotting, in order to make the code more readable and easier to modify, as well as easier to implement
    #in streamlit
    def perform_ridge_plot(self, target_continent, start_year, end_year):
        # Filter the DataFrame for the specified continent and year range
        filtered_data = self.filt_period(target_continent, start_year, end_year)

        plt.figure(figsize=(18, 12))
        plt.style.use('fivethirtyeight')

        # Palette
        pal = sns.color_palette(palette='husl', n_colors=(end_year + 1 - start_year))

        # Creating Grid
        g = sns.FacetGrid(filtered_data, row='Year', hue='Year', aspect=15, height=1, palette=pal)

        # Then we add the densities kdeplots for each year
        g.map(sns.kdeplot, 'AverageTemperature', bw_adjust=0.2, clip_on=False, fill=True, alpha=0.7, linewidth=1.5)

        # Horizontal lines
        g.map(plt.axhline, y=0, lw=2, clip_on=False, color="black")

        # Adjusting to get the subplots to overlap
        g.fig.subplots_adjust(hspace=-0.3)

        # Eventually, we remove axes titles, yticks, and spines
        g.set_titles("")
        g.set(yticks=[])
        g.set_ylabels("")
        g.despine(bottom=True, left=True)
        g.fig.subplots_adjust(hspace=1)
        plt.xlabel('Temperature in degree Celsius', fontweight='bold', fontsize=15)
        g.fig.suptitle(f'Average temperature in {target_continent} from {start_year} to {end_year}', ha='center',
                       fontsize=20, fontweight=20)

        # Return the matplotlib figure
        return plt.gcf()

    #plots the distribution of the average temperature in a single year in two different countries, useful as it acts
    #as a comparison between the two countries, displaying some characeristics of the data, which can be strongly seasonal at times
    def bee_double(self):
        # Get user input for cities and year
        selected_cities = st.multiselect('Select Cities', self.data['City'].unique(), max_selections=2)
        year = st.selectbox('Select Year', np.sort(self.data['Year'].unique()))

        #avoid error when no cities are selected (selected_cities = None)
        if selected_cities is not None and len(selected_cities) == 2:
            fig = self.perform_bee_double(selected_cities, year)
            st.pyplot(fig)

        # Display the result or take further actions

    def perform_bee_double(self, selected_cities, year):
        # Your logic here based on user-selected values
        # Perform calculations or operations using selected_cities and year
        # For example, you might access the dataset and filter it based on user input
        filtered_data = self.data[(self.data['City'].isin(selected_cities)) & (self.data['Year'] == year)]

        # Create a swarmplot using Seaborn
        plt.figure(figsize=(10, 6))
        sns.swarmplot(x='City', y='AverageTemperature', data=filtered_data, size = 11, hue='City', palette='husl')

        # Customize the plot as needed
        plt.title(f'Temperature Distribution of {selected_cities[0]} and {selected_cities[1]} in {year}', fontsize=18, fontweight='bold')
        plt.xlabel('City')
        plt.ylabel('Average Temperature')

        # Return the matplotlib figure
        return plt.gcf()

    #plots the monthly temperature for the selected city, over as many years as the user requests
    def city_liner(self):
        # Get user input for cities and number of years
        selected_city = st.selectbox('Select City', self.data['City'].unique())
        start_year = st.selectbox('Select Year', np.sort(self.data['Year'].unique()))
        end_year = st.selectbox('Select End Year', np.sort(self.data[self.data['Year'] >= start_year]['Year'].unique()))

        # Avoid error when no cities are selected (selected_city = None)
        if selected_city is not None:
            fig = self.perform_city_liner(selected_city, start_year, end_year)
            st.plotly_chart(fig, use_container_width=True)

    def perform_city_liner(self, selected_city, start_year, end_year):
        filtered_data = self.data[(self.data['City'] == selected_city)]

        # Get the monthly data for the range of years specified
        filtered_data = filtered_data[(filtered_data['Date'].dt.year >= start_year) & (filtered_data['Date'].dt.year <= end_year)]
        filtered_data['MonthYear'] = filtered_data['Date'].dt.strftime('%B %Y')
        filtered_data = filtered_data.sort_values(by=['Year','Month'])


        # Use plotly express for interactive plot
        fig = px.line(filtered_data, y='AverageTemperature', x = 'Date',
                      title=f'Average Monthly Temperature in {selected_city} over {end_year - start_year} Years',
                      labels={'AverageTemperature': 'Average Temperature', 'Year': 'Year'},
                      line_shape="linear", markers=True)

        # Customize hover information
        fig.update_traces(showlegend = True, hovertemplate='%{y:.2f} °C')

        return fig

    #plots the scatter plot of the average temperature in the selected cities, over the selected time period. Shows distributions
    def city_scatter(self):
        # Get user input for cities
        selected_cities = st.multiselect('Select Cities', self.data['City'].unique(), max_selections=2)
        start_year = st.selectbox('Select Year', np.sort(self.data['Year'].unique()))
        end_year = st.selectbox('Select End Year', np.sort(self.data[self.data['Year'] >= start_year]['Year'].unique()))

        # Avoid error when no cities are selected (selected_cities = None)
        if selected_cities is not None and len(selected_cities) == 2:
            fig = self.perform_city_scatter(selected_cities, start_year, end_year)
            st.plotly_chart(fig, use_container_width=True)

    def perform_city_scatter(self, selected_cities, start_year, end_year):
        filtered_data = self.data[(self.data['City'].isin(selected_cities))]
        # Filter the data for the specified range of years
        filtered_data = filtered_data[(filtered_data['Year'] >= start_year) & (filtered_data['Year'] <= end_year)]

        # Use plotly express for interactive scatter plot
        fig = px.scatter(filtered_data, x='Year', y='AverageTemperature', color='City',
                         title=f'Temperature Scatter Plot for {", ".join(selected_cities)} ({start_year} - {end_year})',
                         labels={'AverageTemperature': 'Average Temperature', 'Year': 'Year'},
                         color_discrete_sequence=px.colors.qualitative.Set1, size_max=15, hover_data=['City'])

        # Customize hover information
        fig.update_traces(marker=dict(size=8),
                          hovertemplate='<b>City:</b><br>' + filtered_data['City'] +
                                        '<b>Year:</b> %{x}<br>'
                                        '<b>Average Temperature:</b> %{y:.2f} °C')

        return fig

    #plots the histogram of the average temperature in the selected cities, over the selected time period. Shows distributions
    def histogram_city(self):
        # Get user input for cities and range of years
        selected_cities = st.multiselect('Select Cities', self.data['City'].unique())

        # Avoid errors caused by the temporary absence of inputs
        if selected_cities is not None and len(selected_cities) >= 2:
            start_year = st.selectbox('Select Year', np.sort(self.data['Year'].unique()))
            end_year = st.selectbox('Select End Year', np.sort(self.data[self.data['Year'] >= start_year]['Year'].unique()))

            if start_year is not None and end_year is not None:
                fig = self.perform_histogram_city(selected_cities, start_year, end_year)
                st.pyplot(fig)

    def perform_histogram_city(self, selected_cities, start_year, end_year):
        # Your logic here based on user-selected values
        # For example, you might access the dataset and filter it based on user input
        filtered_data = self.data[(self.data['City'].isin(selected_cities)) & (self.data['Year'] >= start_year) & (self.data['Year'] <= end_year)]

        # Set figure size
        plt.figure(figsize=(12, 8))

        # Plot histogram chart for City 1 (var1)
        sns.histplot(x='AverageTemperature', stat="density", data=filtered_data[filtered_data['City'] == selected_cities[0]], bins=20, edgecolor='black', palette='husl', label=selected_cities[0])

        # Plot histogram chart for City 2 (var2)
        n_bins = 20
        # Get positions and heights of bars
        heights, bins = np.histogram(filtered_data[filtered_data['City'] == selected_cities[1]]['AverageTemperature'], density=True, bins=n_bins)
        # Multiply by -1 to reverse it
        heights *= -1
        bin_width = np.diff(bins)[0]
        bin_pos = (bins[:-1] + bin_width / 2)

        # Plot
        plt.bar(bin_pos, heights, width=bin_width, edgecolor='black', label=selected_cities[1], alpha=0.7)

        # Customize the plot as needed
        plt.title(f'Temperature Histogram for {", ".join(selected_cities)} ({start_year} to {end_year})', fontsize=18, fontweight='bold')
        plt.xlabel('AverageTemperature')
        plt.ylabel('Density')
        plt.legend()

        # Return the matplotlib figure
        return plt.gcf()

    #plots a line plot of the average temperature of the selected country, . Shows the evolut
    def single_country(self):
        # Get user input for country and range of years
        selected_country = st.selectbox('Select Country', self.data['Country'].unique())
        start_year = st.selectbox('Select Start Year', np.sort(self.data['Date'].dt.year.unique()))
        end_year = st.selectbox('Select End Year',
                                np.sort(self.data[self.data['Date'].dt.year >= start_year]['Date'].dt.year.unique()))

        # Avoid error when no country is selected (selected_country = None)
        if selected_country is not None and end_year is not None:
            fig = self.perform_single_country(selected_country, start_year, end_year)
            st.plotly_chart(fig, use_container_width=True)

    def perform_single_country(self, country, start_year, end_year):
        # Filter the DataFrame for the specified country and range of years
        data_country = self.data[(self.data['Country'] == country) & (self.data['Date'].dt.year >= start_year)
                                 & (self.data['Date'].dt.year <= end_year)]

        # Use Plotly Express for interactive plot
        fig = px.line(data_country, x='Date', y='AverageTemperature',
                      title=f'Average Monthly Temperature in {country} from {start_year} to {end_year}',
                      labels={'AverageTemperature': 'Average Temperature', 'Date': 'Date'},
                      line_shape="linear", markers=True, hover_data={'AverageTemperature': ':.2f'},
                      error_y='AverageTemperatureUncertainty')

        # Customize hover information
        fig.update_traces(hovertemplate='Temperature: %{y:.2f} °C')

        return fig


    #boxplots for average temperature and uncertainty, for specific countries (2) and year
    def double_country(self):
        # Get user input for country1, country2, and year
        selected_country1 = st.selectbox('Select Country 1', self.data['Country'].unique())
        selected_country2 = st.selectbox('Select Country 2', self.data['Country'].unique())
        selected_year = st.selectbox('Select Year', self.data['Date'].dt.year.unique())

        # Avoid error when no countries are selected
        if selected_country1 is not None and selected_country2 is not None and selected_year is not None:
            fig = self.perform_double_country(selected_country1, selected_country2, selected_year)
            st.plotly_chart(fig, use_container_width=True)

    def perform_double_country(self, country1, country2, year):
        # Filter the DataFrame for the specified countries and year
        data_country1 = self.data[(self.data['Country'] == country1) & (self.data['Date'].dt.year == year)]
        data_country2 = self.data[(self.data['Country'] == country2) & (self.data['Date'].dt.year == year)]
        combined_data = pd.concat([data_country1, data_country2])

        # Use Plotly Express for interactive bar graph
        fig = px.bar(combined_data, x='Month', y='AverageTemperature', color='Country',
                     labels={'AverageTemperature': 'Average Temperature', 'Month': 'Month'},
                     title=f'Average Monthly Temperature in {country1} and {country2} in {year}',
                     category_orders={
                         'Month': ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                                   'September', 'October', 'November', 'December']},
                     error_y='AverageTemperatureUncertainty')

        # Customize hover information
        fig.update_traces(hovertemplate='Temperature: %{y:.2f} °C')

        return fig

        # Return the matplotlib figure
        return plt.gcf()









