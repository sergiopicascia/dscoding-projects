import matplotlib.pyplot as plt
import pandas as pd
import random
import tkinter as tk
from tkinter import messagebox

class MovieRating:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = pd.read_csv(self.file_path)

    def display_chart(self):
        sample_movies = self.df.sample(10)
        plt.figure(figsize=(10, 6))
        plt.bar(sample_movies['name'], sample_movies['score'], color='skyblue')
        plt.xlabel('Movie Name')
        plt.ylabel('Rating Score')
        plt.xticks(rotation=45, ha='right')
        plt.title('What movie has the highest rating?')
        plt.tight_layout()
        plt.show()
        return sample_movies

    def generate_quiz(self, sample_movies):
        highest_rated_movie = sample_movies.loc[sample_movies['score'].idxmax()]['name']
        wrong_answers = sample_movies[sample_movies['name'] != highest_rated_movie].sample(3)['name'].tolist()
        answers = wrong_answers + [highest_rated_movie]
        random.shuffle(answers)

        root = tk.Tk()
        root.title("Movie Quiz")

        question_label = tk.Label(root, text="What movie has the highest rating?")
        question_label.pack()

        def check_answer(selected_answer):
            if selected_answer == highest_rated_movie:
                messagebox.showinfo("Result", "Correct! The highest rated movie is " + highest_rated_movie)
            else:
                messagebox.showinfo("Result", "Incorrect! The highest rated movie is " + highest_rated_movie)
            root.destroy()

        for answer in answers:
            answer_button = tk.Button(root, text=answer, command=lambda ans=answer: check_answer(ans))
            answer_button.pack()

        root.mainloop()

        return highest_rated_movie

# Usage
quiz = MovieRating('movies.csv')
sample_movies = quiz.display_chart()
correct_answer = quiz.generate_quiz(sample_movies)

print("The correct answer is:", correct_answer)


class MovieGenre:
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)
        self.movies = self.df[['name', 'genre']].dropna()

    def get_random_movie(self):
        return self.movies.sample()

    def generate_question(self):
        movie = self.get_random_movie()
        correct_genre = movie['genre'].values[0]
        movie_name = movie['name'].values[0]

        all_genres = list(set(self.movies['genre'].unique()))
        if correct_genre in all_genres:
            all_genres.remove(correct_genre)

        wrong_genres = random.sample(all_genres, 3)
        options = [correct_genre] + wrong_genres
        random.shuffle(options)

        print(f"Choose the genre of the movie '{movie_name}':")
        for i, genre in enumerate(options, start=1):
            print(f"{i}. {genre}")

        return correct_genre, options  


    def play_quiz(self):
        correct_answer, options = self.generate_question()
        user_answer = input("Enter your answer (number): ")

        if options[int(user_answer) - 1] == correct_answer:
            print("Correct!")
        else:
            print("Incorrect. The correct genre is:", correct_answer)

# Usage
genre = MovieGenre('movies.csv')
genre.play_quiz()


class MovieYear:
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)
        self.movies = self.df[['name', 'year']].dropna()

    def get_random_movie(self):
        return self.movies.sample()

    def generate_question(self):
        movie = self.get_random_movie()
        correct_year = movie['year'].values[0]
        movie_name = movie['name'].values[0]

        all_years = set(range(correct_year - 10, correct_year + 10))  # Generates a range of years around the correct year
        all_years.discard(correct_year)  # Removes the correct year from the set

        wrong_years = random.sample(list(all_years), 3)
        options = [correct_year] + wrong_years
        random.shuffle(options)

        print(f"Choose the release year of the movie '{movie_name}':")
        for i, year in enumerate(options, start=1):
            print(f"{i}. {year}")

        return correct_year, options

    def play_quiz(self):
        correct_answer, options = self.generate_question()
        user_answer = input("Enter your answer (number): ")

        if options[int(user_answer) - 1] == correct_answer:
            print("Correct!")
        else:
            print("Incorrect. The correct year is:", correct_answer)

# Usage
q_year = MovieYear('movies.csv')
q_year.play_quiz()


class MovieBudget:
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)
        self.selected_movies = self.df[['name', 'budget']].dropna().sample(10)

    def plot_budget_graph(self):
        sorted_movies = self.selected_movies.sort_values('budget')
        plt.step(sorted_movies['name'], sorted_movies['budget'], where='mid')
        plt.xticks(rotation=45, ha='right')
        plt.xlabel('Movie Name')
        plt.ylabel('Budget')
        plt.title('Which movie has the lowest budget?')
        plt.tight_layout()
        plt.show()

    def generate_quiz(self):
        lowest_budget_movie = self.selected_movies.sort_values('budget').iloc[0]
        correct_answer = lowest_budget_movie['name']
        all_names = list(self.df['name'])
        remaining_names = list(set(all_names) - {correct_answer})  
        wrong_answers = random.sample(remaining_names, 3)
        options = [correct_answer] + wrong_answers
        random.shuffle(options)

        def check_answer(selected_option):
            if selected_option == correct_answer:
                result_label.config(text="Correct!")
            else:
                result_label.config(text=f"Incorrect. The correct answer is: {correct_answer}")

        # Tkinter GUI for the quiz
        quiz_window = tk.Tk()
        quiz_window.title("Movie Budget Quiz")
        question_label = tk.Label(quiz_window, text=f"Which movie has the lowest budget?")
        question_label.pack()

        for option in options:
            btn = tk.Button(quiz_window, text=option, command=lambda opt=option: check_answer(opt))
            btn.pack()

        result_label = tk.Label(quiz_window, text="")
        result_label.pack()

        quiz_window.mainloop()

# Usage
budget = MovieBudget('movies.csv')
budget.plot_budget_graph()  # Display the graph
budget.generate_quiz()      # Start the quiz