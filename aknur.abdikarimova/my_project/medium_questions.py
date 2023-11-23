import pandas as pd
import tkinter as tk
from tkinter import messagebox
import numpy as np

# script to load dataset as pandas dataframe
path_movies = 'movies.csv'
movies = pd.read_csv(path_movies)

class MovieDirector:
    """
    The class processes movie director data from csv file and creates an automatically generated quiz question
    where a user needs to guess a correct director of a randomly selected movie out of 4 options by clicking on button.
    
    Libraries:
    pandas: used for data manipulation
    numpy: used for random selection and shuffling of data   
    Tkinter: used for graphical user interface interactions

    """
    def __init__(self, movies):
        """
        The function initializes the class with dataframe containing movie data.
        The initial score is set as 0.
        Creates the Tkinter window for a quiz question and sets its title.

        Parameters:
        "movies" (pandas.dataframe): dataframe containing movie data.

        """
        self.movies = movies
        self.score = 0
        self.root = tk.Tk()
        self.root.title("Movie Director Quiz")

    def director(self):
        """
        The function selects a random movie from the dataset and 
        creates a quiz question with one correct and three "incorrect" randomly taken director options.

        """        
        chosen_movie = self.movies.sample(1).iloc[0]      
        correct_dir = chosen_movie['director']    
        directors = self.movies['director'].unique()
        wrongs = np.random.choice(directors[directors != correct_dir], 3, replace=False).tolist()        
        options = [correct_dir] + wrongs
        np.random.shuffle(options)
        
        question = f"Who is the director of {chosen_movie['name']}?"
        return question, options, correct_dir

    def ask_question(self):
        """
        The function displays the quiz question and its options in a Tkinter window 
        and manages user interaction, scoring, and shows the result.

        """
        question, options, correct_dir = self.director()

        def check_answer(user_answer):
            """
            The function checks if user's choice is correct and displays current score. The correct answer rises the score by 20 points.
            If the chosen answer is incorrect it shows the correct answer.

            """
            if user_answer == correct_dir:
                self.score += 20
                result_message="Correct!"
            else:
                result_message= f"Incorrect! The correct answer is: {correct_dir}"
            result_message += f"\nCurrent Score: " + str(self.score)
            messagebox.showinfo("Result", result_message)
            self.root.destroy()            
        
        label = tk.Label(self.root, text=question, font=("Times", 16))
        label.pack(pady=20)
       
        for option in options:
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
director = MovieDirector(movies)
director.ask_question()

class MovieStar:
    """
    The class processes movie actor (star) data from csv file and creates an automatically generated interactive quiz question
    where a user needs to guess an actor of a randomly selected movie out of 4 options by clicking on button.
    
    Libraries:
    pandas: used for data manipulation
    numpy: used for random selection and shuffling of data   
    Tkinter: used for graphical user interface interactions

    """
    def __init__(self, movies):
        """
        The function initializes the class with dataframe containing movie data.
        The initial score is the output score from class MovieDirector.
        Creates the Tkinter window for a quiz question and sets its title.

        Parameters:
        "movies" (pandas.dataframe): dataframe containing movie data.

        """
        self.movies = movies
        self.score = director.score
        self.root = tk.Tk()
        self.root.title("Movie Star Quiz")

    def star(self):
        """
        The function selects a random movie from the dataset and 
        creates a quiz question with one correct and three "incorrect" randomly taken star options.

        """ 
        selected_movie = self.movies.sample(1).iloc[0]
        movie_name = selected_movie['name']
        correct_star = selected_movie['star']
        stars = self.movies['star'].unique()
        incorrect_stars = np.random.choice(stars[stars != correct_star], 3, replace=False).tolist()
        options = [correct_star] + incorrect_stars
        np.random.shuffle(options)

        return movie_name, options, correct_star

    def ask_question(self):
        """
        The function displays the quiz question and its options in a Tkinter window 
        and manages user interaction, scoring, and shows the result.

        """
        movie_name, options, correct_star = self.star()

        def check_answer(user_answer):
            """
            The function checks if user's choice is correct and displays current score. The correct answer rises the score by 20 points.
            If the chosen answer is incorrect it shows the correct answer.

            """
            if user_answer == correct_star:
                self.score += 20
                result_message="Correct!"
            else:
                result_message= f"Incorrect! The correct answer is: {correct_star}"
            result_message += f"\nCurrent Score: " + str(self.score)
            messagebox.showinfo("Result", result_message)
            self.root.destroy()
        
        label = tk.Label(self.root, text=f"Who starred in the movie '{movie_name}'?", font=("Times", 16))
        label.pack(pady=20)
    
        for option in options:
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
star = MovieStar(movies)
star.ask_question()


class MovieCompany:
    """
    The class processes movie company data from csv file and creates an automatically generated interactive quiz question
    where a user needs to guess a company that released a randomly selected movie out of 4 options by clicking on button.
    
    Libraries:
    pandas: used for data manipulation
    numpy: used for random selection and shuffling of data   
    Tkinter: used for graphical user interface interactions

    """
    def __init__(self, movies):
        """
        The function initializes the class with dataframe containing movie data.
        The initial score is the output score from class MovieStar.
        Creates the Tkinter window for a quiz question and sets its title.

        Parameters:
        "movies" (pandas.dataframe): dataframe containing movie data.

        """
        self.movies = movies
        self.score = star.score
        self.root = tk.Tk()
        self.root.title("Movie Company Quiz")

    def company(self):
        """
        The function selects a random movie from the dataset and 
        creates a quiz question with one correct and three "incorrect" randomly taken company options.

        """ 
        selected_movie = self.movies.sample(1).iloc[0]
        movie_name = selected_movie['name']
        correct_company = selected_movie['company']        
        companies = self.movies['company'].unique()
        incorrect_companies = np.random.choice(companies[companies != correct_company], 3, replace=False).tolist()
        options = [correct_company] + incorrect_companies
        np.random.shuffle(options)

        return movie_name, options, correct_company


    def ask_question(self):
        """
        The function displays the quiz question and its options in a Tkinter window 
        and manages user interaction, scoring, and shows the result.

        """
        movie_name, options, correct_company = self.company()

        def check_answer(user_answer):
            """
            The function checks if user's choice is correct and displays current score. The correct answer rises the score by 20 points.
            If the chosen answer is incorrect it shows the correct answer.

            """
            if user_answer == correct_company:
                self.score += 20
                result_message="Correct!"
            else:
                result_message= f"Incorrect! The correct answer is: {correct_company}"
            result_message += f"\nCurrent Score: " + str(self.score)
            messagebox.showinfo("Result", result_message)
            self.root.destroy()          

        label = tk.Label(self.root, text=f"What company released the movie '{movie_name}'?", font=("Times", 16))
        label.pack(pady=20)

        for option in options:
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
company = MovieCompany(movies)
company.ask_question()


class MovieCountry:
    """
    The class processes movie country data from csv file and creates an automatically generated interactive quiz question
    where a user needs to guess a country that released a randomly selected movie out of 4 options by clicking on button.
    
    Libraries:
    pandas: used for data manipulation
    numpy: used for random selection and shuffling of data   
    Tkinter: used for graphical user interface interactions

    """
    def __init__(self, movies):
        """
        The function initializes the class with dataframe containing movie data.
        The initial score is the output score from class MovieCompany.
        Creates the Tkinter window for a quiz question and sets its title.

        Parameters:
        "movies" (pandas.dataframe): dataframe containing movie data.

        """
        self.movies = movies
        self.score = company.score
        self.root = tk.Tk()
        self.root.title("Movie Country Quiz")

    def country(self):
        """
        The function selects a random movie from the dataset and 
        creates a quiz question with one correct and three "incorrect" randomly taken country options.

        """ 
        selected_movie = self.movies.sample(1).iloc[0]
        movie_name = selected_movie['name']
        correct_country = selected_movie['country']
        countries = self.movies['country'].unique()
        incorrect_countries = np.random.choice(countries[countries != correct_country], 3, replace=False).tolist()
        options = [correct_country] + incorrect_countries
        np.random.shuffle(options)

        return movie_name, options, correct_country

    def ask_question(self):
        """
        The function displays the quiz question and its options in a Tkinter window 
        and manages user interaction, scoring, and shows the result.

        """
        movie_name, options, correct_country = self.country()

        def check_answer(user_answer):
            """
            The function checks if user's choice is correct, displays current score and total score for medium level questions. 
            The correct answer rises the score by 20 points.
            If the chosen answer is incorrect it shows the correct answer.

            """
            if user_answer == correct_country:
                self.score += 20
                result_message="Correct!"
            else:
                result_message= f"Incorrect! The correct answer is: {correct_country}"
            result_message += f"\nTotal Score for Medium Questions: " + str(self.score) + " out of 80"
            messagebox.showinfo("Result", result_message)      
            self.root.destroy()
        
        label = tk.Label(self.root, text=f"Choose the country that released the movie '{movie_name}':", font=("Times", 16))
        label.pack(pady=20)

        for option in options:
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
country = MovieCountry(movies)
country.ask_question()
medium_total_score=country.score




