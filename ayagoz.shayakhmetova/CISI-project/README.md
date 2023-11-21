# "Movie quiz" project
Purpose of a project is creation of a multiple-choice film-related quiz, exploiting data. 
Movie quiz must fulfill following conditions:

 - quiz generates 1 question and 4 answers where only one is correct answer;
 - quiz must have different difficulty levels;
 - quiz must calculate points scored by the player.

## Used dataset and cleaning process
Because dataset provided by [IMDb](https://www.imdb.com/) is to difficult for my computer to load. I used [TMDB 5000 Movie dataset](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata).
Originally dataset consists of the **4801** rows and **20** columns: budget, genres, homepage, id, keywords, original_language, original_title, overview, popularity, production_companies, production_countries, release_date, revenue, runtime, spoken_languages, status, tagline, title, vote_average, vote_count.
In file "dataI.py" I created functions:

 - to load dataset from .csv file;
 - retrieve some basic information, for instance, len(dataset), dataset.head(), dataset.tail();
 - clean_column() that deletes all non-word symbols ('\W'), numeric symbols ('\d'), words "name" and "id" in specified column
 - drop_column() that deletes specified column
 - show_incorrect_rows() that shows all rows with '0' or 'NaN' in specified column
 -  delete_incorrect_rows() that deletes all rows with '0' or 'NaN' in specified column
 - new_csv() that creates new cleaned dataset
After several calls of functions attributes of columns were cleaned, 1431 rows were deleted. Modified dataset was saved as new .csv file.