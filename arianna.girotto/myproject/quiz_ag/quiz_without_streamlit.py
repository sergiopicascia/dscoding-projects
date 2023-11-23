# QUIZ without Streamlit
# The following code is almost identical to the one 'with Streamlit' but there are some important differences in the
# end. 

# In this quiz there are 4 more functions that differentiates the 3 quizzes: so we have an easy, medium and difficult
# function, and they are all called in the choose_quiz function that to the concept is similar to the run_quiz function.

# The real change in this quiz is the possibility to take different quizzes and store all the results and in the end
# there is a plot that takes into account all the scores of all the quizzes played: so we have an average score.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Quiz:

    def __init__(self, title_basics_path='//Users/ariannagirotto/Desktop/dataset/title.basics.tsv',
                 info_person_path='//Users/ariannagirotto/Desktop/dataset/name.tsv'):
        self.title_basics = pd.read_csv(title_basics_path, sep="\t", quoting=3, encoding='utf-8', engine='python',
                                        nrows=100000)
        self.info_person = pd.read_csv(info_person_path, sep="\t", quoting=3, encoding='utf-8', engine='python',
                                       nrows=100000)
        self.clean_data()

    def clean_data(self):
        self.title_basics = self.title_basics[(self.title_basics['startYear'] != '\\N') &
                                              (self.title_basics['tconst'] != '\\N') &
                                              (self.title_basics['genres'] != '\\N')]
        self.info_person = self.info_person[(self.info_person['birthYear'] != '\\N') &
                                            (self.info_person['primaryName'] != '\\N') &
                                            (self.info_person['primaryProfession'] != '\\N')]

    def filter_sort_data_tb(self, level):
        global filtered_tb
        if level == 'easy':
            filtered_tb = self.title_basics[(self.title_basics['startYear'].astype(int) >= 1990) &
                                            (self.title_basics['startYear'].astype(int) <= 2023)]
            filtered_tb = filtered_tb.sort_values(by='startYear', ascending=False)
        elif level == 'medium':
            filtered_tb = self.title_basics[(self.title_basics['startYear'].astype(int) >= 1940) &
                                            (self.title_basics['startYear'].astype(int) < 1990)]
            filtered_tb = filtered_tb.sort_values(by='startYear', ascending=False)
        elif level == 'difficult':
            filtered_tb = self.title_basics[(self.title_basics['startYear'].astype(int) >= 1800) &
                                            (self.title_basics['startYear'].astype(int) < 1940)]
            filtered_tb = filtered_tb.sort_values(by='startYear', ascending=True)

        return filtered_tb

    def filter_sort_data_ip(self, level):
        global filtered_ip
        if level == 'easy':
            filtered_ip = self.info_person[(self.info_person['birthYear'].astype(int) >= 1960) &
                                           (self.info_person['birthYear'].astype(int) <= 1987)]
            filtered_ip = filtered_ip.sort_values(by='birthYear', ascending=False)
        elif level == 'medium':
            filtered_ip = self.info_person[(self.info_person['birthYear'].astype(int) >= 1930) &
                                           (self.info_person['birthYear'].astype(int) < 1960)]
            filtered_ip = filtered_ip.sort_values(by='birthYear', ascending=False)
        elif level == 'difficult':
            filtered_ip = self.info_person[(self.info_person['birthYear'].astype(int) >= 1800) &
                                           (self.info_person['birthYear'].astype(int) < 1930)]
            filtered_ip = filtered_ip.sort_values(by='birthYear', ascending=True)

        return filtered_ip

    def title_basics_type1(self, df):
        random_tconst = np.random.choice(df['tconst'], replace=False)
        movie_title = df.loc[df['tconst'] == random_tconst, 'primaryTitle'].values[0]
        question = f"In what year was released {movie_title}?"

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

    def title_basics_type2(self, df):
        random_tconst = np.random.choice(df['tconst'], replace=False)
        movie_title = df.loc[df['tconst'] == random_tconst, 'primaryTitle'].values[0]
        question = f"What genre is the film/TV series?{movie_title}?"

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

    def title_basics_qa(self, df, num_type1_qa, num_type2_qa):
        questions = []
        answers = []

        for _ in range(num_type1_qa):
            question, answer = self.title_basics_type1(df)
            questions.append(question)
            answers.append(answer)

        for _ in range(num_type2_qa):
            question, answer = self.title_basics_type2(df)
            questions.append(question)
            answers.append(answer)

        return questions, answers

    def info_person_type1(self, df):
        random_nconst = np.random.choice(df['nconst'], replace=False)
        person_name = df.loc[df['nconst'] == random_nconst, 'primaryName'].values[0]
        question = f"When was born {person_name}?"

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

    def info_person_type2(self, df):
        random_nconst = np.random.choice(df['nconst'], replace=False)
        person_name = df.loc[df['nconst'] == random_nconst, 'primaryName'].values[0]
        question = f"Which are the primary professions of {person_name}?"

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

    def info_person_qa(self, df, num_type1_qa, num_type2_qa):
        questions = []
        answers = []

        for _ in range(num_type1_qa):
            question, answer = self.info_person_type1(df)
            questions.append(question)
            answers.append(answer)

        for _ in range(num_type2_qa):
            question, answer = self.info_person_type2(df)
            questions.append(question)
            answers.append(answer)

        return questions, answers

    def q_a(self, level):
        title_basics_questions, title_basics_answers = self.title_basics_qa(self.filter_sort_data_tb(level), 2, 2)
        info_person_questions, info_person_answers = self.info_person_qa(self.filter_sort_data_ip(level), 2, 2)

        title_basics_pairs = list(zip(title_basics_questions, title_basics_answers))
        info_person_pairs = list(zip(info_person_questions, info_person_answers))
        pairs = title_basics_pairs + info_person_pairs
        np.random.shuffle(pairs)
        questions, answers = zip(*pairs)
        return questions, answers

    def easy(self):
        questions, answers = self.q_a('easy')
        score = 0

        for i, question in enumerate(questions):
            print(f"Question {i + 1}: {question}")
            answer_options = [answers[i]['correct']] + answers[i]['incorrect']
            np.random.shuffle(answer_options)

            for j, answer in enumerate(answer_options):
                print(f"{j + 1}. {answer}")

            while True:
                user_answer = input("Insert the number of the correct answer: ")
                try:
                    user_answer = int(user_answer)
                    if 1 <= user_answer <= len(answer_options) and answer_options[user_answer - 1] == answers[i][
                        'correct']:
                        print("Correct answer!\n")
                        score += 1
                        break
                    elif user_answer > len(answer_options):
                        print("Answer not valid.\n")
                    else:
                        print("Wrong answer!")
                        print(f"The right one was'{answers[i]['correct']}'\n")
                        break
                except ValueError:
                    print("Insert a valid number.\n")
        final_score = score / len(questions)
        perc_easy = final_score * 100
        if perc_easy >= 50:
            print(f"Congratulations! You have passed the easy quiz with {perc_easy}%")
            if 50 <= perc_easy <= 80:
                print(f"Good job! You have passed the test but there is still room for improvement. Try again!")
            elif 80 < perc_easy <= 100:
                print(f"Fantastic! You have a nice knowledge of film. Too easy? Try the medium quiz")
        else:
            print(
                f"Fail! You have done {perc_easy}% and you haven't passed the easy quiz. Are you living in a cave?Try "
                f"again!")
        return perc_easy

    def medium(self):
        questions, answers = self.q_a('medium')
        score = 0

        for i, question in enumerate(questions):
            print(f"Question {i + 1}: {question}")
            answer_options = [answers[i]['correct']] + answers[i]['incorrect']
            np.random.shuffle(answer_options)

            for j, answer in enumerate(answer_options):
                print(f"{j + 1}. {answer}")

            while True:
                user_answer = input("Insert the number of the correct answer: ")
                try:
                    user_answer = int(user_answer)
                    if 1 <= user_answer <= len(answer_options) and answer_options[user_answer - 1] == answers[i][
                        'correct']:
                        print("Correct answer!\n")
                        score += 1
                        break
                    elif user_answer > len(answer_options):
                        print("Answer not valid.\n")
                    else:
                        print("Wrong answer!")
                        print(f"The right one was '{answers[i]['correct']}'\n")
                        break
                except ValueError:
                    print("Insert a valid number.\n")

        final_score = score / len(questions)
        perc_medium = final_score * 100
        if perc_medium >= 60:
            print(f"Congratulations! You have passed the medium quiz with {perc_medium}%")
            if 60 <= perc_medium <= 80:
                print(f"Good job! You have passed the test but there is still room for improvement. Try again!")
            elif 80 < perc_medium <= 100:
                print(f"Fantastic! You have a very good knowledge of film. Too easy? Try the difficult quiz")
        else:
            print(
                f"Fail! You have done {perc_medium}% and you haven't passed the medium quiz ( at least it was the medium "
                f"and not the easy :) )Try again!")
        return perc_medium

    def difficult(self):
        questions, answers = self.q_a('difficult')
        score = 0

        for i, question in enumerate(questions):
            print(f"Question {i + 1}: {question}")
            answer_options = [answers[i]['correct']] + answers[i]['incorrect']
            np.random.shuffle(answer_options)

            for j, answer in enumerate(answer_options):
                print(f"{j + 1}. {answer}")

            while True:
                user_answer = input("Insert the number of the correct answer: ")
                try:
                    user_answer = int(user_answer)
                    if 1 <= user_answer <= len(answer_options) and answer_options[user_answer - 1] == answers[i][
                        'correct']:
                        print("Correct answer!\n")
                        score += 1
                        break
                    elif user_answer > len(answer_options):
                        print("Answer not valid.\n")
                    else:
                        print("Wrong answer!")
                        print(f"The right one was'{answers[i]['correct']}'\n")
                        break
                except ValueError:
                    print("Insert a valid number.\n")

        final_score = score / len(questions)
        perc_diff = final_score * 100
        if perc_diff >= 70:
            print(f"Congratulations! You have passed the difficult quiz with {perc_diff}%")
            if 70 <= perc_diff <= 90:
                print(f"Good job! You have passed the test but there is still room for improvement. Try again!")
            elif 90 < perc_diff <= 100:
                print(f"Fantastic! You have an extraordinary knowledge of film. Too easy? I'm sorry but no room for "
                      f"improvement for you: you are already a God of movies! I mean you know movies from the '800...")
        else:
            print(
                f"Fail! You have done {perc_diff}% and you haven't passed the difficult quiz. I get it I also didn't "
                f"pass it")
        return perc_diff

    def choose_quiz(self):
        quiz_results = {'easy': [], 'medium': [], 'difficult': []}
        while True:
            user_answer = input("Choose the level of the quiz between 'easy', 'medium' and 'difficult': ").lower()
            if user_answer in quiz_results:
                if user_answer == "easy":
                    score = self.easy()
                elif user_answer == "medium":
                    score = self.medium()
                elif user_answer == "difficult":
                    score = self.difficult()

                quiz_results[user_answer].append(score)

                repeat = input("Do you want to try again? (Yes or No): ").lower()
                if repeat == "no":
                    break
            else:
                print("Quiz not valid. Insert a valid quiz.")

        for quiz_type, scores in quiz_results.items():
            if scores:
                average_score = sum(scores) / len(scores)
                color = 'green' if (average_score >= 50 and quiz_type == 'easy') or \
                                   (average_score >= 60 and quiz_type == 'medium') or \
                                   (average_score >= 70 and quiz_type == 'difficult') else 'red'
                plt.bar(quiz_type, average_score, color=color, label=quiz_type)
                plt.text(quiz_type, average_score, f'{average_score:.2f}%')

        plt.ylim(0, 100)
        plt.ylabel('Average Score')
        plt.title('Results')
        plt.legend()
        plt.show()


quiz = Quiz()
quiz.choose_quiz()
