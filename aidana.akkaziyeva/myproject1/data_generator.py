import pandas as pd
import random

netflix_data = pd.read_csv('netflix_data.csv')




#dividing into two groups (tv shows, movies)
TV_Shows = []
Movies = []
for i in range(len(netflix_data)):
    type = netflix_data.loc[i, 'type'] 
    if type == 'TV Show':
        TV_Shows.append(netflix_data.loc[i, 'title'])
    elif type == 'Movie':
        Movies.append(netflix_data.loc[i, 'title'])
    else:
        pass 


"""""
def generate_movie_length_question(Movies):
    show = random.sample(Movies, 4)
    
    length = netflix_data.loc(netflix_data['title']==show, 'duration').values[0]
    
    question = f"Which movie is the longest?"
    correct_answer =
    return question, correct_answer, incorrect_answers

"""


def generate_dir_question(netflix_data):
    show = random.choice(netflix_data['title'])
    director = netflix_data.loc[netflix_data['title']==show, 'director'].values[0]
    cast = netflix_data.loc[netflix_data['title']==show, 'cast'].values[0]
    
    directors_filtered = netflix_data.dropna(subset=['director'])  #Filter out rows where director is Null

    question = f"Who directed '{show}'?"             #{}placeholders for variables in a string
    correct_answer = director
    incorrect_answers = random.sample(list(directors_filtered['director'].unique()),3)  #because has duplicate director columns
   
    return question, correct_answer, incorrect_answers


        
def generate_genre_question(netflix_data):
    question = f"Which of the following belongs to the horror genre?"
    correct_answers_all = []
    incorrect_answers_all = []

    for i in range(len(netflix_data)):
        genre = netflix_data.loc[i, 'listed_in']
        if 'Horror' in genre:
            correct_answers_all.append(netflix_data.loc[i, 'title'])
        else: incorrect_answers_all.append(netflix_data.loc[i, 'title'])
        
    incorrect_answers = random.sample(incorrect_answers_all,3) 
    correct_answer = random.sample(correct_answers_all,1) 
    
    return question, correct_answer, incorrect_answers


def present_dir_question (question, correct_answer, incorrect_answers):
    print(question)
    all_answers = [correct_answer] + incorrect_answers 
    #[]-creating a list from a single string, incorrect answers is already a list of strings

    random.shuffle(all_answers)

    for i, answer in enumerate(all_answers, 1):
        print(f"{i}. {answer}")      #{}placeholders for variables in a string


def present_genre_question (question, correct_answer, incorrect_answers):
    print(question)
    all_answers = correct_answer + incorrect_answers 
    #[]-creating a list from a single string, incorrect answers is already a list of strings

    random.shuffle(all_answers)

    for i, answer in enumerate(all_answers, 1):
        print(f"{i}. {answer}")      #{}placeholders for variables in a string


#







def evaluate_answer (user_answer, correct_answer):
    user_answer==correct_answer


