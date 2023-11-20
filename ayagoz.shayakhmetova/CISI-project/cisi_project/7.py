import pandas as pd
import random
import numpy as np

class MovieQuiz:
    def __init__(self, movie_data, num_questions=5):
        self.movie_data = movie_data
        self.num_questions = num_questions
        self.total_points = 0 
        self.difficulty_level = None

    def generate_easy_question(self):
        random_movie = self.movie_data.sample(1)
        movie_title = random_movie["original_title"].values[0]

        if random.choice([True, False]):
            movie_detail = random_movie["overview"].values[0]
            question = f"What is the name of the movie with the following overview: {movie_detail}"
        else:
            movie_detail = random_movie["tagline"].values[0]
            question = f"What is the name of the movie with the following tagline: {movie_detail}?"

        answer_choices = [movie_title]

        for _ in range(3):
            random_choice = self.movie_data.sample(1)
            incorrect_title = random_choice["original_title"].values[0]
            answer_choices.append(incorrect_title)  

        np.random.shuffle(answer_choices)

        correct_index = answer_choices.index(movie_title)

        return question, answer_choices, correct_index

    def generate_medium_question(self):
        random_movie = self.movie_data.sample(1)
        movie_title = random_movie["original_title"].values[0]
        movie_year = str(random_movie["release_date"].values[0])  

        answer_choices = [movie_year] 

        for _ in range(3):
            random_choice = self.movie_data.sample(1)
            incorrect_year = str(random_choice["release_date"].values[0]) 
            answer_choices.append(incorrect_year) 

        np.random.shuffle(answer_choices)

        correct_index = answer_choices.index(movie_year)

        question = f"What year was the movie '{movie_title}' released in?"

        return question, answer_choices, correct_index

    def generate_hard_question(self):
        random_movie = self.movie_data.sample(1)
        movie_title = random_movie["original_title"].values[0]
        movie_budget = random_movie["budget"].values[0] 

        answer_choices = [movie_title]

        for _ in range(3):
            random_choice = self.movie_data.sample(1)
            incorrect_title = random_choice["original_title"].values[0] 
            answer_choices.append(incorrect_title) 

        np.random.shuffle(answer_choices)

        correct_index = answer_choices.index(movie_title)

        question = f"What is the name of the movie with the following budget: {movie_budget}?"

        return question, answer_choices, correct_index

    def calculate_points(self, player_choice, correct_index):
        if player_choice == correct_index:
            self.total_points += 1 

    def choose_difficulty_level(self):
        while True:
            difficulty_level = input("Choose difficulty level (easy, medium, hard): ").lower()
            if difficulty_level in ['easy', 'medium', 'hard']:
                self.difficulty_level = difficulty_level
                break
            else:
                print("Enter difficulty level properly, choose from the following options: easy, medium, hard")

    def start_quiz(self):
        self.choose_difficulty_level() 

        for _ in range(self.num_questions):
            if self.difficulty_level == 'easy':
                question, choices, correct_index = self.generate_easy_question()
            elif self.difficulty_level == 'medium':
                question, choices, correct_index = self.generate_medium_question()
            elif self.difficulty_level == 'hard':
                question, choices, correct_index = self.generate_hard_question()

            while True:
                print(question)
                for i, choice in enumerate(choices):
                    print(f"{i + 1}. {choice}")

                player_answer = input("Enter the number of your answer choice: ")

                if player_answer.isdigit() and 1 <= int(player_answer) <= 4:
                    player_choice = int(player_answer) - 1
                    self.calculate_points(player_choice, correct_index) 

                    if player_choice == correct_index:
                        print("Correct! You chose the right answer.", '\n')
                    else:
                        print("Wrong! The correct answer is:", choices[correct_index], '\n')
                    break
                else:
                    print("Invalid input. Please enter a number between 1 and 4.", '\n')

    def get_total_points(self):
        return self.total_points

if __name__ == "__main__":
    movies_df = pd.read_csv("/Users/apple/Documents/GitHub/dscoding-projects/ayagoz.shayakhmetova/CISI-project/cisi_project/new_movies_1.csv")

    quiz = MovieQuiz(movies_df, num_questions=5)
    quiz.start_quiz()
    total_points = quiz.get_total_points()
    print(f"Total points: {total_points}")
