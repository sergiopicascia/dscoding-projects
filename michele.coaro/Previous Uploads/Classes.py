import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import pycountry_convert as pc
import seaborn as sns
import matplotlib.pyplot as plt
import functions as f
import numpy as np

class MyDataFrame:

    def __init__(self, path = "GlobalLandTemperaturesByMajorCity.csv"):
        self.df = pd.read_csv(path)

    def coordinatore(self):
        def latitude(x):
                if (x[len(x) - 1] == 'N'):
                        i = float(x[:len(x) - 1])
                else:
                        i = -float(x[:len(x) - 1])
                return i


        def longitude(x):
                if (x[len(x) - 1] == 'E'):
                        i = float(x[:len(x) - 1])
                else:
                        i = -float(x[:len(x) - 1])
                return i

        self.df['Latitude'] = self.df['Latitude'].apply(latitude)
        self.df['Longitude'] = self.df['Longitude'].apply(longitude)


    def aggiustatutto(self):
        self.df.dropna(inplace=True)

        if 'dt' in self.df.columns:
            self.df.rename(columns={'dt': 'Date'}, inplace=True)
            self.df.sort_values(by="Date", inplace=True)
        if 'year' in self.df.columns:
            self.df.rename(columns={'year': 'Year'}, inplace=True)
            self.df.sort_values(by="Year", inplace=True)

        if 'Country' in self.df.columns:
            self.df = self.df[self.df['Country'] != 'Denmark']
            self.df.loc[self.df['Country'] == 'Denmark (Europe)', 'Country'] = 'Denmark'
            if 'Continent' not in self.df.columns:
                self.df['Continent'] = self.df['Country'].apply(f.country_to_continent)


    def data_monthly(self):
        self.df['Date']= pd.to_datetime(self.df['Date'])
        self.df['Year']= self.df['Date'].dt.year
        self.df['Month']= self.df['Date'].dt.month

    def data_yearly(self):
        self.df['Year'] = pd.to_datetime(self.df['Date']).dt.year
        if 'Continent' in self.df.columns:
            self.df = self.df.groupby(['City', 'Latitude', 'Longitude', 'Year', 'Continent'])['AverageTemperature'].mean().reset_index()
        else:
            self.df = self.df.groupby(['City', 'Latitude', 'Longitude', 'Year'])['AverageTemperature'].mean().reset_index()

    def mergeoncontinents(self,Cpath = "c4country.csv"):
        continents = pd.read_csv(Cpath)
        self.df = self.df.dropna()
        self.df = self.df.merge(continents, left_on='Country', right_on='Country', how='left')
        self.df['Year'] = pd.to_datetime(self.df['Date']).dt.year
        #self.df['Year'] = self.df['Date'].dt.year

    def Salvatore(self, saved = "ProvaClasse.csv"):
        self.a = self.df.to_csv(saved)


class Graficante:

    def __init__(self, data = None): #path = "YearlyTemp.csv")
        #self.data = pd.read_csv(path)
        self.data = data

    def mapper(self, namesave = "Animated_YT_Map.html"):
        token = open('token.txt').read()
        self.data['new_size'] = self.data['AverageTemperature'] + abs(self.data['AverageTemperature'].min()) + 2
        # reorder temp by year from lowest to highest
        self.data.sort_values(by="Year")
        fig = px.scatter_mapbox(self.data, lat='Latitude',
                                lon='Longitude', color = 'AverageTemperature',
                                animation_frame='Year',
                                animation_group='City',
                                center=dict(lat=30, lon=10),
                                zoom=1,
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
        fig.update_layout(mapbox_style="dark", mapbox_accesstoken=token)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        fig.update_geos(fitbounds="locations")
        fig.show()

    def ridgePlot(self, target_continent, start_year, end_year):

        self.data = f.filt_period(self.data, target_continent, start_year, end_year)
        plt.figure(figsize=(18, 12))

        plt.style.use('fivethirtyeight')
        # Palette
        pal = sns.color_palette(palette='husl', n_colors=(end_year + 1 - start_year))

        # Creating Grid
        g = sns.FacetGrid(self.data, row='Year', hue='Year', aspect=15, height=1, palette=pal)


        # Then we add the densities kdeplots for each year
        g.map(sns.kdeplot, 'AverageTemperature', bw_adjust=0.2, clip_on=False, fill=True, alpha=0.7, linewidth=1.5)

        # Horizontal lines
        g.map(plt.axhline, y=0, lw=2, clip_on=False, color="black")
        #g.set(xlim=(-10, None), ylim=(0, None))

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
        plt.show()
        #plt.savefig("RidgePlot.html", format = 'svg')

    def bee_double(self, city1, city2, year):
            # Filter the DataFrame for the specified cities and year
        data_city1 = self.data[(self.data['City'] == city1) & (self.data['Date'].dt.year == year)]
        data_city2 = self.data[(self.data['City'] == city2) & (self.data['Date'].dt.year == year)]

        # Combine the data for both cities
        combined_data = pd.concat([data_city1, data_city2])

            # Plotting
        plt.figure(figsize=(10, 6))

        plt.style.use('fivethirtyeight')
        sns.swarmplot(x='City', y='AverageTemperature', size=15, data=combined_data, hue='City', dodge=True)
        plt.title(f'Monthly Temperature in {city1} and {city2} in {year}', fontsize=18, fontweight='bold')
        plt.xlabel('Cities', fontsize=14, fontweight='bold')
        plt.ylabel('Average Temperature', fontsize=14, fontweight='bold')
        plt.legend()
        plt.grid(True)

        plt.show()

    def single_country(self, country, year):
        #plot a line plot of the average temperature in each month in that country for the selected year
        # Filter the DataFrame for the specified country and year
        data_country = self.data[(self.data['Country'] == country) & (self.data['Date'].dt.year == year)]
        #plot the line plot
        plt.figure(figsize=(10, 6))
        plt.style.use('fivethirtyeight')
        sns.lineplot(x='Month', y='AverageTemperature', data=data_country, color='black', marker='o')
        plt.title(f'Average Monthly Temperature in {country} in {year}', fontsize=18, fontweight='bold')
        plt.xlabel('Month', fontsize=14, fontweight='bold')
        plt.ylabel('Average Temperature', fontsize=14, fontweight='bold')
        plt.grid(True)
        plt.show()

    def double_country(self, country1, country2, year):
        #bar graph that compares average temperature for each month in the specified year
        # Filter the DataFrame for the specified country and year
        data_country1 = self.data[(self.data['Country'] == country1) & (self.data['Date'].dt.year == year)]
        data_country2 = self.data[(self.data['Country'] == country2) & (self.data['Date'].dt.year == year)]
        combined_data = pd.concat([data_country1, data_country2])

        #plot the bar graph
        plt.figure(figsize=(10, 6))
        plt.style.use('fivethirtyeight')
        g = sns.catplot(x='Month', y='AverageTemperature', hue='Country', data=combined_data, kind='bar', height=6, palette='husl', errorbar='ci')
        plt.title(f'Average Monthly Temperature in {country1} and {country2} in {year}', fontsize=18, fontweight='bold')
        #set ylim to (0,35) to make the graph more readable
        plt.ylim((combined_data['AverageTemperature'].min()-2), (combined_data['AverageTemperature'].max()+2))
        #on the x axis plot the values inside ['Month'] column
        g.set_xticklabels(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September',
                           'October', 'November', 'December'], fontsize=9, rotation = 45)
        plt.xlabel('Month', fontsize=14, fontweight='bold')
        plt.ylabel('Average Temperature', fontsize=14, fontweight='bold')
        plt.legend()
        plt.grid(True)
        plt.show()

    def boxen_plot(self, country, start_year, end_year, range):
        # Filter the DataFrame for the specified country and year
        data_country = self.data[(self.data['Country'] == country) & (self.data['Date'].dt.year >= start_year) & (
                    self.data['Date'].dt.year <= end_year)]

        # Create a new column to represent the year group based on the specified range
        data_country['YearGroup'] = (data_country['Date'].dt.year - start_year) // range * range + start_year

        # Convert 'AverageTemperature' and any other relevant columns to numeric data type
        numeric_columns = ['AverageTemperature']  # Add other relevant columns here
        data_country[numeric_columns] = data_country[numeric_columns].apply(pd.to_numeric, errors='coerce')

        # Group by the new 'YearGroup' and calculate the mean for each group
        data_country = data_country.groupby('YearGroup').mean().reset_index()

        # Plot the boxen plot
        plt.figure(figsize=(10, 6))
        plt.style.use('fivethirtyeight')
        sns.boxenplot(x='YearGroup', y='AverageTemperature', data=data_country, color='black')
        plt.title(f'Average Temperature in {country} from {start_year} to {end_year}', fontsize=18, fontweight='bold')
        plt.xlabel('Year Group', fontsize=14, fontweight='bold')
        plt.ylabel('Average Temperature', fontsize=14, fontweight='bold')
        plt.ylim(range)
        plt.grid(True)
        plt.show()






