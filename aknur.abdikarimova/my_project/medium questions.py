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


def q_star():
       
    # Randomly select a movie
    selected_movie = movies.sample(1).iloc[0]
    movie_name = selected_movie['name']
    correct_star = selected_movie['star']

    # Get three other incorrect options
    incorrect_stars = movies[movies['star'] != correct_star]['star'].drop_duplicates().sample(3).tolist()

    # Combine the correct answer with the incorrect options
    options = [correct_star] + incorrect_stars
    random.shuffle(options)  # Shuffle the options

    # Present the question and options
    print(f"Who starred in the movie '{movie_name}'?")
    for idx, option in enumerate(options, start=1):
        print(f"{idx}. {option}")

    # Get a player's answer
    try:
        user_answer = int(input("Enter the option number of your answer: "))
        if options[user_answer - 1] == correct_star:
            print("Correct!")
        else:
            print(f"Wrong! The correct answer was: {correct_star}")
    except (ValueError, IndexError):
        print("Invalid input. Please enter the number corresponding to your answer.")

q_star()

def q_company():
       
    # Randomly select a movie
    selected_movie = movies.sample(1).iloc[0]
    movie_name = selected_movie['name']
    correct_company = selected_movie['company']

    # Get three other unique incorrect options
    incorrect_companies = movies[movies['company'] != correct_company]['company'].drop_duplicates().sample(3).tolist()

    # Combine the correct answer with the incorrect options
    options = [correct_company] + incorrect_companies
    random.shuffle(options)  # Shuffle the options

    # Present the question and options
    print(f"What company released the movie '{movie_name}'?")
    for idx, option in enumerate(options, start=1):
        print(f"{idx}. {option}")

    # Get player's answer
    try:
        user_answer = int(input("Enter the option number of your answer: "))
        if options[user_answer - 1] == correct_company:
            print("Correct!")
        else:
            print(f"Wrong! The correct answer was: {correct_company}")
    except (ValueError, IndexError):
        print("Invalid input. Please enter the number corresponding to your answer.")

q_company()

def q_country():
    
    # Randomly select a movie
    selected_movie = movies.sample(1).iloc[0]
    movie_name = selected_movie['name']
    correct_country = selected_movie['country']

    # Get three other unique incorrect options
    incorrect_countries = movies[movies['country'] != correct_country]['country'].drop_duplicates().sample(3).tolist()

    # Combine the correct answer with the incorrect options
    options = [correct_country] + incorrect_countries
    random.shuffle(options)  # Shuffle the options

    # Present the question and options
    print(f"Choose the country that released the movie '{movie_name}':")
    for idx, option in enumerate(options, start=1):
        print(f"{idx}. {option}")

    # Get player's answer
    try:
        user_answer = int(input("Enter the option number of your answer: "))
        if options[user_answer - 1] == correct_country:
            print("Correct!")
        else:
            print(f"Wrong! The correct answer was: {correct_country}")
    except (ValueError, IndexError):
        print("Invalid input. Please enter the number corresponding to your answer.")

q_country()

