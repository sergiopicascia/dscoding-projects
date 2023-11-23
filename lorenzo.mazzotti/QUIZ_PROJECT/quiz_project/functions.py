import pandas as pd
import numpy as np
import plotly.graph_objects as go

#this functions let's the user choose the difficulty level, it validates the imput and return the chosen difficulty or prompts the user again if he does not write 1/2/3
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
    print("Invalid choice. Select a number between 1 and 3.")
    return select_difficulty()

#filter for gross revenue of the film based on the difficulty level. it then selects 10 random questions from the dataset with the filter applied
def select_questions(df, difficulty):
 if difficulty == 'easy':
    df = df.nlargest(100, 'gross')
 elif difficulty == 'medium':
    df = df.nlargest(200, 'gross')
 elif difficulty == 'hard':
    df = df.nlargest(400, 'gross')
 questions = df.sample(10)
 return questions

# Create a line chart of score changes
def plot_score_changes(quiz_instance):
   # starting from 00
   x_values = [0] + list(range(1, len(quiz_instance.score_changes) + 1))
   y_values = [0] + quiz_instance.score_changes

   fig = go.Figure(data=go.Scatter(
       x=x_values,
       y=y_values,
       mode='lines+markers',
       line_color='purple'
   ))
   fig.update_layout(paper_bgcolor='white') # White background
   fig.update_layout(plot_bgcolor='white') # White plot area background
   fig.update_layout(xaxis=dict(title='Question Number', tickmode='linear', dtick=1)) # displaying all question numbers on x
   fig.update_layout(title_text='Score') 
   fig.show()



#asking the user if they want to retake the quiz. also handles "wrong" responses
def ask_retake():
    while True:
        user_input = input('Would you like to retake the quiz? Type "y" for yes and "n" for no: ')
        if user_input.lower().startswith('y'):
            return True
        elif user_input.lower().startswith('n'):
            print("Thank you for playing!")
            return False
        else:
            print("Please enter either 'y' for yes or 'n' for no.")
