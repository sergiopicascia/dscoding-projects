'''
IMPORTARE I PACCHETTI CHE MI SERVONO PER IL PROGETTO
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

'''
IMPORTARE I DATASET E PULIRLI, METTENDO SOLO I CAMPI CHE MI SERVONO
'''
title_basics = pd.read_csv("//Users/ariannagirotto/Desktop/dataset/title.basics.tsv", sep="\t", quoting=3,
                           encoding='utf-8', engine='python', nrows=100000)
info_person = pd.read_csv("//Users/ariannagirotto/Desktop/dataset/name.tsv", sep="\t", quoting=3, encoding='utf-8',
                          engine='python', nrows=100000)

title_basics = title_basics[(title_basics != '\\N').all(axis=1)]
info_person = info_person[(info_person != '\\N').all(axis=1)]

easy_title_basics = title_basics[
    (title_basics['startYear'].astype(int) >= 1990) &
    (title_basics['startYear'].astype(int) <= 2023)]
easy_title_basics = easy_title_basics.sort_values(by='startYear', ascending=False)

medium_title_basics = title_basics[
    (title_basics['startYear'].astype(int) >= 1940) &
    (title_basics['startYear'].astype(int) < 1990)]
easy_title_basics = easy_title_basics.sort_values(by='startYear', ascending=False)

difficult_title_basics = title_basics[
    (title_basics['startYear'].astype(int) >= 1800) &
    (title_basics['startYear'].astype(int) < 1940)]

easy_info_person = info_person[
    (info_person['birthYear'].astype(int) >= 1960) &
    (info_person['birthYear'].astype(int) <= 1987)]
easy_info_person = easy_info_person.sort_values(by='birthYear', ascending=False)

medium_info_person = info_person[
    (info_person['birthYear'].astype(int) >= 1930) &
    (info_person['birthYear'].astype(int) < 1960)]
medium_info_person = medium_info_person.sort_values(by='birthYear', ascending=False)

difficult_info_person = info_person[
    (info_person['birthYear'].astype(int) >= 1800) &
    (info_person['birthYear'].astype(int) < 1930)]
'''
FUNZIONI PER CREARE LE DOMANDE E LE RISPOSTE
'''


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


def title_basics_type2(df):
    random_tconst = np.random.choice(df['tconst'], replace=False)
    movie_title = df.loc[df['tconst'] == random_tconst, 'primaryTitle'].values[0]
    question = f"Di quale genere è il film {movie_title}?"

    right_answer = df.loc[df['tconst'] == random_tconst, 'genres'].values[0]
    wrong_answers = []
    while len(wrong_answers) < 3:
        wrong_answer = np.random.choice(df['genres'])
        if wrong_answer != right_answer and wrong_answer not in wrong_answers:
            wrong_answers.append(wrong_answer)

    answers = {
        'correct': right_answer,
        'incorrect': wrong_answers
    }

    return question, answers


def title_basics_qa(df, num_type1_qa, num_type2_qa):
    questions = []
    answers = []

    for _ in range(num_type1_qa):
        question, answer = title_basics_type1(df)
        questions.append(question)
        answers.append(answer)

    for _ in range(num_type2_qa):
        question, answer = title_basics_type2(df)
        questions.append(question)
        answers.append(answer)

    return questions, answers


def info_person_type1(df):
    random_nconst = np.random.choice(df['nconst'], replace=False)
    person_name = df.loc[df['nconst'] == random_nconst, 'primaryName'].values[0]
    question = f"In che anno è nato/a {person_name}?"

    right_answer = df.loc[df['nconst'] == random_nconst, 'birthYear'].values[0]
    wrong_answers = []
    while len(wrong_answers) < 3:
        wrong_answer = np.random.choice(df['birthYear'])
        if wrong_answer != right_answer and wrong_answer not in wrong_answers:
            wrong_answers.append(wrong_answer)

    answers = {
        'correct': right_answer,
        'incorrect': wrong_answers
    }

    return question, answers


def info_person_type2(df):
    random_nconst = np.random.choice(df['nconst'], replace=False)
    person_name = df.loc[df['nconst'] == random_nconst, 'primaryName'].values[0]
    question = f"Quali sono le principali professioni di {person_name}?"

    right_answer = df.loc[df['nconst'] == random_nconst, 'primaryProfession'].values[0]
    wrong_answers = []
    while len(wrong_answers) < 3:
        wrong_answer = np.random.choice(df['primaryProfession'])
        if wrong_answer != right_answer and wrong_answer not in wrong_answers:
            wrong_answers.append(wrong_answer)

    answers = {
        'correct': right_answer,
        'incorrect': wrong_answers
    }

    return question, answers


def info_person_qa(df, num_type1_qa, num_type2_qa):
    questions = []
    answers = []

    for _ in range(num_type1_qa):
        question, answer = info_person_type1(df)
        questions.append(question)
        answers.append(answer)

    for _ in range(num_type2_qa):
        question, answer = info_person_type2(df)
        questions.append(question)
        answers.append(answer)

    return questions, answers


'''
FUNZIONI CHE SUDDIVIDONO NEI VARI TIPI DI QUIZ
'''


def easy():
    title_basics_questions, title_basics_answers = title_basics_qa(easy_title_basics, 2, 2)
    info_person_questions, info_person_answers = info_person_qa(easy_info_person, 2, 2)

    title_basics_pairs = list(zip(title_basics_questions, title_basics_answers))
    info_person_pairs = list(zip(info_person_questions, info_person_answers))
    pairs = title_basics_pairs + info_person_pairs
    np.random.shuffle(pairs)
    questions, answers = zip(*pairs)

    score = 0

    for i, question in enumerate(questions):
        print(f"Domanda {i + 1}: {question}")
        answer_options = [answers[i]['correct']] + answers[i]['incorrect']
        np.random.shuffle(answer_options)

        for j, answer in enumerate(answer_options):
            print(f"{j + 1}. {answer}")

        while True:
            user_answer = input("Inserisci il numero della risposta corretta: ")
            try:
                user_answer = int(user_answer)
                if 1 <= user_answer <= len(answer_options) and answer_options[user_answer - 1] == answers[i]['correct']:
                    print("Risposta corretta!\n")
                    score += 1
                    break
                elif user_answer > len(answer_options):
                    print("Risposta non valida.\n")
                else:
                    print("Risposta errata!\n")
                    break
            except ValueError:
                print("Inserisci un numero valido.\n")

    print(f"Il punteggio finale è {score}/{len(questions)}")
    final_score = score / len(questions)
    percentuale_easy = final_score * 100
    if percentuale_easy >= 50:
        print(f"Congratulations! You have passed the easy quiz with {percentuale_easy}%")
        if 50 <= percentuale_easy <= 80:
            print(f"Good job! You have passed the test but there is still room for improvement. Try again!")
        elif 80 < percentuale_easy <= 100:
            print(f"Fantastic! You have a nice knowledge of film. Too easy? Try the medium quiz")
    else:
        print(f"Fail! You have done {percentuale_easy}% and you haven't passed the easy quiz. Are you living in a cave?Try "
              f"again!")
    return percentuale_easy


def medium():
    title_basics_questions, title_basics_answers = title_basics_qa(medium_title_basics, 1)
    info_person_questions, info_person_answers = info_person_qa(medium_info_person, 1)

    title_basics_pairs = list(zip(title_basics_questions, title_basics_answers))
    info_person_pairs = list(zip(info_person_questions, info_person_answers))
    pairs = title_basics_pairs + info_person_pairs
    np.random.shuffle(pairs)
    questions, answers = zip(*pairs)

    score = 0

    for i, question in enumerate(questions):
        print(f"Domanda {i + 1}: {question}")
        answer_options = [answers[i]['correct']] + answers[i]['incorrect']
        np.random.shuffle(answer_options)

        for j, answer in enumerate(answer_options):
            print(f"{j + 1}. {answer}")

        while True:
            user_answer = input("Inserisci il numero della risposta corretta: ")
            try:
                user_answer = int(user_answer)
                if 1 <= user_answer <= len(answer_options) and answer_options[user_answer - 1] == answers[i]['correct']:
                    print("Risposta corretta!\n")
                    score += 1
                    break
                elif user_answer > len(answer_options):
                    print("Risposta non valida.\n")
                else:
                    print("Risposta errata!\n")
                    break
            except ValueError:
                print("Inserisci un numero valido.\n")

    print(f"Il punteggio finale è {score}/{len(questions)}")
    final_score = score / len(questions)
    percentuale_medium = final_score * 100
    if percentuale_medium >= 60:
        print(f"Congratulations! You have passed the medium quiz with {percentuale_medium}%")
        if 60 <= percentuale_medium <= 80:
            print(f"Good job! You have passed the test but there is still room for improvement. Try again!")
        elif 80 < percentuale_medium <= 100:
            print(f"Fantastic! You have a very good knowledge of film. Too easy? Try the difficult quiz")
    else:
        print(
            f"Fail! You have done {percentuale_medium}% and you haven't passed the medium quiz ( at least it was the medium "
            f"and not the easy :) )Try again!")
    return percentuale_medium


def difficult():
    title_basics_questions, title_basics_answers = title_basics_qa(difficult_title_basics, 1)
    info_person_questions, info_person_answers = info_person_qa(difficult_info_person, 1)

    title_basics_pairs = list(zip(title_basics_questions, title_basics_answers))
    info_person_pairs = list(zip(info_person_questions, info_person_answers))
    pairs = title_basics_pairs + info_person_pairs
    np.random.shuffle(pairs)
    questions, answers = zip(*pairs)

    score = 0

    for i, question in enumerate(questions):
        print(f"Domanda {i + 1}: {question}")
        answer_options = [answers[i]['correct']] + answers[i]['incorrect']
        np.random.shuffle(answer_options)

        for j, answer in enumerate(answer_options):
            print(f"{j + 1}. {answer}")

        while True:
            user_answer = input("Inserisci il numero della risposta corretta: ")
            try:
                user_answer = int(user_answer)
                if 1 <= user_answer <= len(answer_options) and answer_options[user_answer - 1] == answers[i]['correct']:
                    print("Risposta corretta!\n")
                    score += 1
                    break
                elif user_answer > len(answer_options):
                    print("Risposta non valida.\n")
                else:
                    print("Risposta errata!\n")
                    break
            except ValueError:
                print("Inserisci un numero valido.\n")

    print(f"Il punteggio finale è {score}/{len(questions)}")
    final_score = score / len(questions)
    percentuale_diff = final_score * 100
    if percentuale_diff >= 70:
        print(f"Congratulations! You have passed the difficult quiz with {percentuale_diff}%")
        if 70 <= percentuale_diff <= 90:
            print(f"Good job! You have passed the test but there is still room for improvement. Try again!")
        elif 90 < percentuale_diff <= 100:
            print(f"Fantastic! You have an extraordinary knowledge of film. Too easy? I'm sorry but no room for "
                  f"improvement for you: you are already a God of movies! I mean you know movies from the '800...")
    else:
        print(
            f"Fail! You have done {percentuale_diff}% and you haven't passed the difficult quiz. I get it I also didn't "
            f"pass it")
    return percentuale_diff

'''
FUNZIONE PER SCEGLIERE IL QUIZ CHE VUOI
'''


def choose_quiz():
    while True:
        choosen_quiz = False
        while not choosen_quiz:
            user_answer = input("Inserisci il quiz che vuoi fare tra easy, medium e difficult: ")
            user_answer = user_answer.lower()
            if user_answer == "easy":
                easy()
                choosen_quiz = True
            elif user_answer == "medium":
                medium()
                choosen_quiz = True
            elif user_answer == "difficult":
                difficult()
                choosen_quiz = True
            else:
                print("Quiz non valido. Inserisci un quiz valido.")
        repeat = input("Vuoi ripetere il quiz? (Sì o No): ")
        if repeat.lower() != "sì" and repeat.lower() != "si":
            break


choose_quiz()

