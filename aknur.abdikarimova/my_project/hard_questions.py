import pandas as pd
import random
import tkinter as tk
from tkinter import messagebox

class Duration:
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)
        self.question = ""
        self.correct_answer = ""
        self.options = []
        self.score = 0
        self.root = tk.Tk()
        self.root.title("Movie Duration Quiz")

    def generate_question(self):
        movie = self.df.sample()
        movie_name = movie['name'].values[0]
        movie_runtime = movie['runtime'].values[0]
        self.question = f"How long does the movie '{movie_name}' last in minutes?"
        self.correct_answer = movie_runtime
        self.options = [movie_runtime]

        while len(self.options) < 4:
            # random runtimes
            random_runtime = random.randint(70, 180)
            if random_runtime not in self.options:
                self.options.append(random_runtime)

        random.shuffle(self.options)

    def ask_question(self):
        def check_answer(user_answer):
            if user_answer == self.correct_answer:
                self.score += 30
                messagebox.showinfo("Result", f"Correct! Your score is now: {self.score}")
            else:
                messagebox.showinfo("Result", f"Wrong. Better luck next time! Your score is: {self.score}")
            self.root.quit()


        label = tk.Label(self.root, text=self.question, font=("Times", 16))
        label.pack(pady=20)

        for option in self.options:
            button = tk.Button(self.root, text=f"{option} minutes", font=("Times", 14), command=lambda opt=option: check_answer(opt))
            button.pack(pady=5)

        window_width = 700
        window_height = 300
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        self.root.mainloop()

duration = Duration('movies.csv')
duration.generate_question()
duration.ask_question()


class HigherRating:
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)
        self.question = ""
        self.correct_answer = ""
        self.options = []
        self.score = duration.score
        self.root = tk.Tk()
        self.root.title("Higher Rating Movie Quiz")

    def generate_question(self):
        chosen_movie = self.df.sample()
        chosen_movie_name = chosen_movie['name'].values[0]
        chosen_movie_score = chosen_movie['score'].values[0]
        
        self.question = f"What movie has a higher rating than the movie '{chosen_movie_name}'?"
        
        higher_rated_movies = self.df[self.df['score'] > chosen_movie_score]

        if higher_rated_movies.empty:
            raise ValueError("No movie found with a higher rating. Please try again.")
        
        correct_movie = higher_rated_movies.sample()
        self.correct_answer = correct_movie['name'].values[0]
        self.options = [self.correct_answer]
        
        while len(self.options) < 4:
            wrong_movie = self.df.sample()
            if wrong_movie['name'].values[0] not in self.options:
                self.options.append(wrong_movie['name'].values[0])

        random.shuffle(self.options)

    def ask_question(self):
        def check_answer(user_answer):
            if user_answer == self.correct_answer:
                self.score += 30
                result_message = f"Correct! Your score is now: {self.score}"
            else:
                result_message = f"Wrong. The correct answer was: '{self.correct_answer}'."
            result_message += f"\nYour score is: {self.score}"            
            messagebox.showinfo("Result", result_message)
            self.root.quit()
        
        label = tk.Label(self.root, text=self.question, font=("Times", 16))
        label.pack(pady=20)
    
        for option in self.options:
            button = tk.Button(self.root, text=option, font=("Times", 14), command=lambda opt=option: check_answer(opt))
            button.pack(pady=5)
        
        window_width = 700
        window_height = 300
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        self.root.mainloop()

higher_rating = HigherRating('movies.csv')
higher_rating.generate_question()
higher_rating.ask_question()


class OldestMovie:
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)
        self.question = "Choose the oldest movie among the given options."
        self.correct_answer = ""
        self.options = []
        self.score = higher_rating.score
        self.root = tk.Tk()
        self.root.title("Oldest Movie Quiz")

    def generate_question(self):
        
        selected_movies = self.df.sample(n=4)        
        sorted_movies = selected_movies.sort_values(by='year')
        self.correct_answer = sorted_movies.iloc[0]['name']
        self.options = sorted_movies['name'].tolist()

    def ask_question(self):
        def check_answer(user_answer):
            if user_answer == self.correct_answer:
                self.score += 30
                result_message = f"Correct! Your score is now: {self.score}"
            else:
                result_message = f"Wrong. The correct answer was: '{self.correct_answer}'."
            result_message += f"\nYour score is: {self.score}"
            messagebox.showinfo("Result", result_message)
            self.root.quit()

        label = tk.Label(self.root, text=self.question, font=("Times", 16))
        label.pack(pady=20)

        for option in self.options:
            button = tk.Button(self.root, text=option, font=("Times", 14), command=lambda opt=option: check_answer(opt))
            button.pack(pady=5)

        window_width = 700
        window_height = 300
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        self.root.mainloop()

oldest_movie = OldestMovie('movies.csv')
oldest_movie.generate_question()
oldest_movie.ask_question()


class MovieBudget:
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)
        self.question = ""
        self.correct_answer = ""
        self.options = []
        self.score = oldest_movie.score
        self.root = tk.Tk()
        self.root.title("Movie Budget Quiz")

    def generate_question(self):
        while True:
            movie = self.df.sample()
            movie_name = movie['name'].values[0]
            movie_budget = movie['budget'].values[0]

            if pd.notna(movie_budget):
                break

        self.question = f"How much money was spent on the movie '{movie_name}'?"
        self.correct_answer = movie_budget
        self.options = [movie_budget]

        while len(self.options) < 4:
            random_budget = random.randint(int(movie_budget * 0.5), int(movie_budget * 1.5))
            if random_budget not in self.options:
                self.options.append(random_budget)

        random.shuffle(self.options)

    def ask_question(self):
        def check_answer(user_answer):
            if user_answer == self.correct_answer:
                self.score += 30
                result_message = f"Correct! Your score is now: {self.score}"
            else:
                result_message = f"Wrong. The correct answer was: ${self.correct_answer}."
            result_message += f"\nYour score is: {self.score}"
            messagebox.showinfo("Result", result_message)
            self.root.quit()

        label = tk.Label(self.root, text=self.question, font=("Times", 16))
        label.pack(pady=20)

        for option in self.options:
            button = tk.Button(self.root, text=f"${option}", font=("Times", 14), command=lambda opt=option: check_answer(opt))
            button.pack(pady=5)

        window_width = 700
        window_height = 300
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        self.root.mainloop()

movie_budget = MovieBudget('movies.csv')
movie_budget.generate_question()
movie_budget.ask_question()

