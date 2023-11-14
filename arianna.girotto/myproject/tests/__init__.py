import pandas as pd
import numpy as np
title_basics = pd.read_csv("//Users/ariannagirotto/Desktop/dataset/title.basics.tsv", sep="\t", quoting=3,
                           encoding='utf-8', engine='python', nrows=100000)
info_person = pd.read_csv("//Users/ariannagirotto/Desktop/dataset/name.tsv", sep="\t", quoting=3, encoding='utf-8',
                          engine='python', nrows=100000)

def title_basics_type1(df):
    random_tconst = np.random.choice(df['tconst'], replace=False)
    movie_title = df.loc[df['tconst'] == random_tconst, 'primaryTitle'].values[0]
    question = f"In quale anno è uscito {movie_title}?"

    right_answer = df.loc[df['tconst'] == random_tconst, 'startYear'].values[0]
    wrong_answers = []
    while len(wrong_answers) < 3:
        wrong_answer = np.random.choice(df['startYear'])
        if wrong_answer != right_answer and wrong_answer not in wrong_answers:
            wrong_answers.append(wrong_answer)

    answers = {
        'correct': right_answer,
        'incorrect': wrong_answers
    }

    return question, answers

title_basics_type1(title_basics)