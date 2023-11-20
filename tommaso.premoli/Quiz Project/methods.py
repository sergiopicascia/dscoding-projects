import pandas as pd
from numpy import random
import string
import matplotlib.pyplot as plt
import time

class play_quiz:
    def __init__(self, movies):
        self.movies = movies
        self.score_history = [0]

    def format_genres(self, genres):
        genres = genres.split('|')
        if len(genres) > 1:
            genres = ', '.join(genres[:-1]) + ' and ' + genres[-1]
        else:
            genres = genres[0]
        return genres

    def data_cleaning(self):
        self.movies['genres'] = self.movies['genres'].str.lower()
        self.movies['genres'] = self.movies['genres'].apply(self.format_genres)
        self.movies.dropna(inplace=True)
        self.movies['year'] = pd.to_numeric(self.movies['year'], errors='coerce').fillna(0).astype(int)

    def choose_difficulty(self):
        difficulty = input("Choose your difficulty level (Easy/Difficult): ").lower()
        if difficulty == 'easy':
            return self.movies['year'] > 1990, 5 * 60
        elif difficulty == 'difficult':
            return self.movies['year'] < 1990, 3 * 60
        else:
            print("Invalid choice, defaulting to Easy")
            return self.movies['year'] > 1990, 5 * 60

    def generate_question(self, difficulty_filter):
        correct_movie = self.movies[difficulty_filter].sample(1)
        question = f"What is the title of the film released in {correct_movie['year'].values[0]} directed by {correct_movie['director_name'].values[0]}, starring {correct_movie['actor_name'].values[0]}, produced in {correct_movie['country'].values[0]} and belonging to the genre {correct_movie['genres'].values[0]}?"
        return question, correct_movie

    def generate_answers(self, correct_movie):
        incorrect_movies = self.movies.drop(correct_movie.index.values.tolist())
        incorrect_answers = incorrect_movies.sample(3)['movie_title'].values
        correct_answer = correct_movie['movie_title'].values[0]
        answers = [correct_answer] + list(incorrect_answers)
        random.shuffle(answers)
        return answers

    def run_quiz(self):
        self.data_cleaning()
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

            for j, answer in zip(string.ascii_uppercase, answers):
                print(f"{j}. {answer}")

            user_answer = input("Your answer: ").upper()
            while user_answer not in string.ascii_uppercase:
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
            self.run_quiz()
        else:
            print("\nThanks for trying!")

