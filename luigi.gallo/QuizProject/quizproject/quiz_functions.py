from numpy import random
import pandas as pd
import time
import plotly.graph_objects as go

earnings_ranges = {
 1: (200000000, float('inf')), # Easy
 2: (50000000, 200000000), # Medium
 3: (10000000, 50000000), # Hard
 4: (0, 10000000) # Extreme
}

difficulty_points = {
 1: 5, # Easy
 2: 10, # Medium
 3: 20, # Hard
 4: 30 # Extreme
}

def __init__(self, df):
  self.df = df
  self.difficulty = self.choose_difficulty()
  self.points = difficulty_points[self.difficulty]
  self.penalty = self.points // 2 # Half of the points for the difficulty level
  self.score = 0

  # Filter the dataframe based on the earnings range for the current difficulty level
  min_earnings, max_earnings = earnings_ranges[self.difficulty]
  self.df_filtered = df[(df['Gross'] >= min_earnings) & (df['Gross'] < max_earnings)]
  
  # Replace non-standard missing values with NaN
  self.df_filtered = self.df_filtered.replace("", "NaN")
  
  # Drop rows with NaN values
  self.df_filtered = self.df_filtered.dropna()

def choose_difficulty(self):
  print("Welcome to IMDBest Quiz!")
  print("Choose your difficulty level:")
  print("1. Easy")
  print("2. Medium")
  print("3. Hard")
  print("4. Extreme")
  while True:
      try:
          difficulty = int(input("Enter a number between 1 and 4: "))
          if 1 <= difficulty <= 4:
            return difficulty
          else:
            print("Invalid choice. Please choose a number between 1 and 4.")
      except ValueError:
          print("Invalid choice. Please enter a number.")

def create_quiz(self):
  random_row = self.df_filtered.sample(1)

  actor = random_row['Star1'].values[0]
  actor2 = random_row['Star2'].values[0]
  director = random_row['Director'].values[0]
  runtime = random_row['Runtime'].values[0]
  genre = random_row['Genre'].values[0].split(',')[0] # Split the genres and select the first one
  year = random_row['Released_Year'].values[0]
  film = random_row['Series_Title'].values[0]

  # Adjust the amount of information based on the difficulty level
  if self.difficulty == 1: # Easy
      question = f"What is the {genre} film directed by {director} starring {actor} and {actor2} released in {year} with a runtime of {runtime}?"
  elif self.difficulty == 2: # Medium
      question = f"What is the {genre} film directed by {director} starring {actor} and {actor2} released in {year}?"
  elif self.difficulty == 3: # Hard
      question = f"What is the {genre} film directed by {director} starring {actor} released in {year}?"
  elif self.difficulty == 4: # Extreme
      question = f"What is the {genre} film directed by {director} starring {actor}"

  choices = [film]
  while len(choices) < 4:
      random_film = self.df_filtered['Series_Title'].sample(1).values[0]
      if random_film not in choices:
          choices.append(random_film)

  random.shuffle(choices)

  return question, choices, film

def play_quiz(self, num_questions=5):
  score_changes = [0] # List to store score changes for each question, starting with 0
  for i in range(num_questions):
      question, choices, correct_answer = self.create_quiz()
      print(question)
      for j, choice in enumerate(choices, start=1):
          print(f"{j}. {choice}")
      time.sleep(1) # Add a small delay
      
      # Get player's choice
      while True:
          answer = int(input("Enter the number of your answer (1-4): "))
          if 1 <= answer <= 4:
            break
          else:
            print("Invalid choice. Please choose a number between 1 and 4.") 
      if choices[answer - 1] == correct_answer:
          print("Correct!")
          self.score += self.points
          score_changes.append(self.score) # Add total score to the list
      else:
          print("Incorrect. The correct answer was", correct_answer)
          self.score -= self.penalty
          score_changes.append(self.score) # Add total score to the list
      if i < num_questions - 1: # If it's not the last question
          print(f"Your current score is {self.score}")

  # Calculate the maximum possible score
  max_score = num_questions * self.points
  if self.score == max_score:
     print(f"Your final score is {self.score}. Congratulations you got a perfect score!")
  else:
     print(f"Your final score is {self.score}")

  # Plot the score changes over time
  fig = go.Figure()
  fig.add_trace(go.Scatter(x=list(range(len(score_changes))), y=score_changes, mode='lines+markers', line=dict(color='red')))
  fig.update_layout(font=dict(family='Arial', size=14))
  fig.update_layout(title= 'Score changes over time', xaxis_title='Time', yaxis_title='Score')
  fig.update_layout(template = 'plotly_white')
  fig.show()
