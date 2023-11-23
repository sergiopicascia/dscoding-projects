# "Movie quiz" project
Purpose of a project is creation of a multiple-choice film-related quiz, exploiting data. 
Movie quiz must fulfill following conditions:
 - quiz generates 1 question and 4 answers where only one is correct answer;
 - quiz must have different difficulty levels;
 - quiz must calculate points scored by the player.

## Used dataset and cleaning process
Because dataset provided by [IMDb](https://www.imdb.com/) is to difficult for my computer to load. I used [TMDB 5000 Movie dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata).
Originally dataset consists of the **4801** rows and **20** columns: budget, genres, homepage, id, keywords, original_language, original_title, overview, popularity, production_companies, production_countries, release_date, revenue, runtime, spoken_languages, status, tagline, title, vote_average, vote_count.
In file *dataModify* I created functions that:
 - load dataset from .csv file;
 - retrieve some basic information, for instance, len(dataset), dataset.head(), dataset.tail();
 - clean_column() that deletes all non-word symbols ('\W'), numeric symbols ('\d'), words "name" and "id" in specified column;
 - drop_column() that deletes specified column;
 - show_incorrect_rows() that shows all rows with '0' or 'NaN' in specified column;
 -  delete_incorrect_rows() that deletes all rows with '0' or 'NaN' in specified column;
 - new_csv() that creates new cleaned dataset.
After several calls of functions attributes of columns were cleaned. Modified dataset with **2983** rows and **19** columns was saved as new .csv file.
In file *cleanData* class CISIData was imported from file dataModify, all modifications and information retrieval were made there.
Initial dataset named "tmdb_5000_movies.csv" -> modified dataset named "new_movies_1.csv"

## Quiz creation process
Quiz creation logic is written in *createQuiz* file.
In this file class MovieQuiz is defined and initialized with 3 default parameters: the movie dataset, difficulty level and the number of questions.
Class MovieQuiz has functions:
 - generate question when difficulty level = 'easy', question will be randomly chosen between 'tagline' or 'overview' column names;
 - generate questions when difficulty level = 'medium', question will be formed based on 'original_title' and 'release_date' columns;
 - generate questions when difficulty level = 'hard', question will be formed based on 'original_title' and 'budget' columns;
 - start quiz based on specified difficulty level, generates and stores the specified number of questions and answer choices.

## Visualization process
Visualization process is written in *visual* file. In this file class VisualData is defined. The class is initialized with a file path pointing to a CSV file containing the dataset. Class VisualData has functions:
 - create line chart based on 'release_date_duplicate' column;
 - create pie chart based on 'runtime' column;
 - create scatter plot based on 'vote_count' and 'vote_average' columns.
 
## Web app creation process
Web app creation process is written in *quizApp* file. In this file class FinalData is defined, it uses the streamlit framework to create a web application. The quiz questions are generated based on a movie dataset, and visualizations of the dataset are displayed, including a line chart, a pie chart, and a scatter plot also is displayed. Class FinalData has functions:
 - start a quiz, check if the quiz has already been started in the session, user selects difficulty level of a quiz, reate a new quiz or reset the existing one based on the selected difficulty level;
 - show question and possible answers as radio buttons. This method displays each quiz question, provides radio buttons for selecting answers, and stores the selected answers in the session state;
 - calculate the quiz score based on the selected answers and correct indices;
 - show the quiz result and the correct answers for each question;
 - collect whole quiz with choosing difficulty level, showing question and showing final score with correct answers;
 - show visualisation data of dataset;
 - main function that creates an instance of the class FinalData, initializes it with the file path to the movie dataset, and then shows both the quiz and visualizations sections in a Streamlit web application.