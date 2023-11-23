import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkFont

class MovieRating:
    """ 
    The class processes and visualizes movie rating data from a csv file, 
    and based on the displayed bar chart creates an interactive quiz question with clickable options
    where a user needs to choose a movie with the highest rating score among displayed movies.

    Libraries:
    pandas: used for data manipulation
    numpy: used for random selection and shuffling of data
    matplotlib: used for visualization of a bar chart
    Tkinter: used for graphical user interface interactions

    """

    def __init__(self, file_path):
        """
        The function initializes the class with the path to the csv file and loads the data into a pandas DataFrame.
        The initial user's score is set to be 0.
        
        Parameters:
        'file_path'(str): path to the csv file contatining movies data.

        """
        self.file_path = file_path
        self.df = pd.read_csv(self.file_path)
        self.score = 0

    def display_chart(self):
        """
        The function randomly selects 10 movies from a pandas dataframe and returns a bar chart showing their name and rating scores.

        """
        sample_movies = self.df.sample(10)
        plt.figure(figsize=(10, 6))
        plt.bar(sample_movies['name'], sample_movies['score'], color='skyblue')
        plt.xlabel('Movie Name')
        plt.ylabel('Rating Score')
        plt.xticks(rotation=45, ha='right')
        plt.title('What movie has the highest rating? \n*Close the window to answer the question')
        plt.tight_layout()
        plt.show()
        return sample_movies

    def generate_quiz(self, sample_movies):
        """
        The function uses Tkinter library to generate a quiz window 
        which asks a user to choose a movie with the highest rating among 4 options from above 10 randomly selested set.

        Parameters:
        "sample_movies" (pandas.dataframe): a sample of 10 randomly taken movies which is output of the function "display_chart".

        """
        highest_rated_movie = sample_movies.loc[sample_movies['score'].idxmax()]['name']
        wrong_answers = sample_movies[sample_movies['name'] != highest_rated_movie].sample(3)['name'].tolist()
        answers = wrong_answers + [highest_rated_movie]
        np.random.shuffle(answers)

        root = tk.Tk()
        root.title("Movie Quiz")
        self.set_window_size(root, 800, 600)  
        font = tkFont.Font(family="Times", size=14)  

        question_label = tk.Label(root, text="What movie has the highest rating?", font=font)
        question_label.pack(pady=20)

        def check_answer(selected_answer):
            """
            The function checks if user's choice is correct and displays current score. The correct answer rises the score by 10 points.
            If the chosen answer is incorrect it shows the correct answer.

            """
            if selected_answer == highest_rated_movie:
                self.score += 10
                result_message = "Correct! The highest rated movie is " + highest_rated_movie
            else:
                result_message = "Incorrect! The highest rated movie is " + highest_rated_movie
            result_message += f"\nCurrent score: {self.score}"
            messagebox.showinfo("Result", result_message)
            root.destroy()

        for answer in answers:
            answer_button = tk.Button(root, text=answer, command=lambda ans=answer: check_answer(ans), font=font)
            answer_button.pack(pady=5)

        root.mainloop()
        return highest_rated_movie

    def set_window_size(self, root, width, height):
        """
        The function sets size and centralizes Tkinter window on the screen.

        Parameters:
        "root" (tk.Tk): Tkinter window.
        "width" (int): width of the window.
        "height" (int): height of the window.

        """
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

# usage of the class
rating = MovieRating('movies.csv')
sample_movies = rating.display_chart()
correct_answer = rating.generate_quiz(sample_movies)

class MovieGenre:
    """
    The class processes movie genre data from csv file and creates an automatically generated quiz question
    where a user needs to guess a correct genre of a randomly selected movie.
    
    Libraries:
    pandas: used for data manipulation
    numpy: used for random selection and shuffling of data   
    Tkinter: used for graphical user interface interactions

    """
    def __init__(self, csv_file):
        """
        The function initializes the class by loading necessary data from csv file.
        The score depends on the output score of MovieRating class.

        Parameters:
        "csv_file" (str): path to the CSV file containing movie data.

        """
        self.df = pd.read_csv(csv_file)
        self.movies = self.df[['name', 'genre']].dropna()
        self.score = rating.score  
        
    
    def generate_question(self):
        """
        The function selects a random movie and creates a quiz question with 4 genre options.
        Returns name of randomly selected movie, its respective genre and other three wrong genre options.

        """
        movie = self.movies.sample()
        correct_genre = movie['genre'].values[0]
        movie_name = movie['name'].values[0]

        all_genres = np.array(self.movies['genre'].unique())
        wrong_genres = np.random.choice(all_genres[all_genres != correct_genre], 3, replace=False)
        options = np.random.permutation(np.append(wrong_genres, correct_genre))

        return movie_name, correct_genre, options.tolist()

    def create_quiz_window(self, movie_name, correct_genre, options):
        """
        The function generates a Tkinter window which shows a quiz question and genre options as a clickable buttons.

        Parameters:
        (the output of function "generate_question")
        "movie_name" (str): the name of the movie for the quiz question.
        "correct_genre" (str): the correct genre for the movie.
        "options" (list): list of genre options to display.

        """
        root = tk.Tk()
        root.title("Movie Genre Quiz")
        self.set_window_size(root, 1000, 600)
        font = tkFont.Font(family="Times", size=14)

        question_label = tk.Label(root, text=f"Choose the genre of the movie '{movie_name}':", font=font)
        question_label.pack(pady=20)

        def check_answer(selected_genre):
            """
            The function checks if user's choice is correct and displays current score. The correct answer rises the score by 10 points.
            If the chosen answer is incorrect it shows the correct answer.

            """
            if selected_genre == correct_genre:
                self.score += 10
                result_message= f"Correct! The genre of '{movie_name}' is {correct_genre}"
            else:
                result_message= f"Incorrect. The correct genre of '{movie_name}' is {correct_genre}"
            result_message += f"\nCurrent score: {self.score}"
            messagebox.showinfo("Result", result_message)
            root.destroy()

        for genre in options:
            genre_button = tk.Button(root, text=genre, command=lambda g=genre: check_answer(g), font=font)
            genre_button.pack(pady=5)

        root.mainloop()

    def set_window_size(self, root, width, height):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

    def play_quiz(self):
        """
        The function runs a quiz question generating methods together.        
        """
        movie_name, correct_genre, options = self.generate_question()
        self.create_quiz_window(movie_name, correct_genre, options)

# usage of the class
genre = MovieGenre('movies.csv')
genre.play_quiz()


class MovieYear:
    """
    The class processes movie year data from csv file and creates an automatically generated question with options as clickable buttons 
    where a user needs to guess a released year of randomly chosen movie.

    Libraries:
    pandas: used for data manipulation
    numpy: used for random selection and shuffling of data   
    Tkinter: used for graphical user interface interaction

    """
    def __init__(self, csv_file):
        """
        The function initializes the class by loading necessary data from csv file.
        The score depends on the output score of MovieGenre class.
        Creates Tkinter window, sets its size using function "set_window_size" and text font.

        Parameters:
        "csv_file" (str): path to the CSV file containing movie data.

        """
        self.df = pd.read_csv(csv_file)
        self.movies = self.df[['name', 'year']].dropna()
        self.score = genre.score
        self.root = tk.Tk()
        self.root.title("Movie Year Quiz")
        self.set_window_size(1000, 600)  
        self.font = tkFont.Font(family="Times", size=14) 

    def set_window_size(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()        
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

    def generate_question(self):
        """
        The function creates a quiz question by taking a random movie from dataframe, its respective released year 
        and generating other 3 wrong options in a range of 10 years before and 10 years after the released year.

        """
        movie = self.movies.sample()
        correct_year = movie['year'].values[0]
        movie_name = movie['name'].values[0]

        all_years = np.arange(correct_year - 10, correct_year + 11)
        wrong_years = np.random.choice(all_years[all_years != correct_year], 3, replace=False)
        options = np.random.permutation(np.append(wrong_years, correct_year))

        return movie_name, correct_year, options.tolist()

    def check_answer(self, user_choice, correct_answer):
        """
        The function checks if user's choice is correct and displays current score. The correct answer rises the score by 10 points.
        If the chosen answer is incorrect it shows the correct answer.

        """
        if user_choice == correct_answer:
            self.score += 10
            result_message="Correct!"
        else:
            result_message=f"Incorrect. The correct year is: {correct_answer}"
        result_message += f"\nCurrent score: {self.score}"
        messagebox.showinfo("Result", result_message)
        self.root.destroy()
        

    def play_quiz(self):
        """
        The function uses abovegiven methods to generate a quiz question, display it in a Tkinter window, 
        and evaluates the user's choice and score.
        
        """
        movie_name, correct_answer, options = self.generate_question()

        label = tk.Label(self.root, text=f"Choose the release year of the movie '{movie_name}':", font=self.font)
        label.pack(pady=20)

        for option in options:
            btn = tk.Button(self.root, text=option, command=lambda opt=option: self.check_answer(opt, correct_answer), font=self.font)
            btn.pack(pady=5)

        self.root.mainloop()

# usage of the class
year = MovieYear('movies.csv')
year.play_quiz()


class MovieBudget:
    """
    The class processes movie budget data from csv file and displays a graph,
    then based on the graph creates a quiz question with clickable button options
    where a user needs to choose a movie with the lowest budget among randomly selected set.

    Libraries:
    pandas: used for data manipulation
    numpy: used for random selection and shuffling of data
    matplotlib: used for visualization of a step graph
    Tkinter: used for graphical user interface interactions

    """
    def __init__(self, csv_file):
        """
        The function initializes the class by selecting random 10 movies with respective budget data from csv file.
        Initial score depends on the output score of the class MovieYear.

        """
        self.df = pd.read_csv(csv_file)
        self.selected_movies = self.df[['name', 'budget']].dropna().sample(10)
        self.score = year.score
        
    def plot_budget_graph(self):
        """
        The function uses randomly selected set of 10 movies 
        to display a step graph using matplotlib where the movies names and their budget are visualized.

        """
        sorted_movies = self.selected_movies.sort_values('budget')
        plt.step(sorted_movies['name'], sorted_movies['budget'], where='mid')
        plt.xticks(rotation=45, ha='right')
        plt.xlabel('Movie Name')
        plt.ylabel('Budget')
        plt.title('Which movie has the lowest budget?\n*Close the window to answer the question')
        plt.tight_layout()
        plt.show()

    def generate_quiz(self):
        """
        The function generates a quiz question in Tkinter window 
        where a user needs to choose button with movie name that has the lowest budget.
        It uses numpy to randomly select three wrong options from 10 movies set used for graph and to shuffle options.

        """
        lowest_budget_movie = self.selected_movies.sort_values('budget').iloc[0]
        correct_answer = lowest_budget_movie['name']
        all_names = self.df['name'].to_numpy()
        remaining_names = np.setdiff1d(all_names, [correct_answer])
        wrong_answers = np.random.choice(remaining_names, 3, replace=False)
        options = np.random.permutation(np.append(wrong_answers, correct_answer))  

        def check_answer(selected_option):
            """
            The function checks if user's choice is correct, displays current score and total score for easy questions section. 
            The correct answer rises the score by 10 points.
            If the chosen answer is incorrect it shows the correct answer.

            """
            if selected_option == correct_answer:
                self.score += 10
                result_message="Correct!"
            else:
                result_message=f"Incorrect. The correct answer is: {correct_answer}"
            result_message += f"\nTotal Score for Easy Questions: {self.score} out of 40"
            messagebox.showinfo("Result", result_message)
            quiz_window.destroy()
        
        quiz_window = tk.Tk()
        quiz_window.title("Movie Budget Quiz")
        font = tkFont.Font(family="Times", size=16) 
        quiz_window.update()

        # script to set size of Tkinter window and to centralize it on the screen
        window_width = 800
        window_height = 600
        screen_width = quiz_window.winfo_screenwidth()
        screen_height = quiz_window.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        quiz_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        question_label = tk.Label(quiz_window, text=f"Which movie has the lowest budget?", font=font)
        question_label.pack(pady=20)

        for option in options:
            btn = tk.Button(quiz_window, text=option, command=lambda opt=option: check_answer(opt), font=font)
            btn.pack(pady=5) 

        quiz_window.mainloop()

# usage of the class
budget = MovieBudget('movies.csv')
budget.plot_budget_graph()  
budget.generate_quiz()   
easy_total_score=budget.score


