import pandas as pd
import numpy as np

df = pd.read_csv("movies.csv")

#creating a Quiz class to manage the quiz
class Quiz:
   def __init__(self, df):
       self.df = df
       self.difficulty = self.select_difficulty()
       self.score = 0

#asking the user for the difficoulty level
   def select_difficulty(self):
       print("Select a difficulty level:")
       print("1. Easy")
       print("2. Medium")
       print("3. Hard")

       #user input for the difficulty level
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

#filter for the dataset on difficulty level
   def select_questions(self):
       if self.difficulty == 'easy':
           self.df = self.df.nlargest(30, 'gross')
       elif self.difficulty == 'medium':
           self.df = self.df.nlargest(60, 'gross')
       elif self.difficulty == 'hard':
           self.df = self.df.nlargest(100, 'gross')
           #number of questions asked 
       self.questions = self.df.sample(1)

#first question -> leading actor
   def ask_question(self, question):
       #here we create a copy of the data so we can exclude the correct answer without modifying the original
       df_copy = self.df.copy()
       #excluding the correct answer
       df_copy = df_copy[df_copy['star'] != question['star']]

       # Selecting 3 unique random stars from the DataFrame copy
       incorrect_stars = df_copy['star'].drop_duplicates().sample(3)
       #and adding the correct answer to the options and shuffle them
       options = np.append(incorrect_stars, question['star'])
       np.random.shuffle(options)
#print question
       print(f"Who was the leading actor of {question['name']}?")
       for i, option in enumerate(options, start=1):
           print(f"{i}. {option}")
#getting user answer, if correct increase the score in easy, ask next question in medium and hard, if wrong -0.5
       answer = int(input())
       if answer == options.tolist().index(question['star']) + 1:
           if self.difficulty == 'easy':
             self.score += 1
           if self.difficulty in ['medium', 'hard']:
               self.ask_year_question(question, df_copy)
       else:
           print(f"Sorry, the correct answer is {options.tolist().index(question['star']) + 1}.")
           self.score -= 0.5

#second question (year)
   def ask_year_question(self, question, df_copy):
       #copy excluding right answer
       df_copy = df_copy[df_copy['year'] != question['year']]

       # Select 3 unique random incorrect years from the DataFrame copy
       incorrect_years = df_copy['year'].drop_duplicates().sample(3)
       options = np.append(incorrect_years, question['year'])
       np.random.shuffle(options)

       print(f"When was {question['name']} released?")
       for i, option in enumerate(options, start=1):
           print(f"{i}. {option}")

#score +1 only in medium, in hard go ask director question
       answer = int(input())
       if answer == options.tolist().index(question['year']) + 1:
           if self.difficulty == 'medium':
             self.score += 1
           if self.difficulty == 'hard':
               self.ask_director_question(question, df_copy)
       else:
           print(f"Sorry, the correct answer is {options.tolist().index(question['year']) + 1}.")
           self.score -= 0.5

#last question (director)
   def ask_director_question(self, question, df_copy):
       #copy exluding right answer
       df_copy = df_copy[df_copy['director'] != question['director']]

       # Select 3 unique random incorrect directors from the DataFrame copy
       incorrect_directors = df_copy['director'].drop_duplicates().sample(3)
       options = np.append(incorrect_directors, question['director'])
       np.random.shuffle(options)

       print(f"Who is the director of {question['name']}?")
       for i, option in enumerate(options, start=1):
           print(f"{i}. {option}")

#if in hard you respond correctly to all 3 questions related to a movie you get the point otherwise -0,5
       answer = int(input())
       if answer == options.tolist().index(question['director']) + 1:
           self.score += 1
       else:
           print(f"Sorry, the correct answer is {options.tolist().index(question['director']) + 1}.")
           self.score -= 0.5

   def start_quiz(self):
       self.select_questions()
       for _, question in self.questions.iterrows():
           self.ask_question(question)
       print(f"Your final score is {self.score}/10")

# Create an instance of the Quiz class
quiz_instance = Quiz(df)

# Starting the quiz
quiz_instance.start_quiz()