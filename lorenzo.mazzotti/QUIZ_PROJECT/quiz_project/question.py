import pandas as pd
import numpy as np

class Question:
 questions = []

 def __init__(self, df):
     self.df = df
     Question.questions.append(self)

 def star_Question(self, question, difficulty):
     df_copy = self.df.copy()
     df_copy = df_copy[df_copy['star'] != question['star']]
     incorrect_stars = df_copy['star'].drop_duplicates().sample(3)
     options = np.append(incorrect_stars, question['star'])
     np.random.shuffle(options)

     if difficulty == 'easy':
         print(f"Who was the leading actor of {question['name']} that was written by {question['writer']} and came out in {question['year']}?")
     elif difficulty == 'medium':
         print(f"Who was the leading actor of {question['name']} that was written by {question['writer']}?")
     elif difficulty == 'hard':
         print(f"Who was the leading actor of {question['name']}?")

     for i, option in enumerate(options, start=1):
         print(f"{i}. {option}")

     answer = int(input())
     if answer == options.tolist().index(question['star']) + 1: 
         if difficulty in ['easy', 'medium', 'hard']:
             return 1
     else:
         print(f"Sorry, the correct answer is {options.tolist().index(question['star']) + 1}.")
         return -0.5

 def year_question(self, question, difficulty):
     df_copy = self.df.copy()
     df_copy = df_copy[df_copy['year'] != question['year']]
     incorrect_years = df_copy['year'].drop_duplicates().sample(3)
     options = np.append(incorrect_years, question['year'])
     np.random.shuffle(options)

     if difficulty == 'easy':
         print(f"\"{question['name']}\" was written by {question['writer']} and directed by {question['director']} and had a budget of {question['budget']}, when was this film released?")
     elif difficulty == 'medium':
         print(f"\"{question['name']}\" was written by {question['writer']} and directed by {question['director']}, when was this film released?")
     elif difficulty == 'hard':
         print(f"\"{question['name']}\" was written by {question['writer']}, when was this film released?")

     for i, option in enumerate(options, start=1):
         print(f"{i}. {option}")

     answer = int(input())
     if answer == options.tolist().index(question['year']) + 1: 
         if difficulty in ['easy', 'medium', 'hard']:
             return 1
     else:
         print(f"Sorry, the correct answer is {options.tolist().index(question['year']) + 1}.")
         return -0.5
     
