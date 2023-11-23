import pandas as pd
import numpy as np
import plotly.graph_objects as go
from functions import select_difficulty, select_questions, plot_score_changes, ask_retake
from question import Question
import random

#import data
df = pd.read_csv("movies.csv")
#drop rows with budget 0 
df = df.loc[df['budget'] != 0]
#main class
class Quiz:
 #init
 def __init__(self, df):
    self.df = df
    self.difficulty = select_difficulty()
    self.score = 0
    self.score_changes = []
    self.question = Question(self.df)

 #this is the function that filters the dataset on the difficulty level
 def select_questions(self):
    self.questions = select_questions(self.df, self.difficulty)

 #first possible question from question class
 def star_Question(self, question):
    score_change = self.question.star_Question(question, self.difficulty)
    self.score += score_change
    self.score_changes.append(self.score)

 #second possible question from question class
 def year_question(self, question):
    score_change = self.question.year_question(question, self.difficulty)
    self.score += score_change
    self.score_changes.append(self.score)


 #starting the quiz and selecting randomly one of the questions, diplays the score, linechart and asks the user to retake the quiz.
 def start_quiz(self):
   while True:
     self.select_questions()
     for _, question in self.questions.iterrows():
         method = random.choice([self.star_Question, self.year_question])
         method(question)
     plot_score_changes(self)
     print(f"Your final score is {self.score}/100")
     if not ask_retake():
         break
     self.score = 0
     self.score_changes = []

quiz_instance = Quiz(df)
quiz_instance.start_quiz()
