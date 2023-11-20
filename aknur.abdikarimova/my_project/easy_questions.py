import matplotlib.pyplot as plt
import pandas as pd
import random
import numpy as np
import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkFont  

class MovieRating:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = pd.read_csv(self.file_path)
        self.score = 0

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
        self.set_window_size(root, 800, 600)  
        font = tkFont.Font(family="Helvetica", size=14)  

        question_label = tk.Label(root, text="What movie has the highest rating?", font=font)
        question_label.pack()

        def check_answer(selected_answer):
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
            answer_button.pack()

        root.mainloop()
        return highest_rated_movie

    def set_window_size(self, root, width, height):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

rating = MovieRating('movies.csv')
sample_movies = rating.display_chart()
correct_answer = rating.generate_quiz(sample_movies)

class MovieGenre:
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)
        self.movies = self.df[['name', 'genre']].dropna()
        self.score = rating.score  

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

        return movie_name, correct_genre, options

    def create_quiz_window(self, movie_name, correct_genre, options):
        root = tk.Tk()
        root.title("Movie Genre Quiz")
        self.set_window_size(root, 800, 600)
        font = tkFont.Font(family="Helvetica", size=14)

        question_label = tk.Label(root, text=f"Choose the genre of the movie '{movie_name}':", font=font)
        question_label.pack()

        def check_answer(selected_genre):
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
            genre_button.pack()

        root.mainloop()

    def set_window_size(self, root, width, height):
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

    def play_quiz(self):
        movie_name, correct_genre, options = self.generate_question()
        self.create_quiz_window(movie_name, correct_genre, options)

genre = MovieGenre('movies.csv')
genre.play_quiz()


class MovieYear:
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)
        self.movies = self.df[['name', 'year']].dropna()
        self.score = genre.score
        self.root = tk.Tk()
        self.root.title("Movie Year Quiz")
        self.set_window_size(800, 600)  
        self.font = tkFont.Font(family="Helvetica", size=14) 

    def set_window_size(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = (screen_width / 2) - (width / 2)
        y = (screen_height / 2) - (height / 2)
        self.root.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

    def get_random_movie(self):
        return self.movies.sample()

    def generate_question(self):
        movie = self.get_random_movie()
        correct_year = movie['year'].values[0]
        movie_name = movie['name'].values[0]

        all_years = set(range(correct_year - 10, correct_year + 10))
        all_years.discard(correct_year)

        wrong_years = random.sample(list(all_years), 3)
        options = [correct_year] + wrong_years
        random.shuffle(options)

        return movie_name, correct_year, options

    def check_answer(self, user_choice, correct_answer):
        if user_choice == correct_answer:
            self.score += 10
            result_message="Correct!"
        else:
            result_message=f"Incorrect. The correct year is: {correct_answer}"
        result_message += f"\nCurrent score: {self.score}"
        messagebox.showinfo("Result", result_message)
        self.root.destroy()
        

    def play_quiz(self):
        movie_name, correct_answer, options = self.generate_question()

        label = tk.Label(self.root, text=f"Choose the release year of the movie '{movie_name}':", font=self.font)
        label.pack()

        for option in options:
            btn = tk.Button(self.root, text=option, command=lambda opt=option: self.check_answer(opt, correct_answer), font=self.font)
            btn.pack()

        self.root.mainloop()

    def get_score(self):
        return self.score

year = MovieYear('movies.csv')
year.play_quiz()


class MovieBudget:
    def __init__(self, csv_file):
        self.df = pd.read_csv(csv_file)
        self.selected_movies = self.df[['name', 'budget']].dropna().sample(10)
        self.score = 0
        self.root = tk.Tk()    
        self.font = tkFont.Font(family="Helvetica", size=16) 


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
        all_names = self.df['name'].to_numpy()  
        remaining_names = np.setdiff1d(all_names, [correct_answer])  
        wrong_answers = np.random.choice(remaining_names, 3, replace=False).tolist() 
        options = [correct_answer] + wrong_answers
        np.random.shuffle(options)  

        def check_answer(selected_option):
            if selected_option == correct_answer:
                self.score += 10
                result_message="Correct!"
            else:
                result_message=f"Incorrect. The correct answer is: {correct_answer}"
            result_message += f"\nCurrent score: {self.score}"
            messagebox.showinfo("Result", result_message)
            self.root.destroy()
      
        
        quiz_window = self.root
        quiz_window.title("Movie Budget Quiz")

        quiz_window.update()

        window_width = 800
        window_height = 600
        screen_width = quiz_window.winfo_screenwidth()
        screen_height = quiz_window.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        quiz_window.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        question_label = tk.Label(quiz_window, text=f"Which movie has the lowest budget?", font=self.font)
        question_label.pack()

        for option in options:
            btn = tk.Button(quiz_window, text=option, command=lambda opt=option: check_answer(opt), font=self.font)
            btn.pack(pady=5) 

        quiz_window.mainloop()

budget = MovieBudget('movies.csv')
budget.plot_budget_graph()  
budget.generate_quiz()   


