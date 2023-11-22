## Board game project
The objective of this project is to generate a user preference-based ranking of 
games sourced from the [BoardGameGeek (BGG) website](https://boardgamegeek.com/). Users have the ability to allocate a 
score ranging from 0 to 10 to express their liking for each game.

### Dataset
This [dataset](https://island.ricerca.di.unimi.it/~alfio/shared/bgg.csv.zip)
includes comments for almost 30,000 games. To enhance program efficiency,
I will be working with a subset of just over 2,000 board games, 
taking into account only the first 100,000 rows of the dataset.
It is possible to consider the entirety of the games by adjusting 
the number of rows in the provided code:`Bgg = Bgg[0:100000]`

It should be noted that in the dataset, the number of ratings 
for each game is lower, sometimes by several hundred, compared to those on the website. 
Therefore, some adjustments are necessary, and as a result, 
the averages cannot be directly compared to those provided by the official ranking.  

### Project 
This project, fully contained within `Board game.py`, consists of two main components: 
the first involves the generation of potential rankings using various types of ratings, 
and the second part focuses on the comparison of these methods through graphical representation.

#### Class Rating 
This initial segment enables the computation of three distinct rankings:

- *Average rating:* 
It calculates the arithmetic mean of the scores for each game. However, this method does 
not account for variations in the number of votes, hence the need to explore additional ranking methods.
- *Geek rating:* This method mirrors the approach used in the official BGG ranking. According to the 
[website](https://boardgamegeek.com/thread/1702432/what-geek-rating), it involves 
introducing artificial dummy votes with a score of 5.5. This has a minor impact on the
average for games with a high number of votes but can significantly influence games
with fewer votes. The intention is to prevent games with only a handful of votes 
from disproportionately influencing the top rankings,  ensuring that games with 
more votes, even if some of them are low, receive fair consideration. The website 
typically adds 100 artificial votes for each game, but due to the limited number of 
comments in this dataset compared to the site, only 5 artificial votes have been added.
- *New rating:* 
The final approach is known as Bayesian approximation, recognized as a highly effective method 
for ranking items assessed on a K-star scale. Unlike other methods, this formula takes into account 
not just the overall quantity of ratings but also the distribution of votes across each potential 
value on the scale. 
A comprehensive explanation, along with the complete formula, can be found on this
[website](https://www.evanmiller.org/ranking-items-with-star-ratings.html).
 
At the end of this first section, it is possible to visualize results in a table based on 
the chosen rating method. Additionally, you can obtain information 
about a specific game or find out which game is in a particular position in the ranking.

#### Class graphs 
In the second part, it is possible to compare 
different rating methods and visualize the results through three graphs:
- *Comparison plot:* When using a specific rating method, users can observe, for each 
position in the corresponding ranking, the assigned value for the game in that position,
along with the values calculated through alternative methods. 
This highlights the existence of distinct rankings based on the chosen method.
- *Scatter plot:* This graph enables users to visualize the distribution of games on a Cartesian
plane. Users can observe whether there is a 
correlation between the number of votes and the average value.
It's also possible to select one or more methods for display on the graph.
- *Pie chart:* This final chart shows the percentage of games in 
different ranking categories. Each slice represents a specific ranking, 
giving a quick and clear picture of how many games are in each category.
