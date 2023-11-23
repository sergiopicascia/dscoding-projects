from data_manager import DataManager
from quiz import Quiz

try:
    # Establishing connection to the IMDb database
    imdb_data = DataManager(
        dbname='imdb',
        user='samaher',
        password="CodingIsFun++",
        host='localhost',
        port='5432'
    )

    # Getting the movie data from the database
    movie_data = imdb_data.get_movie()

    # Creating a Quiz instance with the movie data
    quiz = Quiz(movie_data)

    # Running the quiz
    quiz.run_quiz()

finally:
    # Ensuring the database connection is closed
    if 'imdb_data' in locals():
        imdb_data.close_connection()