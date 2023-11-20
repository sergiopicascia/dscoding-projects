
import random
import pandas as pd
import data_generator

import matplotlib.pyplot as plt
netflix_data = pd.read_csv('netflix_data.csv')


#RELEASE YEAR BAR PLOT
show_release_year = netflix_data['release_year'].value_counts()

# Creating a bar chart year-number of movies
plt.bar(show_release_year.index, show_release_year.values)

plt.xlabel('Release Year')
plt.ylabel('Count')
plt.title('Distribution of movies and TV shows by year')

plt.show()






#SHOW TYPES PLOT

# Calculate the count of each show type
show_type = netflix_data['type'].value_counts()

# Create a pie chart
plt.pie(show_type, labels=show_type.index, autopct='%1.1f%%')
plt.axis('equal')
plt.title('Distribution of Show Types on Netflix')

plt.show()






#DURATION PLOT
# Converting the duration column to int only
netflix_data['duration'] = netflix_data['duration'].str.replace(' Seasons', '').str.replace(' min', '').str.replace(' Season', '')
netflix_data['duration'] = pd.to_numeric(netflix_data['duration'], errors='coerce')

# Separating data for movies and TV shows
movies_data = netflix_data[(netflix_data['type'] == 'Movie')&(netflix_data['duration']<= 180)]
tv_shows_data = netflix_data[(netflix_data['type'] == 'TV Show')&(netflix_data['duration'] <= 11)]
#season_counts is a Series with index(num.of seasons) and values(the count of TV shows)
season_counts = tv_shows_data['duration'].value_counts().sort_index() 


# Creating the area for the plots
plt.figure(figsize=(8, 5))
# Histogram for movies
plt.subplot(1, 2, 1)
plt.hist(movies_data['duration'], bins=20, edgecolor='black')
plt.title('Movie Durations')
plt.xlabel('Duration (minutes)')
plt.ylabel('Frequency')
plt.xticks(range(0,180,30))

# bar chart for movies
plt.subplot(1, 2, 2)
plt.bar(season_counts.index, season_counts.values, edgecolor='black')
plt.title('Number of TV Shows by Season')
plt.xlabel('Number of Seasons')
plt.ylabel('Count')
plt.xticks(range(0, 12))

plt.tight_layout()
plt.show()


