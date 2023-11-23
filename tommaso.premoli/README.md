# Movie Quiz

## Dataset
The dataset was obtained from the website kaggle.com (https://www.kaggle.com/code/abdulrahmankhaled1/top-1000-imdb-movie-eda/notebook) and contains 5042 films obtained from IMDB (Internet Movie Database). 
The database refers to an Exploratory Data Analysis (EDA). Through this process, the film data are explored and analysed to better visualise all available information.

### Data Cleaning
First of all, an initial cleaning of the data took place by filtering the columns, keeping only the most important variables for the quiz. The variables that were taken into account are:
- movie_title: original title of the film
- year: year in which the film was produced
- director_name: director's full name
- actor_name: full name of one of the main actors in the film
- genres: genre the film belongs to	
- country: country where the film was produced

After that, a more thorough cleaning was carried out. Genres were put in lower case letters and replaced '|' with ', ' and '. All rows that contained at least one non-existent value (NaN) were deleted. For example, the film called 'Star Wars: The Force Awakens' did not present the year of production in the dataset and was therefore deleted. Finally, the 'year' column was also fixed by converting all numbers to integers.

## Data Visualization
The level of difficulty the player can choose is based on the year the film was produced. For this reason, a histogram was also created to show the player the amount of films released per year. In this way, it can be seen that within the dataset, there is clearly a greater amount of films produced in the early 2000s.

## Quiz Creation
The quiz is organised in this way. The player initially has to choose between two difficulty options: easy or difficult. If he chooses the difficulty "easy", the player has a total of 5 minutes in which to answer questions about films that were categorically made after 1990. On the other hand, the player who chooses the difficulty 'difficult' will have less time, 3 minutes, to answer films produced before 1990. A time criterion was used to assess the complexity of the quiz.
The player has to answer a total of 10 questions.
At the end, he will see his total result and a graph will appear in which the progress of the quiz can be observed. Finally, the player will have the possibility to play several times.
