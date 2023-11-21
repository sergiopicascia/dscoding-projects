import pandas as pd
import numpy as np
#this functions let's the user choose the difficulty level
def select_difficulty():
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
      return select_difficulty()
#filter for gross revenue of the film
def select_questions(df, difficulty):
  if difficulty == 'easy':
      df = df.nlargest(10, 'gross')
  elif difficulty == 'medium':
      df = df.nlargest(120, 'gross')
  elif difficulty == 'hard':
      df = df.nlargest(200, 'gross')
  questions = df.sample(10)
  return questions
