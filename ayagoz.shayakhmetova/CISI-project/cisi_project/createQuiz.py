import pandas as pd
import random
import numpy as np

class MovieQuiz:
    def __init__(self, data_movie, difficulty_level, number_questions = 7):
        self.data_movie = data_movie
        self.number_questions = number_questions
        self.difficulty_level = difficulty_level
        self.questions = []
        self.answers = []
        self.correct_indices = []
        self.selected_answers = [None] * self.number_questions
        self.start_quiz()

    #generate questions when difficulty level = easy, question will be randomly chosen between 'tagline'
    #or 'overview' column names
    def generate_easy_question(self):
        random_movie = self.data_movie.sample(1)
        movie_title = random_movie["original_title"].values[0]

        if random.choice([True, False]):
            movie_detail = random_movie["overview"].values[0]
            question = f"What is the name of the movie with the following overview: {movie_detail}"
        else:
            movie_detail = random_movie["tagline"].values[0]
            question = f"What is the name of the movie with the following tagline: {movie_detail}?"

        answer_choices = [movie_title]

        for _ in range(3):
            random_choice = self.data_movie.sample(1)
            incorrect_title = random_choice["original_title"].values[0]
            answer_choices.append(incorrect_title)  

        np.random.shuffle(answer_choices)

        correct_index = answer_choices.index(movie_title)

        return question, answer_choices, correct_index

    #generate questions when difficulty level = medium, question will be formed based on 'original_title'
    #and 'release_date' columns
    def generate_medium_question(self):
        random_movie = self.data_movie.sample(1)
        movie_title = random_movie["original_title"].values[0]
        movie_year = str(random_movie["release_date"].values[0])  

        answer_choices = [movie_year] 

        for _ in range(3):
            random_choice = self.data_movie.sample(1)
            incorrect_year = str(random_choice["release_date"].values[0]) 
            answer_choices.append(incorrect_year) 

        np.random.shuffle(answer_choices)

        correct_index = answer_choices.index(movie_year)

        question = f"What year was the movie '{movie_title}' released in?"

        return question, answer_choices, correct_index
    
    #generate questions when difficulty level = hard, question will be formed based on 'original_title'
    #and 'budget' columns
    def generate_hard_question(self):
        random_movie = self.data_movie.sample(1)
        movie_title = random_movie["original_title"].values[0]
        movie_budget = random_movie["budget"].values[0] 

        answer_choices = [movie_title]

        for _ in range(3):
            random_choice = self.data_movie.sample(1)
            incorrect_title = random_choice["original_title"].values[0] 
            answer_choices.append(incorrect_title) 

        np.random.shuffle(answer_choices)

        correct_index = answer_choices.index(movie_title)

        question = f"What is the name of the movie with the following budget: {movie_budget}?"

        return question, answer_choices, correct_index
    
    def start_quiz(self):
        question_difficulty = None
        if self.difficulty_level == 'easy':
            question_difficulty = self.generate_easy_question
        elif self.difficulty_level == 'medium':
            question_difficulty = self.generate_medium_question
        elif self.difficulty_level == 'hard':
            question_difficulty = self.generate_hard_question

        for _ in range(self.number_questions):
            question, answer_choices, correct_index = question_difficulty()
            self.questions.append(question)
            self.answers.append(answer_choices)
            self.correct_indices.append(correct_index)