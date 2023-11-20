import streamlit as st
from quiz_st import Quiz
from data_manager import DataManager 

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

# Creating a Quiz instance with the retrieved movie data
quiz = Quiz(movie_data)

# Launching
quiz.quiz_game()


# Ensure the database connection is closed
imdb_data.close_connection()
