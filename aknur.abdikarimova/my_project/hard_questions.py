import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import messagebox

class Duration:
    """    
    The class processes movie runtime data from csv file and creates an automatically generated quiz question
    where a user needs to guess a correct runtime of a randomly selected movie out of 4 options by clicking on button.
    
    Libraries:
    pandas: used for data manipulation
    numpy: used for random selection and shuffling of data   
    Tkinter: used for graphical user interface interactions

    """
    def __init__(self, csv_file):
        """
        The function initializes the class by loading necessary movie data from csv file.
        It sets up the main Tkinter window and titles it.
        The inital score is set to be 0.

        Parameters:
        "csv_file" (str): path to the CSV file containing movie data.

        """
        self.df = pd.read_csv(csv_file)
        self.question = ""
        self.correct_answer = ""
        self.options = []
        self.score = 0
        self.root = tk.Tk()
        self.root.title("Movie Duration Quiz")

    def generate_question(self):
        """
        The function generates a quiz question about movie's runtime by choosing a random movie from the dataset, its respective runtime,
        then by creating other three runtime options through numpy random method in a range between 70 and 180.

        """
        movie = self.df.sample()
        movie_name = movie['name'].values[0]
        movie_runtime = movie['runtime'].values[0]
        self.question = f"How long does the movie '{movie_name}' last?"
        self.correct_answer = movie_runtime
        self.options = [movie_runtime]

        while len(self.options) < 4:            
            random_runtime = np.random.randint(70, 180)
            if random_runtime not in self.options:
                self.options.append(random_runtime)

        np.random.shuffle(self.options)

    def ask_question(self):
        """
        The function displays the quiz question and its options in a Tkinter window 
        and manages user interaction, scoring, and shows the result.

        """
        def check_answer(user_answer):
            """
            The function checks if user's choice is correct and displays current score. The correct answer rises the score by 30 points.
            If the chosen answer is incorrect it shows the correct answer.

            """
            if user_answer == self.correct_answer:
                self.score += 30
                messagebox.showinfo("Result", f"Correct! Your score is now: {self.score}")
            else:
                messagebox.showinfo("Result", f"Incorrect! The correct answer is {self.correct_answer} minutes. \nYour score is: {self.score}")
            self.root.destroy()

        label = tk.Label(self.root, text=self.question, font=("Times", 16))
        label.pack(pady=20)

        for option in self.options:
            button = tk.Button(self.root, text=f"{option} minutes", font=("Times", 14), command=lambda opt=option: check_answer(opt))
            button.pack(pady=5)

        # script to set size of Tkinter window and to centralize it on the screen
        window_width = 800
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        self.root.mainloop()

# usage of the class
duration = Duration('movies.csv')
duration.generate_question()
duration.ask_question()


class HigherRating:
    """    
    The class processes movie rating data from csv file and creates an automatically generated quiz question
    where a user needs to guess a movie that has a higher rating than a randomly selected movie out of 4 options by clicking on button.
    
    Libraries:
    pandas: used for data manipulation
    numpy: used for random selection and shuffling of data   
    Tkinter: used for graphical user interface interactions

    """
    def __init__(self, csv_file):
        """
        The function initializes the class by loading necessary movie data from csv file.
        It sets up the main Tkinter window and titles it.
        The inital score depends on output score of the class Duration.

        Parameters:
        "csv_file" (str): path to the CSV file containing movie data.

        """
        self.df = pd.read_csv(csv_file)
        self.question = ""
        self.correct_answer = ""
        self.options = []
        self.score = duration.score
        self.root = tk.Tk()
        self.root.title("Higher Rating Movie Quiz")

    def generate_question(self):
        """
        The function selects a random movie from the dataset and generates a quiz question. 
        It finds movies with higher ratings than the selected movie and chooses one as the correct answer,
        and provides other three options with movie names that have lower rating than the selected movie.
        Raiese "ValueErroe" if no movie is found with a higher rating than the selected movie.

        """
        chosen_movie_index = np.random.choice(self.df.index)
        chosen_movie = self.df.loc[chosen_movie_index]
        chosen_movie_name = chosen_movie['name']
        chosen_movie_score = chosen_movie['score']
        
        self.question = f"What movie has a higher rating than the movie '{chosen_movie_name}'?"
        
        higher_rated_movies = self.df[self.df['score'] > chosen_movie_score]

        if higher_rated_movies.empty:
            raise ValueError("No movie found with a higher rating. Please try again.")
        
        correct_movie_index = np.random.choice(higher_rated_movies.index)
        self.correct_answer = higher_rated_movies.loc[correct_movie_index, 'name']
        self.options = [self.correct_answer]
        
        while len(self.options) < 4:
            wrong_movie_index = np.random.choice(self.df.index)
            wrong_movie_name = self.df.loc[wrong_movie_index, 'name']
            if wrong_movie_name not in self.options:
                self.options.append(wrong_movie_name)

        np.random.shuffle(self.options)


    def ask_question(self):
        """
        The function displays the quiz question and its options in a Tkinter window 
        and manages user interaction, scoring, and shows the result.

        """
        def check_answer(user_answer):
            """
            The function checks if user's choice is correct and displays current score. 
            The correct answer rises the score by 30 points.
            If the chosen answer is incorrect it shows the correct answer.

            """
            if user_answer == self.correct_answer:
                self.score += 30
                result_message = f"Correct! Your score is now: {self.score}"
            else:
                result_message = f"Incorrect!. The correct answer was: '{self.correct_answer}'."
            result_message += f"\nYour score is: {self.score}"            
            messagebox.showinfo("Result", result_message)
            self.root.destroy()
        
        label = tk.Label(self.root, text=self.question, font=("Times", 16))
        label.pack(pady=20)
    
        for option in self.options:
            button = tk.Button(self.root, text=option, font=("Times", 14), command=lambda opt=option: check_answer(opt))
            button.pack(pady=5)
        
        # script to set size of Tkinter window and to centralize it on the screen
        window_width = 800
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        self.root.mainloop()

# usage of the class
higher_rating = HigherRating('movies.csv')
higher_rating.generate_question()
higher_rating.ask_question()


class OldestMovie:
    """
    The class processes movie year data from csv file and creates an automatically generated interactive quiz question
    where a user needs to guess the oldest movie among a set of randomly selected movies from a dataset.

    Libraries:
    pandas: used for data manipulation
    numpy: used for random selection and shuffling of data   
    Tkinter: used for graphical user interface interactions

    """
    def __init__(self, csv_file):
        """
        The function initializes the class by loading necessary movie data from csv file.
        It sets up the main Tkinter window and titles it.
        The inital score depends on output score of the class HigherRating.

        Parameters:
        "csv_file" (str): path to the CSV file containing movie data.

        """
        self.df = pd.read_csv(csv_file)
        self.question = "Choose the oldest movie among the given options."
        self.correct_answer = ""
        self.options = []
        self.score = higher_rating.score
        self.root = tk.Tk()
        self.root.title("Oldest Movie Quiz")

    def generate_question(self):
        """
        The function randomly selects four movies from the dataset and sorts them by their release year to determine the oldest movie,
        then creates a quiz question with these movies as options.
        """   
        selected_indices = np.random.choice(self.df.index, size=4, replace=False)
        selected_movies = self.df.loc[selected_indices]       
        sorted_movies = selected_movies.sort_values(by='year')
        self.correct_answer = sorted_movies.iloc[0]['name']
        self.options = sorted_movies['name'].tolist()

    def ask_question(self):
        """
        The function displays the quiz question and its options in a Tkinter window 
        and manages user interaction, scoring, and shows the result.

        """
        def check_answer(user_answer):
            """
            The function checks if user's choice is correct and displays current score. 
            The correct answer rises the score by 30 points.
            If the chosen answer is incorrect it shows the correct answer.

            """
            if user_answer == self.correct_answer:
                self.score += 30
                result_message = f"Correct! Your score is now: {self.score}"
            else:
                result_message = f"Incorrect! The correct answer was: '{self.correct_answer}'."
                result_message += f"\nYour score is: {self.score}"
            messagebox.showinfo("Result", result_message)
            self.root.destroy()

        label = tk.Label(self.root, text=self.question, font=("Times", 16))
        label.pack(pady=20)

        for option in self.options:
            button = tk.Button(self.root, text=option, font=("Times", 14), command=lambda opt=option: check_answer(opt))
            button.pack(pady=5)

        # script to set size of Tkinter window and to centralize it on the screen
        window_width = 800
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        self.root.mainloop()

# usage of the class
oldest_movie = OldestMovie('movies.csv')
oldest_movie.generate_question()
oldest_movie.ask_question()


class HardBudget:
    """
    The class processes movie budget data from csv file and creates an automatically generated interactive quiz question
    where a user needs to guess the exact budget spent on a randomly selected movie from a dataset.

    Libraries:
    pandas: used for data manipulation
    numpy: used for random selection and shuffling of data   
    Tkinter: used for graphical user interface interactions

    """
    def __init__(self, csv_file):
        """
        The function initializes the class by loading necessary movie data from csv file.
        It sets up the main Tkinter window and titles it.
        The inital score depends on output score of the class HigherRating.

        Parameters:
        "csv_file" (str): path to the CSV file containing movie data.

        """
        self.df = pd.read_csv(csv_file)
        self.question = ""
        self.correct_answer = ""
        self.options = []
        self.score = oldest_movie.score
        self.root = tk.Tk()
        self.root.title("Movie Budget Quiz")

    def generate_question(self):
        """
        The function randomly selects a movie from the dataset and prepares a quiz question about its budget. 
        It generates budget options, including the correct answer and additional options within a 50% to 150% range of the correct budget.
        It checks if the movie budget is not a NaN (Not a Number) to choose valid data.
    
        """
        while True:
            movie_index = np.random.choice(self.df.index)
            movie = self.df.loc[movie_index]
            movie_name = movie['name']
            movie_budget = movie['budget']


            if pd.notna(movie_budget):
                break

        self.question = f"How much money was spent on the movie '{movie_name}'?"
        self.correct_answer = movie_budget
        self.options = [movie_budget]

        while len(self.options) < 4:
            random_budget = np.random.randint(int(movie_budget * 0.5), int(movie_budget * 1.5))
            if random_budget not in self.options:
                self.options.append(random_budget)

        np.random.shuffle(self.options)

    def ask_question(self):
        """
        The function displays the quiz question and its options in a Tkinter window 
        and manages user interaction, scoring, and shows the result.

        """
        def check_answer(user_answer):
            """
            The function checks if user's choice is correct, displays current score and total score for hard questions section. 
            The correct answer rises the score by 30 points.
            If the chosen answer is incorrect it shows the correct answer.

            """
            if user_answer == self.correct_answer:
                self.score += 30
                result_message = f"Correct! Your score is now: {self.score}"
            else:
                result_message = f"Incorrect! The correct answer was: ${self.correct_answer}."
            result_message += f"\nTotal Score for Hard Questions: {self.score} out of 120"
            messagebox.showinfo("Result", result_message)
            self.root.destroy()

        label = tk.Label(self.root, text=self.question, font=("Times", 16))
        label.pack(pady=20)

        for option in self.options:
            button = tk.Button(self.root, text=f"${option}", font=("Times", 14), command=lambda opt=option: check_answer(opt))
            button.pack(pady=5)

        # script to set size of Tkinter window and to centralize it on the screen
        window_width = 800
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        self.root.mainloop()

# usage of the class
movie_budget = HardBudget('movies.csv')
movie_budget.generate_question()
movie_budget.ask_question()

hard_total_score=movie_budget.score