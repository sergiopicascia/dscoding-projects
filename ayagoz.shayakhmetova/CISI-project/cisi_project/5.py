import pandas as pd
import random
import numpy as np

class MovieQuiz:
    def __init__(self, movie_data, num_questions=2):
        self.movie_data = movie_data
        self.num_questions = num_questions
        self.total_points = 0 

    def generate_movie_question(self):
        random_movie = self.movie_data.sample(1)
        movie_title = random_movie["original_title"].values[0]
        movie_year = str(random_movie["release_date"].values[0]) 
        movie_budget = random_movie["budget"].values[0] 
        movie_overview = random_movie["overview"].values[0]

        answer_choices_year = [movie_year] 
        answer_choices_budget = [movie_title] 
        answer_choices_overview = [movie_overview]

        for _ in range(3):
            random_choice = self.movie_data.sample(1)
            incorrect_year = str(random_choice["release_date"].values[0]) 
            incorrect_title = random_choice["original_title"].values[0] 
            incorrect_budget = random_choice["budget"].values[0]  
            incorrect_overview = random_choice["overview"].values[0]

            answer_choices_year.append(incorrect_year) 
            answer_choices_budget.append(incorrect_title) 
            answer_choices_overview.append(incorrect_overview)

        np.random.shuffle(answer_choices_year)
        np.random.shuffle(answer_choices_budget)
        np.random.shuffle(answer_choices_overview)

        correct_index_year = answer_choices_year.index(movie_year)
        correct_index_budget = answer_choices_budget.index(movie_title)
        correct_index_overview = answer_choices_overview.index(movie_overview)

        question_year = f"What year was the movie '{movie_title}' released?"
        question_budget = f"What movie had this '{movie_budget}'?"
        question_overview = f"What is the name of a movie based on following overview: '{movie_overview}?"

        return question_year, answer_choices_year, correct_index_year, question_budget, answer_choices_budget, correct_index_budget, question_overview, answer_choices_overview, correct_index_overview

    def calculate_points(self, player_choice, correct_index):
        if player_choice == correct_index:
            self.total_points += 1 

    def start_quiz(self):
        for _ in range(self.num_questions):
            question_year, choices_year, correct_index_year, question_budget, choices_budget, correct_index_budget, question_overview, choices_overview, correct_index_overview = self.generate_movie_question()
            
            print(question_year)
            for i, choice in enumerate(choices_year):
                print(f"{i + 1}. {choice}")

            player_answer = input("Enter the number of your answer choice for the release year: ")

            if player_answer.isdigit() and 1 <= int(player_answer) <= 4:
                player_choice = int(player_answer) - 1
                self.calculate_points(player_choice, correct_index_year) 

                if player_choice == correct_index_year:
                    print("Correct! You chose the right answer.", '\n')
                else:
                    print("Wrong! The correct answer is:", choices_year[correct_index_year], '\n')
            else:
                print("Invalid input. Please enter a number between 1 and 4.", '\n')

            print(question_budget)
            for i, choice in enumerate(choices_budget):
                print(f"{i + 1}. {choice}")

            player_answer = input("Enter the number of your answer choice for the movie title related to the budget: ")

            if player_answer.isdigit() and 1 <= int(player_answer) <= 4:
                player_choice = int(player_answer) - 1
                self.calculate_points(player_choice, correct_index_budget) 

                if player_choice == correct_index_budget:
                    print("Correct! You chose the right answer.", '\n')
                else:
                    print("Wrong! The correct answer is:", choices_budget[correct_index_budget], '\n')
            else:
                print("Invalid input. Please enter a number between 1 and 4.", '\n')

            print(question_overview)
            for i, choice in enumerate(choices_overview):
                print(f"{i + 1}. {choice}")

            player_answer = input("Enter the number of your answer choice for the movie title related to the overview: ")

            if player_answer.isdigit() and 1 <= int(player_answer) <= 4:
                player_choice = int(player_answer) - 1
                self.calculate_points(player_choice, correct_index_overview) 

                if player_choice == correct_index_overview:
                    print("Correct! You chose the right answer.", '\n')
                else:
                    print("Wrong! The correct answer is:", choices_overview[correct_index_overview], '\n')
            else:
                print("Invalid input. Please enter a number between 1 and 4.", '\n')

    def get_total_points(self):
        return self.total_points

if __name__ == "__main__":
    movies_df = pd.read_csv("/Users/apple/Documents/GitHub/dscoding-projects/ayagoz.shayakhmetova/CISI-project/cisi_project/new_movies.csv")

    quiz = MovieQuiz(movies_df, num_questions=2)
    quiz.start_quiz()
    total_points = quiz.get_total_points()
    print(f"Total points: {total_points}")
