import pandas as pd
import numpy as np
import plotly.graph_objects as go
from functions import select_difficulty, select_questions
from question import Question
import random

df = pd.read_csv("movies.csv")

class Quiz:
 def __init__(self, df):
     self.df = df
     self.difficulty = select_difficulty()
     self.score = 0
     self.score_changes = []
     self.question = Question(self.df)

 def select_questions(self):
     self.questions = select_questions(self.df, self.difficulty)

 def star_Question(self, question):
     score_change = self.question.star_Question(question, self.difficulty)
     self.score += score_change
     self.score_changes.append(self.score)

 def year_question(self, question):
     score_change = self.question.year_question(question, self.difficulty)
     self.score += score_change
     self.score_changes.append(self.score)

 def start_quiz(self):
     self.select_questions()
     for _, question in self.questions.iterrows():
         method = random.choice([self.star_Question, self.year_question])
         method(question)
     print(f"Your final score is {self.score}/10")

 def plot_score_changes(self):
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
quiz_instance.plot_score_changes()
