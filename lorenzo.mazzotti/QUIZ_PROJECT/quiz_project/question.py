import pandas as pd
import numpy as np

#here we define the quiz question
class Question:
 questions = []

 def __init__(self, df):
   self.df = df
   Question.questions.append(self)

#first question - creating a copy of the data. taking out 3 wrong answers that are unique and the right one. user then must select the only right answer
 def star_Question(self, question, difficulty):
   df_copy = self.df.copy()
   df_copy = df_copy[df_copy['star'] != question['star']]
   incorrect_stars = df_copy['star'].drop_duplicates().sample(3)
   options = np.append(incorrect_stars, question['star'])
   np.random.shuffle(options)

   if difficulty == 'easy':
       print(f"Who is the leading actor of {question['name']} that was written by {question['writer']} and came out in {question['year']}?")
   elif difficulty == 'medium':
       print(f"Who is the leading actor of {question['name']} that was written by {question['writer']}?")
   elif difficulty == 'hard':
       print(f"Who is the leading actor of {question['name']}?")

   for i, option in enumerate(options, start=1):
       print(f"{i}. {option}")
#here we handle imputs different from 1-2-3-4
   while True:
       try:
           answer = int(input())
           if 1 <= answer <= 4:
               break
           else:
               print("Enter a number between 1 and 4.")
       except ValueError:
           print("That's not a number! Enter a number between 1 and 4.")
#correct answer +10 wrong answers score is either 0 -5 or -10 depending on difficulty
   if answer == options.tolist().index(question['star']) + 1: 
       if difficulty in ['easy', 'medium', 'hard']:
           return 10
   else:
       correct_star = question['star']
       print(f"Sorry, the correct answer is {correct_star}.")
       if difficulty == 'easy':
        return 0
       if difficulty == 'medium':
        return -5
       if difficulty == 'hard':
        return -10

#second question 
 def year_question(self, question, difficulty):
   df_copy = self.df.copy()
   df_copy = df_copy[df_copy['year'] != question['year']]
   incorrect_years = df_copy['year'].drop_duplicates().sample(3)
   options = np.append(incorrect_years, question['year'])
   np.random.shuffle(options)

   if difficulty == 'easy':
       print(f"{question['name']} was written by {question['writer']} and directed by {question['director']} and had a budget of {question['budget']}, when was this film released?")
   elif difficulty == 'medium':
       print(f"{question['name']} was written by {question['writer']} and directed by {question['director']}, when was this film released?")
   elif difficulty == 'hard':
       print(f"{question['name']} was written by {question['writer']}, when was this film released?")

   for i, option in enumerate(options, start=1):
       print(f"{i}. {option}")

   while True:
       try:
           answer = int(input())
           if 1 <= answer <= 4:
               break
           else:
               print("Enter a number between 1 and 4.")
       except ValueError:
           print("That's not a number! Enter a number between 1 and 4.")

   if answer == options.tolist().index(question['year']) + 1: 
       if difficulty in ['easy', 'medium', 'hard']:
           return 10
   else:
       correct_year = question['year']
       print(f"Sorry, the correct answer is the year {correct_year}.")
       if difficulty == 'easy':
        return 0
       if difficulty == 'medium':
        return -5
       if difficulty == 'hard':
        return -10
