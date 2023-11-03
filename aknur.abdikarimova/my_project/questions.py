import pandas as pd
import random

#load the dataset
path_movies='movies.csv'
movies=pd.read_csv(path_movies)

# Function creates automatically generated question about director

def q_director():
   
    # Randomly select a movie
    chosen_movie = movies.sample(1).iloc[0]

    # Add the correct answer
    correct_dir = chosen_movie['director']

    # Add three wrong answers
    wrongs = movies[movies['director'] != correct_dir]['director'].sample(3).tolist()

    # Shuffle all options
    options = [correct_dir] + wrongs
    random.shuffle(options)

    # Create the quiz question
    question = f"Who is the director of {chosen_movie['name']}?"
    return question, options, correct_dir

def ask_question(question, options, correct_dir):
    print(question)
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")

    # Player's answer
    try:
        user_answer = int(input("\nPlease select your answer (1-4): "))

        # Validate user input
        if 1 <= user_answer <= 4:
            if options[user_answer - 1] == correct_dir:
                print("You are great!")
            else:
                print(f"You were very close! But, the correct answer is: {correct_dir}")
        else:
            print("Oops! Please choose a number between 1 and 4.")
    except ValueError:
        print("Please enter a valid number (1-4)!")


#just for test:
question, options, correct_dir = q_director()
ask_question(question, options, correct_dir)