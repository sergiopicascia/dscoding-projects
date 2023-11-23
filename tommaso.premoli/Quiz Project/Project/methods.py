import pandas as pd
from numpy import random
import string
import matplotlib.pyplot as plt
import time

"""
A class for a movie quiz game, which allows users to play a movie quiz game. The game involves answering questions
related to movie characteristics, such as release year, director, actors, country, and genre. The quiz has also a time
limit, and the user's score is displayed at the end.
"""

class play_quiz:
    """
    Constructor method to initialize the play_quiz object with the import and data cleaning (Performing tasks such as
    converting genres to lowercase, formatting genre entries, removing NaN values, and transforming the 'year' column
    into numeric format) functions.
    """
    def __init__(self, movies_file_path):
        self.ID = ['A', 'B', 'C', 'D']
        self.score_history = [0]
        self.movies = pd.read_excel(movies_file_path)
        self.movies['genres'] = self.movies['genres'].str.lower()
        self.movies['genres'] = self.movies['genres'].apply(self.format_genres)
        self.movies.dropna(inplace=True)
        self.movies['year'] = pd.to_numeric(self.movies['year'], errors='coerce').fillna(0).astype(int)

    """
    Formats movie genres for display.
    """
    def format_genres(self, genres):
        genres = genres.split('|')
        if len(genres) > 1:
            genres = ', '.join(genres[:-1]) + ' and ' + genres[-1]
        else:
            genres = genres[0]
        return genres

    """
    It gives the player a choice between easy and difficult difficulty. There will be have a difficulty filter and a 
    time limit.
    """
    def choose_difficulty(self):
        difficulty = input("Choose your difficulty level (Easy/Difficult): ").lower()
        if difficulty == 'easy':
            return self.movies['year'] > 1990, 5 * 60
        elif difficulty == 'difficult':
            return self.movies['year'] < 1990, 3 * 60
        else:
            print("Invalid choice, defaulting to Easy")
            return self.movies['year'] > 1990, 5 * 60


    """
    It is the function for generating the demand by providing the correct attributes of an individual film.
    """
    def generate_question(self, difficulty_filter):
        correct_movie = self.movies[difficulty_filter].sample(1)
        question = f"What is the title of the film released in {correct_movie['year'].values[0]} directed by {correct_movie['director_name'].values[0]}, starring {correct_movie['actor_name'].values[0]}, produced in {correct_movie['country'].values[0]} and belonging to the genre {correct_movie['genres'].values[0]}?"
        return question, correct_movie

    """
    It is the function for generating three wrong answers and one correct answer. The player will see the answers 
    arranged randomly.
    """
    def generate_answers(self, correct_movie):
        incorrect_movies = self.movies.drop(correct_movie.index.values.tolist())
        incorrect_answers = incorrect_movies.sample(3)['movie_title'].values
        correct_answer = correct_movie['movie_title'].values[0]
        answers = [correct_answer] + list(incorrect_answers)
        random.shuffle(answers)
        return answers

    """
    It is the function to run the quiz, showing the question, the four answers and giving the player the chance to 
    choose the correct one. The function will show the result at the end.
    """
    def play_quiz(self):
        difficulty_filter, time_limit = self.choose_difficulty()
        start_time = time.time()
        score = 0

        for i in range(1, 11):
            elapsed_time = time.time() - start_time
            remaining_time = max(0, time_limit - elapsed_time)
            print(f"\nTime remaining: {int(remaining_time // 60)} minutes {int(remaining_time % 60)} seconds\n")

            question, correct_movie = self.generate_question(difficulty_filter)
            answers = self.generate_answers(correct_movie)
            print(f"Question {i}. {question}")

            for j, answer in zip(self.ID, answers):
                print(f"{j}. {answer}")

            user_answer = input("Your answer: ").upper()
            while user_answer not in self.ID:
                print("You have another chance, try again!")
                user_answer = input("Your answer: ").upper()

            correct_answer = correct_movie['movie_title'].values[0]
            selected_answer = answers[string.ascii_uppercase.index(user_answer)]
            if selected_answer == correct_answer:
                print("Correct!\n")
                score += 1
                self.score_history.append(score)
            else:
                print(f"Wrong! The correct answer is {correct_answer}\n")
                self.score_history.append(score)

            elapsed_time = time.time() - start_time
            if elapsed_time > time_limit:
                print("Time's up!")
                break

        print(f"\nYour total score is {score}/10!\n")
        plt.plot(self.score_history)
        plt.xlabel('Question number')
        plt.ylabel('Score')
        plt.title('Score over time')
        plt.ylim(0, 10)
        plt.show()
        retry = input("Do you want to retry? (yes/no): ").lower()
        if retry != 'no':
            self.play_quiz()
        else:
            print("\nThanks for trying!")

