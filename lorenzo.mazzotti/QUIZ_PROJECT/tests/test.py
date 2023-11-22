import pandas as pd
import numpy as np
import plotly.graph_objects as go

df = pd.read_csv("movies.csv")

class Quiz:
  def __init__(self, df):
      self.df = df
      self.difficulty = self.select_difficulty()
      self.score = 0
      self.score_changes = []

  def select_difficulty(self):
      print("Select a difficulty level:")
      print("1. Easy")
      print("2. Medium")
      print("3. Hard")

      difficulty = input()
      if difficulty == '1':
          return 'easy'
      elif difficulty == '2':
          return 'medium'
      elif difficulty == '3':
          return 'hard'
      else:
          print("Invalid choice. Please select a number between 1 and 3.")
          return self.select_difficulty()

  def select_questions(self):
      if self.difficulty == 'easy':
          self.df = self.df.nlargest(50, 'gross')
      elif self.difficulty == 'medium':
          self.df = self.df.nlargest(12, 'gross')
      elif self.difficulty == 'hard':
          self.df = self.df.nlargest(200, 'gross')
      self.questions = self.df.sample(10)

  def ask_question(self, question):
      df_copy = self.df.copy()
      df_copy = df_copy[df_copy['star'] != question['star']]
      incorrect_stars = df_copy['star'].drop_duplicates().sample(3)
      options = np.append(incorrect_stars, question['star'])
      np.random.shuffle(options)

      if self.difficulty == 'easy':
          print(f"Who was the leading actor of {question['name']} that was written by {question['writer']} and came out in {question['year']}?")
      elif self.difficulty == 'medium':
          print(f"Who was the leading actor of {question['name']} that was written by {question['writer']}?")
      elif self.difficulty == 'hard':
          print(f"Who was the leading actor of {question['name']}?")

      for i, option in enumerate(options, start=1):
          print(f"{i}. {option}")

      answer = int(input())
      if answer == options.tolist().index(question['star']) + 1: 
          if self.difficulty in ['easy', 'medium', 'hard']:
              self.score += 1
              self.score_changes.append(self.score)
      else:
          print(f"Sorry, the correct answer is {options.tolist().index(question['star']) + 1}.")
          self.score -= 0.5
          self.score_changes.append(self.score)

  def start_quiz(self):
     self.select_questions()
     for _, question in self.questions.iterrows():
         self.ask_question(question)
     print(f"Your final score is {self.score}/10")
     
     # Create a line chart of score changes
     fig = go.Figure(data=go.Scatter(
         x=list(range(len(self.score_changes))),
         y=self.score_changes,
         mode='lines'
     ))
     fig.update_layout(title_text='Score changes')
     fig.show()

quiz_instance = Quiz(df)

quiz_instance.start_quiz()