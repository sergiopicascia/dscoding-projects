import pandas as pd
import random
import tkinter as tk
from tkinter import messagebox

# Load the dataset
path_movies = 'movies.csv'
movies = pd.read_csv(path_movies)

class MovieDirector:
    def __init__(self, movies):
        self.movies = movies
        self.score = 0
        self.root = tk.Tk()
        self.root.title("Movie Director Quiz")

    def q_director(self):        
        
        chosen_movie = self.movies.sample(1).iloc[0]      
        correct_dir = chosen_movie['director']        
        wrongs = self.movies[self.movies['director'] != correct_dir]['director'].sample(3).tolist()       
        options = [correct_dir] + wrongs
        random.shuffle(options)
        question = f"Who is the director of {chosen_movie['name']}?"
        return question, options, correct_dir

    def ask_question(self):
        question, options, correct_dir = self.q_director()

        def check_answer(user_answer):
            if user_answer == correct_dir:
                self.score += 20
                result_message="Correct!"
            else:
                result_message= f"Incorrect! The correct answer is: {correct_dir}"
            result_message += f"\nCurrent Score: " + str(self.score)
            messagebox.showinfo("Result", result_message)
            self.root.quit()
        
        label = tk.Label(self.root, text=question, font=("Times", 16))
        label.pack(pady=20)
       
        for option in options:
            button = tk.Button(self.root, text=option, font=("Times", 14), command=lambda opt=option: check_answer(opt))
            button.pack(pady=5)
        
        window_width = 500
        window_height = 300
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        self.root.mainloop()

director = MovieDirector(movies)
director.ask_question()

class MovieStar:
    def __init__(self, movies):
        self.movies = movies
        self.score = director.score
        self.root = tk.Tk()
        self.root.title("Movie Star Quiz")

    def star(self):
        
        selected_movie = self.movies.sample(1).iloc[0]
        movie_name = selected_movie['name']
        correct_star = selected_movie['star']      
        incorrect_stars = self.movies[self.movies['star'] != correct_star]['star'].drop_duplicates().sample(3).tolist()
        options = [correct_star] + incorrect_stars
        random.shuffle(options)  

        return movie_name, options, correct_star

    def ask_question(self):
        movie_name, options, correct_star = self.star()

        def check_answer(user_answer):
            if user_answer == correct_star:
                self.score += 20
                result_message="Correct!"
            else:
                result_message= f"Incorrect! The correct answer is: {correct_star}"
            result_message += f"\nCurrent Score: " + str(self.score)
            messagebox.showinfo("Result", result_message)
            self.root.quit()
        
        label = tk.Label(self.root, text=f"Who starred in the movie '{movie_name}'?", font=("Times", 16))
        label.pack(pady=20)
    
        for option in options:
            button = tk.Button(self.root, text=option, font=("Times", 14), command=lambda opt=option: check_answer(opt))
            button.pack(pady=5)
        
        window_width = 500
        window_height = 300
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        self.root.mainloop()

star = MovieStar(movies)
star.ask_question()

class MovieCompany:
    def __init__(self, movies):
        self.movies = movies
        self.score = star.score
        self.root = tk.Tk()
        self.root.title("Movie Company Quiz")

    def company(self):
        selected_movie = self.movies.sample(1).iloc[0]
        movie_name = selected_movie['name']
        correct_company = selected_movie['company']        
        incorrect_companies = self.movies[self.movies['company'] != correct_company]['company'].drop_duplicates().sample(3).tolist()      
        options = [correct_company] + incorrect_companies
        random.shuffle(options)  

        return movie_name, options, correct_company

    def ask_question(self):
        movie_name, options, correct_company = self.company()

        def check_answer(user_answer):
            if user_answer == correct_company:
                self.score += 20
                result_message="Correct!"
            else:
                result_message= f"Incorrect! The correct answer is: {correct_company}"
            result_message += f"\nCurrent Score: " + str(self.score)
            messagebox.showinfo("Result", result_message)
            self.root.quit()          

        label = tk.Label(self.root, text=f"What company released the movie '{movie_name}'?", font=("Times", 16))
        label.pack(pady=20)

        for option in options:
            button = tk.Button(self.root, text=option, font=("Times", 14), command=lambda opt=option: check_answer(opt))
            button.pack(pady=5)

        window_width = 500
        window_height = 300
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        self.root.mainloop()

company = MovieCompany(movies)
company.ask_question()


class MovieCountry:
    def __init__(self, movies):
        self.movies = movies
        self.score = company.score
        self.root = tk.Tk()
        self.root.title("Movie Country Quiz")

    def country(self):
        selected_movie = self.movies.sample(1).iloc[0]
        movie_name = selected_movie['name']
        correct_country = selected_movie['country']
        incorrect_countries = self.movies[self.movies['country'] != correct_country]['country'].drop_duplicates().sample(3).tolist()
        options = [correct_country] + incorrect_countries
        random.shuffle(options)  

        return movie_name, options, correct_country

    def ask_question(self):
        movie_name, options, correct_country = self.country()

        def check_answer(user_answer):
            if user_answer == correct_country:
                self.score += 20
                result_message="Correct!"
            else:
                result_message= f"Incorrect! The correct answer is: {correct_country}"
            result_message += f"\nCurrent Score: " + str(self.score)
            messagebox.showinfo("Result", result_message)      
            self.root.quit()
        
        label = tk.Label(self.root, text=f"Choose the country that released the movie '{movie_name}':", font=("Times", 16))
        label.pack(pady=20)

        for option in options:
            button = tk.Button(self.root, text=option, font=("Times", 14), command=lambda opt=option: check_answer(opt))
            button.pack(pady=5)
        
        window_width = 500
        window_height = 300
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        self.root.mainloop()

country = MovieCountry(movies)
country.ask_question()





