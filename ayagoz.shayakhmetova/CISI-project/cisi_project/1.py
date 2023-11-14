import pandas as pd
import numpy as np
import random

data_movie = pd.read_csv("/Users/apple/Documents/GitHub/dscoding-projects/ayagoz.shayakhmetova/CISI-project/cisi_project/tmdb_5000_movies.csv")
data_credits = pd.read_csv("/Users/apple/Documents/GitHub/dscoding-projects/ayagoz.shayakhmetova/CISI-project/cisi_project/tmdb_5000_credits.csv")

def movie_question(data_movie):
    random_movie = data_movie.sample(1) #sample() is used to generate a sample random row or column from the function caller data frame.
    movie_original_title = random_movie["original_title"].values[0] # IndexError: index 1 is out of bounds for axis 0 with size 1 0 rows, 1 columns
    answer_choice = [f"{movie_original_title}"]

    for _ in range (3):
        random_choice = data_movie.sample(1)
        incorrect_original_title = random_choice["original_title"].values[0]
        incorrect_choice = f"{incorrect_original_title}"
        answer_choice.append(incorrect_choice)
    
    random.shuffle(answer_choice)

    correct_index = answer_choice.index(f"{movie_original_title}")
    return f"What is the original title? of '{movie_original_title}'", answer_choice, correct_index

question, choices, correct_index = movie_question(data_movie)
print(question)
for i, choice in enumerate(choices):
    print(f"{i + 1}. {choice}")

player_answer = input("Enter the number of your answer choice: ")

if player_answer.isdigit() and 1 <= int(player_answer) <= 4:
    player_choice = int(player_answer) - 1  # Subtract 1 to match the list index
    if player_choice == correct_index:
        print("Correct! You chose the right answer.")
    else:
        print("Wrong! The correct answer is:", choices[correct_index])
else:
    print("Invalid input. Please enter a number between 1 and 4.")

    
    #print(movie_original_title)

#print(movie_question(data_movie))
#print(data_movie.sample(n=10))