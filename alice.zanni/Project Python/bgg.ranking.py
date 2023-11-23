##  Importing necessary libraries
import pandas as pd
# Library for data manipulation and analysis. Provides data structures and facilitates handling and analyzing structured data.

import numpy as np
# Numerical Python library that provides support for large, multi-dimensional arrays and matrices, along with mathematical functions to operate on these arrays

import matplotlib.pyplot as plt
# Library for creating interactive visualisations

from scipy.stats import norm
# Submodule of SciPy, this library provides support for statistical functions

import seaborn as sns
# Built on top of matplotlib, library for better statistical data visualisation



# Comparing Geek top 20 games (as of Friday 17th of November 2023)

# Create Data frame with top 20 geek ranking games and their respective ratings
# Define the data
dt = {
    'g_ranking': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
    'title': [
        'Brass: Birmingham', 'Terraforming Mars: Prelude', 'Pandemic Legacy: Season 1',
        'Gloomhaven', 'Ark Nova', 'Twilight Imperium: Fourth Edition', 'Terraforming Mars',
        'Dune: Imperium', 'Gloomhaven: Jaws of the Lion', 'War of the Ring: Second Edition',
        'Star Wars: Rebellion', 'Spirit Island', 'Gaia Project', 'Twilight Struggle',
        'Through the Ages: A New Story of Civilization', 'Great Western Trail', 'Spirit Island: Jagged Earth',
        'Viticulture: Tuscany Essential Edition', 'The Castles of Burgundy', 'Scythe'
    ],
    'g_rating': [8.422, 8.398, 8.387, 8.374, 8.318, 8.241, 8.223, 8.206, 8.191, 8.179, 8.170, 8.150, 8.130, 8.077, 8.075, 8.051, 8.021, 8.008, 8.008, 8.006],
    'avg_rating': [8.61, 8.84, 8.53, 8.61, 8.53, 8.61, 8.37, 8.42, 8.47, 8.53, 8.42, 8.35, 8.40, 8.25, 8.30, 8.22, 9.36, 8.56, 8.13, 8.16],
    'num_voters': [41667, 14229, 51825, 60101, 36428, 22008, 93646, 39130, 31335, 20010, 30962, 47211, 25696, 47550, 30490, 39510, 4078, 9581, 59614, 79513]
}

# Create a DataFrame
geek_df = pd.DataFrame(dt)

# Sort the DataFrame by 'g_rating' in descending order to maintain the ranking
df_sorted = geek_df.sort_values(by='g_rating', ascending=False)

# Plotting
plt.figure(figsize=(12, 8))
plt.plot(df_sorted.head(20)['title'], df_sorted.head(20)['g_rating'], label='Geek Rating', marker='o', color='skyblue')
plt.plot(df_sorted.head(20)['title'], df_sorted.head(20)['avg_rating'], label='Avg Rating', marker='o', color='orange')
plt.xlabel('Game Title')
plt.ylabel('Rating')
plt.title('Geek Rating vs. Avg Rating for Top 20 Board Games')
plt.xticks(rotation=45, ha='right')
plt.legend()
plt.show()


## Cleaning our data, making it ready for further manipulations

bgg = pd.read_csv('bgg.csv')
summary = bgg.describe()
bgg = pd.DataFrame(bgg)
# Print the summary
print(summary)

# Looking at NAs within BGG dataset
null_proportion = bgg['rating'].isnull().mean()
print('Proportion of Null Values in BGG dataset')
print(null_proportion)


##Imputing group mean in null values
bgg['rating'] = bgg.groupby('game')['rating'].transform(lambda x: x.fillna(x.mean()))

# two board games have only written reviews with no ratings, we can drop these board game from our dataset
bgg.dropna(subset=['rating'], inplace=True)

print(bgg.isna().any().any())


### WILSON SCORE

##Creating liked column
bgg['liked'] = bgg['rating'].apply(lambda x: 1 if x >= 7.0 else 0)
bgg.to_csv('modified_bgg.csv', index=False)

mod_bgg = pd.read_csv('modified_bgg.csv')

## Define function  and merge results into dataframe
def wilson_score(liked_count, # number of time the game was liked
                 total_count, # total number of rating for the game
                 confidence=0.95 # confidence level for which the true population will lie in
                 ):
    if total_count == 0: # check that if there are no rating for a game.
        return 0.0
    # defining our parameters
    p = liked_count / total_count # calculating proportions of liked ratings
    z = norm.ppf(1 - (1 - confidence) / 2) # calculating the Z score corresponding to the desire level of confidence using inverse normal distribution

    lower_bound = (p + z ** 2 / (2 * total_count) - z * np.sqrt(
        (p * (1 - p) + z ** 2 / (4 * total_count)) / total_count)) / (1 + z ** 2 / total_count) # adjust proportion of liked ratings to the sample size (total_count)

    return lower_bound


# Use group_by function
wilson_scores = (bgg.groupby('game') # group the dataframe by game
                 .apply(lambda x: wilson_score(sum(x['liked']), len(x['liked'])))) # applies W-score to each game
# Add the calculated Wilson scores to the DataFrame
wilson_df = pd.DataFrame({'game': wilson_scores.index, 'wilson_score': wilson_scores.values})

# Merge the Wilson scores back to the original DataFrame
wilson = pd.merge(mod_bgg, wilson_df, on='game')
wilson = pd.DataFrame(wilson)

# Calculate average rating for each title by grouping by 'title'
average_rating_per_title = wilson.groupby('game')['rating'].mean().reset_index()
average_rating_per_title.columns = ['game', 'average_rating']

# Step 2: Create a new DataFrame with game, title, average rating, Wilson score
# Group by title and calculate the mean Wilson score for each title
wilson = wilson.groupby('game').agg({
    'title': 'first',  # Assuming 'game' is the same for each title
    'wilson_score': 'mean'
}).reset_index()

# Merge average rating into the grouped_df DataFrame
wilson = pd.merge(wilson, average_rating_per_title, on='game')

## To better compare the two methods, we will scale the wilson Score so that they are both on a 0 to 10 range.
# Create a new column 'adjusted_wilson' by multiplying 'wilson_score' by 10
wilson['adjusted_wilson'] = wilson['wilson_score'] * 10

print(wilson)
wilson.to_csv('Wilson.Score.csv')






#### Comparing the diffrent ranking method

##  Distributions of scores
# 1. Average ratings

# create distribution of average rating
plt.figure(figsize=(12, 6))
sns.kdeplot(wilson['average_rating'], color='blue')
plt.xlabel('Average User Rating')
plt.ylabel('Frequency')
plt.title('Distribution of Average User Ratings')
plt.show()

sum = wilson['average_rating'].describe()
print(sum)

# 2. Wilson Scores
# create distribution of Wilson score
plt.figure(figsize=(12, 6))
sns.kdeplot(wilson['adjusted_wilson'], color='orange')
plt.xlabel('Wilson Score')
plt.ylabel('Frequency')
plt.title('Distribution of Wilson Score')
plt.show()

sum1 = wilson['adjusted_wilson'].describe()
print(sum1)


### Plotting our entire dataset

## Boxplot comparing both methods

# Set the style for Seaborn
sns.set(style="whitegrid")

# Create a figure and axis
fig, ax = plt.subplots(figsize=(12, 6))

# Define data and colors
data = wilson[['average_rating', 'adjusted_wilson']]
colors = ['teal', 'yellow']

# Plot boxplot for top average ratings and top Wilson scores
sns.boxplot(data=data, palette=colors, ax=ax)
ax.set_xlabel('Score Type')
ax.set_ylabel('Scores')

# Title and legend
plt.title('Figure 4 : Boxplot of Top Average Ratings and Top Wilson Scores')

# Show the plot
plt.show()



### Diffrences between Scores Assignments

# Sort the DataFrame by 'average_rating' and 'wilson_score'
sorted_by_rating = wilson.sort_values(by='average_rating', ascending=False)
sorted_by_wilson = wilson.sort_values(by='adjusted_wilson', ascending=False)


# Calculate the difference between adjusted Wilson score and average rating
wilson['score_difference'] = wilson['adjusted_wilson'] - wilson['average_rating']

# Calculate the average difference
average_difference = wilson['score_difference'].mean()

print(f'Average Difference: {average_difference}')


# Select top and bottom games for each criterion
# Calculate the difference between adjusted Wilson score and average rating for top 20 games
top_20_avg = wilson.sort_values(by='average_rating', ascending=False).head(20)
top_20_avg['score_difference'] = top_20_avg['adjusted_wilson'] - top_20_avg['average_rating']
dif_top_20_avg = top_20_avg['score_difference'].mean()
print(f'Average Difference (Top 20 Avg Rating): {dif_top_20_avg}')

top_200_avg = wilson.sort_values(by='average_rating', ascending=False).head(200)
top_200_avg['score_difference'] = top_200_avg['adjusted_wilson'] - top_200_avg['average_rating']
dif_top_200_avg = top_200_avg['score_difference'].mean()
print(f'Average Difference (Top 200 Avg Rating): {dif_top_200_avg}')

top_2000_avg = wilson.sort_values(by='average_rating', ascending=False).head(2000)
top_2000_avg['score_difference'] = top_2000_avg['adjusted_wilson'] - top_2000_avg['average_rating']
dif_top_2000_avg = top_2000_avg['score_difference'].mean()
print(f'Average Difference (Top 2000 Avg Rating): {dif_top_2000_avg}')

# Calculate the difference between adjusted Wilson score and average rating for bottom 20 games
bottom_20_avg = wilson.sort_values(by='average_rating').head(20)
bottom_20_avg['score_difference'] = bottom_20_avg['adjusted_wilson'] - bottom_20_avg['average_rating']
dif_bottom_20_avg = bottom_20_avg['score_difference'].mean()
print(f'Average Difference (Bottom 20 Avg Rating): {dif_bottom_20_avg}')

bottom_200_avg = wilson.sort_values(by='average_rating').head(200)
bottom_200_avg['score_difference'] = bottom_200_avg['adjusted_wilson'] - bottom_200_avg['average_rating']
dif_bottom_200_avg = bottom_200_avg['score_difference'].mean()
print(f'Average Difference (Bottom 200 Avg Rating): {dif_bottom_200_avg}')

bottom_2000_avg = wilson.sort_values(by='average_rating').head(2000)
bottom_2000_avg['score_difference'] = bottom_2000_avg['adjusted_wilson'] - bottom_2000_avg['average_rating']
dif_bottom_2000_avg = bottom_2000_avg['score_difference'].mean()
print(f'Average Difference (Bottom 2000 Avg Rating): {dif_bottom_2000_avg}')


### Visualising both methods, how do they compare ?
# Select top and bottom games for each criterion
a_20 = sorted_by_rating.head(20)
w_20 = sorted_by_wilson.head(20)


a_200 = sorted_by_rating.head(200)
w_200 = sorted_by_wilson.head(200)


# Top 20
# Create a figure and axis
fig, ax1 = plt.subplots(figsize=(12, 6))
bar_width = 0.4
index = np.arange(len(a_20['game']))

# Plot bar chart for top average ratings on the primary y-axis
ax1.bar(index, a_20['average_rating'], width=bar_width, label='Top Avg Rating', color='blue')
ax1.set_xlabel('Game')
ax1.set_ylabel('Average Rating', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.set_xticks(index + bar_width / 2)
ax1.set_xticklabels([])

# Set y-axis limits for top average ratings
ax1.set_ylim(8.5, 10)

# Create a secondary y-axis for top Wilson scores
ax2 = ax1.twinx()
ax2.bar(index + bar_width, w_20['adjusted_wilson'], width=bar_width, label='Top Wilson Score', color='orange')
ax2.set_ylabel('Wilson Score', color='orange')
ax2.tick_params(axis='y', labelcolor='orange')

# Set y-axis limits for top Wilson scores
ax2.set_ylim(8.5, 10)

# Title and legend
plt.title('Figure 5 : Comparison of Top Average Ratings and Top Wilson Scores : 20 top average user-rated ')
fig.tight_layout()

# Show the plot
plt.show()



## Top 200
# Create a figure and axis
fig, ax1 = plt.subplots(figsize=(12, 6))
bar_width = 0.5
index = np.arange(len(La_200['game']))

# Plot bar chart for top average ratings on the primary y-axis
ax1.bar(index, a_200['average_rating'], width=bar_width, label='Top Avg Rating', color='blue')
ax1.set_xlabel('Game')
ax1.set_ylabel('Average Rating', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.set_xticks(index + bar_width / 2)
ax1.set_xticklabels([])

# Set y-axis limits for top average ratings
ax1.set_ylim(8.5, 10)

# Create a secondary y-axis for top Wilson scores
ax2 = ax1.twinx()
ax2.bar(index + bar_width, w_200['adjusted_wilson'], width=bar_width, label='Top Wilson Score', color='orange')
ax2.set_ylabel('Wilson Score', color='orange')
ax2.tick_params(axis='y', labelcolor='orange')

# Set y-axis limits for top Wilson scores
ax2.set_ylim(8.5, 10)

# Title and legend
plt.title('Figure 6 : Comparison of Top Average Ratings and Top Wilson Scores : 200 top average user-rated ')
fig.tight_layout()

# Show the plot
plt.show()


### Wilson Score Performance in Lower Ranked Games
# Get the minimum and maximum values of the bottom Wilson scores
Lw_2000 = sorted_by_wilson.tail(2000)
min_wilson_score = Lw_2000['adjusted_wilson'].min()
max_wilson_score = Lw_2000['adjusted_wilson'].max()

print(f"Minimum Lower Wilson Score: {min_wilson_score}")
print(f"Maximum Lower Wilson Score: {max_wilson_score}")


### Plotting the top 200 Board Games Ranking according their Wilson Scores, then comparing the same 200 games and their Average Ratings

#Top 20
# Create a figure and axis
fig, ax1 = plt.subplots(figsize=(12, 6))

bar_width = 0.4
index = np.arange(len(w_20['game']))

# Plot bar chart for top average ratings on the primary y-axis, sorted by top Wilson scores
ax1.bar(index, w_20['average_rating'], width=bar_width, label='Top Avg Rating', color='teal')
ax1.set_xlabel('Game')
ax1.set_ylabel('Average Rating', color='teal')
ax1.tick_params(axis='y', labelcolor='teal')
ax1.set_xticks(index + bar_width / 2)
ax1.set_xticklabels([])

# Set y-axis limits for top average ratings
ax1.set_ylim(5, 10)

# Create a secondary y-axis for top Wilson scores
ax2 = ax1.twinx()
ax2.bar(index + bar_width, w_20['adjusted_wilson'], width=bar_width, label='Top Wilson Score', color='yellow')
ax2.set_ylabel('Wilson Score', color='yellow')
ax2.tick_params(axis='y', labelcolor='yellow')

# Set y-axis limits for top Wilson scores
ax2.set_ylim(5, 10)

# Title and legend
plt.title('Figure 7 : Comparison of Top Average Ratings and Top Wilson Scores : Top 20 according to their wilson-score ranking')
fig.tight_layout()

# Show the plot
plt.show()




##Top 200
# Create a figure and axis
fig, ax1 = plt.subplots(figsize=(12, 6))

bar_width = 0.45
index = np.arange(len(w_200['game']))

# Plot bar chart for top average ratings on the primary y-axis, sorted by top Wilson scores
ax1.bar(index, w_200['average_rating'], width=bar_width, label='Top Avg Rating', color='teal')
ax1.set_xlabel('Game')
ax1.set_ylabel('Average Rating', color='teal')
ax1.tick_params(axis='y', labelcolor='teal')
ax1.set_xticks(index + bar_width / 2)
ax1.set_xticklabels([])

# Set y-axis limits for top average ratings
ax1.set_ylim(7, 10)

# Create a secondary y-axis for top Wilson scores
ax2 = ax1.twinx()
ax2.bar(index + bar_width, w_200['adjusted_wilson'], width=bar_width, label='Top Wilson Score', color='yellow')
ax2.set_ylabel('Wilson Score', color='yellow')
ax2.tick_params(axis='y', labelcolor='yellow')

# Set y-axis limits for top Wilson scores
ax2.set_ylim(7, 10)

# Title and legend
plt.title('Figure 8 : Comparison of Top Average Ratings and Top Wilson Scores : Top 200 according to their wilson-score ranking')
fig.tight_layout()

# Show the plot
plt.show()