import pandas as pd
from numpy import random
import string
import matplotlib.pyplot as plt

# Movie Management
class movie:
   def __init__(self, title, director, actor, country, year, genres):
       self.title = title
       self.director = director
       self.actor = actor
       self.country = country
       self.year = year
       self.genres = self.format_genres(genres)

   def format_genres(self, genres):
       genres = genres.split('|')
       if len(genres) > 1:
           genres = ', '.join(genres[:-1]) + ' and ' + genres[-1]
       else:
           genres = genres[0]
       return genres

   def generate_question(self):
       question = f"What is the title of the film released in {self.year} directed by {self.director}, starring {self.actor}, produced in {self.country} and belonging to the genre {self.genres}?"
       return question, self.title

   def generate_answers(self, incorrect_movies):
       incorrect_answers = incorrect_movies.sample(3)['movie_title'].values
       correct_answer = self.title
       answers = [correct_answer] + list(incorrect_answers)
       random.shuffle(answers)
       return answers

   # Quiz Management
   class quiz:
       def __init__(self, movies, difficulty):
           self.movies = movies
           self.difficulty = difficulty
           self.score = 0
           self.score_history = [0]

       def choose_difficulty(self):
           if self.difficulty == 'easy':
               return self.movies['year'] > 1990
           elif self.difficulty == 'difficult':
               return self.movies['year'] < 1990
           else:
               print("Invalid choice, defaulting to Easy")
               return self.movies['year'] > 1990

       def generate_question(self):
           correct_movie = self.movies[self.choose_difficulty()].sample(1)
           question, correct_movie = correct_movie.generate_question()
           return question, correct_movie

       def generate_answers(self, correct_movie):
           incorrect_movies = self.movies.drop(correct_movie.index.values.tolist())
           return correct_movie.generate_answers(incorrect_movies)

       def play(self):
           for i in range(1, 11):
               question, correct_movie = self.generate_question()
               answers = self.generate_answers(correct_movie)
               print(f"Question {i}. {question}")
               for j, answer in zip(string.ascii_uppercase, answers):
                   print(f"{j}. {answer}")
               user_answer = input("Your answer: ").upper()
               while user_answer not in string.ascii_uppercase:
                   print("You have another chance, try again!")
                   user_answer = input("Your answer: ").upper()
               correct_answer = correct_movie.title
               selected_answer = answers[string.ascii_uppercase.index(user_answer)]
               if selected_answer == correct_answer:
                   print("Correct!\n")
                   self.score += 1
                   self.score_history.append(self.score)
               else:
                   print(f"Wrong! The correct answer is {correct_answer}\n")
                   self.score_history.append(self.score)
           print(f"Your total score is {self.score}/10!\n")
           plt.plot(self.score_history)
           plt.xlabel('Question number')
           plt.ylabel('Score')
           plt.title('Score over time')
           plt.ylim(0, 10)
           plt.show()
           retry = input("Do you want to retry? (yes/no): ").lower()
           if retry != 'no':
               self.play()
           else:
               print("\nThanks for trying!")


