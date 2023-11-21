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

    movie_data = imdb_data.get_movie()

    quiz = Quiz(movie_data)

    quiz.run_quiz_game()


finally:
    # Ensuring the database connection is closed
    if 'imdb_data' in locals():
        imdb_data.close_connection()