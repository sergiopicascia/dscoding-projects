
import matplotlib.pyplot as plt
import pandas as pd
import random
import tkinter as tk
from tkinter import messagebox

def q_rating(file_path):

    # Load the dataset
    df = pd.read_csv(file_path)

    # Select 10 random movies
    sample_movies = df.sample(10)

    # Create and display a bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(sample_movies['name'], sample_movies['score'], color='skyblue')
    plt.xlabel('Movie Name')
    plt.ylabel('Rating Score')
    plt.xticks(rotation=45, ha='right')
    plt.title('What movie has the highest rating?')
    plt.tight_layout()
    plt.show()

    # Get the movie with the highest rating
    highest_rated_movie = sample_movies.loc[sample_movies['score'].idxmax()]['name']

    # Select 3 other movies as wrong answers
    wrong_answers = sample_movies[sample_movies['name'] != highest_rated_movie].sample(3)['name'].tolist()

    # Combine correct and wrong answers and shuffle
    answers = wrong_answers + [highest_rated_movie]
    random.shuffle(answers)

    # Create a Tkinter window for the quiz
    root = tk.Tk()
    root.title("Movie Quiz")

    # Label for the question
    question_label = tk.Label(root, text="What movie has the highest rating?")
    question_label.pack()

    # Function to check the answer
    def check_answer(selected_answer):
        if selected_answer == highest_rated_movie:
            messagebox.showinfo("Result", "Correct! The highest rated movie is " + highest_rated_movie)
        else:
            messagebox.showinfo("Result", "Incorrect! The highest rated movie is " + highest_rated_movie)
        root.destroy()

    # Create buttons for each answer
    for answer in answers:
        answer_button = tk.Button(root, text=answer, command=lambda ans=answer: check_answer(ans))
        answer_button.pack()

    # Run the Tkinter loop
    root.mainloop()

    return highest_rated_movie

# Usage
file_path = 'movies.csv'
correct_answer = q_rating(file_path)

print("The correct answer is:", correct_answer)