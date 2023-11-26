import pandas as pd
from quiz_functions import __init__, choose_difficulty, create_quiz, play_quiz

class Quiz:
   __init__ = __init__
   choose_difficulty = choose_difficulty
   create_quiz = create_quiz
   play_quiz = play_quiz

# Start Quiz
df = pd.read_csv(r'\Users\Asus\Desktop\QuizProject\quizproject\imdb_top_1000.csv')
df['Gross'] = df['Gross'].str.replace(',', '').astype(float)
quiz = Quiz(df)

while True:
     quiz.play_quiz()
     play_again = input("Do you want to play again? (Yes/No): ")
     if play_again.lower() != 'yes':
         break
