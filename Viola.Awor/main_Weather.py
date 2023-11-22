

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import plotly.express as px
import plotly


pd.options.plotting.backend = "plotly"
pd.set_option('display.width', 200)

plt.style.use('dark_background')

"""With pandas loaded data as a dataframe"""
# Reading the dataset

df_City = pd.read_csv('GlobalLandTemperaturesByCity.csv')
df_MajorCity = pd.read_csv('GlobalLandTemperaturesByMajorCity.csv')

df_MajorCity.info()

"""###  Dataset cleaning by removing rows with Any missing data,dropping null values,
converting the td column to Datetime format,removing duplicates ,describing the dataset to understand
 the statistical methods and structures"""

df_MajorCity.isnull().sum().sort_values(ascending=False)

# set(df_MajorCity.City.unique()).intersection(df_City.City.unique())

df_MajorCity_clean = df_MajorCity.loc[:,['dt','AverageTemperature','City']].copy()
# Drop null rows if any column value is null
df_MajorCity_clean = df_MajorCity_clean.dropna(how='any')
df_MajorCity_clean['dt'] = pd.to_datetime(df_MajorCity_clean['dt'])
df_MajorCity_clean['year'] = df_MajorCity_clean['dt'].dt.year
df_MajorCity_clean = df_MajorCity_clean[df_MajorCity_clean['year']>=1750]
df_MajorCity_clean = df_MajorCity_clean.drop_duplicates()
df_MajorCity_clean = df_MajorCity_clean.reset_index(drop=True)
df_MajorCity_clean.info()

df_MajorCity_clean.describe()



''' Plotting timeseries graph to show the temperature changes over the years using the monthly average temperature values'''


# Convert the 'dt' column to datetime format
df_MajorCity_clean['dt'] = pd.to_datetime(df_MajorCity_clean['dt'])

# Extract year and month from the 'dt' column
df_MajorCity_clean['year'] = df_MajorCity_clean['dt'].dt.year
df_MajorCity_clean['month'] = df_MajorCity_clean['dt'].dt.month
# Filter years for 2013
data = df_MajorCity_clean[(df_MajorCity_clean['year'] >= 1880) & (df_MajorCity_clean['year'] <= 1990)]
sample_cities = ['Los angelos', 'Shanghai', 'New Delhi', ' Madras', 'Abidjan', 'Izmir']
data = data[(data['City'].isin(sample_cities))]
# Check if 'Country' column is present in data
if 'City' in data.columns:
    # Create an animated time series plot for sample countries
    plt.figure(figsize=(10, 6))

    def update(frame):
        plt.clf()
        df = data[data['year'] == frame]
        ax = sns.lineplot(x='month', y='AverageTemperature', hue='City', data=df)
        ax.set_title(f'Temperature Changes Over Time (Year: {frame})')
        ax.set_xlabel('MonthS')
        ax.set_ylabel('Average Temperature (°C)')

    # Animating the plot
    years = sorted(data['year'].unique())
    ani = FuncAnimation(plt.gcf(), update, frames=years, repeat=True, interval=500)

    # Save the animation as a GIF using ImageMagick
    ani.save('temperature_changes.gif', writer='imagemagick')
    plt.show()
else:
    print("Error: 'Country' column not found in the DataFrame.")





'''calculating the largest temperatures ranking according frequency to find the highest Ranking'''

# Rank Cities based on their temperatures ranges
df_MajorCity_clean["rank"] = df_MajorCity_clean.groupby("dt")["AverageTemperature"].\
rank(method="dense", ascending=False)
df_MajorCity_clean.head()

df_MajorCity_ranks = \
df_MajorCity_clean.groupby(['City','rank'])['rank'].count().rename('count').reset_index().\
  pivot(index='City', columns='rank', values='count').reset_index().\
  sort_values(by=[1,2,3,4], ascending=[False, False, False,False]).\
  reset_index(drop=True).\
  iloc[:,:5]

df_MajorCity_ranks = df_MajorCity_ranks.rename_axis(None, axis=1)
df_MajorCity_ranks.head(15)



'''Plotting a stacked bar graph to showing the distribution of highest average  
temperature according to 4 highest ranks in top 15 cities'''

data = (df_MajorCity_ranks.head(15)).set_index('City')

cols = ["blue", "brown", "pink", "green"]
for rank, col in zip(data.columns, cols):
  plt.barh(data.index, data.loc[:,rank], color=col)
plt.xlabel("City")
plt.ylabel("Rank")
plt.title("Count of City Ranks for 15 most frequently hottest Cities")
plt.show()

data

df_MajorCity_dt = \
df_MajorCity_clean.pivot(index='dt', columns='City', values='AverageTemperature').reset_index()

df_MajorCity_dt = df_MajorCity_dt.rename_axis(None, axis=1)
df_MajorCity_dt.head()

'''Filtering the top five highest avaerage temperating ranking Cities in the dataset'''
cities = ['dt'] + (df_MajorCity_ranks.nlargest(5, 1))['City'].tolist()
df_MajorCity_dt_viz = df_MajorCity_dt.loc[:,cities]
df_MajorCity_dt_viz = df_MajorCity_dt_viz.set_index('dt').dropna(how='any')
df_MajorCity_dt_viz.head()

# df_MajorCity_dt_viz.to_csv('df_MajorCity_dt_viz.csv')




'''plotting a heatmap graph showing comparison in hight  average temperature ranges
 among the top five cities over the last two years'''

# Filtering the last 5 years
df_MajorCity_dt_viz = df_MajorCity_dt_viz[df_MajorCity_dt_viz.index.year >= (df_MajorCity_dt_viz.index.year.max() -2)]

# Plot heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(df_MajorCity_dt_viz.transpose(), cmap='YlOrRd',  annot=True, cbar_kws={'label': 'Temperature (°C)'})
plt.xlabel('Years')
plt.ylabel('Cities')
plt.title('Temperature Changes comparison Across Top 5 Hottest Cities Over the Last 2 Years')
plt.show()




'''Plotting a heat map graph to  comparison between 5 cities  in the top ranking 2  years of  the highest temperatures'''

# Finding the top five years with the highest temperatures in the top ranking two years
top_five_years = df_MajorCity_dt_viz.resample('Y').max().mean(axis=1).nlargest(2).index.year

# Filtering data for the top five years
df_MajorCity_dt_viz_top_years = df_MajorCity_dt_viz[df_MajorCity_dt_viz.index.year.isin(top_five_years)]

#  heatmap plotting
plt.figure(figsize=(12, 8))

# Using diverging colormap to show  temperature differences
cmap = sns.color_palette("coolwarm", as_cmap=True)

sns.heatmap(df_MajorCity_dt_viz_top_years.transpose(),  annot=True, cmap=cmap, fmt=".2f", cbar_kws={'label': 'Temperature (°C)'})
plt.xlabel('Year')
plt.ylabel('City')
plt.title('Highest Temperature Comparison Among Top 5 Cities Over the Top ranking  2 years')
plt.show()








"""## Part 2 <a class="anchor" id="second"></a>"""

df_MajorCity_path = (df_MajorCity.drop(columns=['AverageTemperatureUncertainty'])).dropna(how='any')

df_MajorCity_path['dt'] = pd.to_datetime(df_MajorCity_path['dt'])
df_MajorCity_path['year'] = df_MajorCity_path['dt'].dt.year
df_MajorCity_path = df_MajorCity_path[df_MajorCity_path['year']>=1750]
df_MajorCity_path = df_MajorCity_path.drop_duplicates()
df_MajorCity_path = df_MajorCity_path.reset_index(drop=True)
df_MajorCity_path.head()

df_MajorCity_path.info()