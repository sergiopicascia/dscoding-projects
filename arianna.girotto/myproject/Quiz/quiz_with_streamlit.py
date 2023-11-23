# QUIZ

# Importing the libraries necessary for this project
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Creating an only class called 'Quiz' that contains all the methods for creating the quiz with the application web of
# Streamlit
class Quiz:
    # Defining the constructure method. It has the two file tsv that I have used to do the project and has a recalling
    # of the following method 'clean.data()'
    def __init__(self, title_basics_path='//Users/ariannagirotto/Desktop/dataset/title.basics.tsv',
                 info_person_path='//Users/ariannagirotto/Desktop/dataset/name.tsv'):
        self.title_basics = pd.read_csv(title_basics_path, sep="\t", quoting=3, encoding='utf-8', engine='python',
                                        nrows=100000)
        self.info_person = pd.read_csv(info_person_path, sep="\t", quoting=3, encoding='utf-8', engine='python',
                                       nrows=100000)
        self.clean_data()
    # It's a function to do data manipulation to the purpose of eliminate all those rows that don't have the information
    # that we need to create the questions and the answers
    def clean_data(self):
        self.title_basics = self.title_basics[(self.title_basics['startYear'] != '\\N') &
                                              (self.title_basics['tconst'] != '\\N') &
                                              (self.title_basics['genres'] != '\\N')]
        self.info_person = self.info_person[(self.info_person['birthYear'] != '\\N') &
                                            (self.info_person['primaryName'] != '\\N') &
                                            (self.info_person['primaryProfession'] != '\\N')]

    # The next two functions are identical but one is for the dataset of title_basics and the other one for the dataset
    # of info_person. I have split the dataset into three different parts, using the start year of the movies for
    # 'title_basics' and the birth year of the actors for 'info_person' as the criterion: in this way I have created
    # different levels of difficulty based on the quiz the user chooses to play: therefore, the further back in time
    # we go, the more likely it is that the user doesn't know the answers, and consequently the difficulty increases.

    def filter_sort_data_tb(self, level):
        global filtered_tb
        if level == 'EASY':
            filtered_tb = self.title_basics[(self.title_basics['startYear'].astype(int) >= 1990) &
                                            (self.title_basics['startYear'].astype(int) <= 2023)]
            filtered_tb = filtered_tb.sort_values(by='startYear', ascending=False)
        elif level == 'MEDIUM':
            filtered_tb = self.title_basics[(self.title_basics['startYear'].astype(int) >= 1940) &
                                            (self.title_basics['startYear'].astype(int) < 1990)]
            filtered_tb = filtered_tb.sort_values(by='startYear', ascending=False)
        elif level == 'DIFFICULT':
            filtered_tb = self.title_basics[(self.title_basics['startYear'].astype(int) >= 1800) &
                                            (self.title_basics['startYear'].astype(int) < 1940)]
            filtered_tb = filtered_tb.sort_values(by='startYear', ascending=True)

        return filtered_tb

    def filter_sort_data_ip(self, level):
        global filtered_ip
        if level == 'EASY':
            filtered_ip = self.info_person[(self.info_person['birthYear'].astype(int) >= 1960) &
                                           (self.info_person['birthYear'].astype(int) <= 1987)]
            filtered_ip = filtered_ip.sort_values(by='birthYear', ascending=False)
        elif level == 'MEDIUM':
            filtered_ip = self.info_person[(self.info_person['birthYear'].astype(int) >= 1930) &
                                           (self.info_person['birthYear'].astype(int) < 1960)]
            filtered_ip = filtered_ip.sort_values(by='birthYear', ascending=False)
        elif level == 'DIFFICULT':
            filtered_ip = self.info_person[(self.info_person['birthYear'].astype(int) >= 1800) &
                                           (self.info_person['birthYear'].astype(int) < 1930)]
            filtered_ip = filtered_ip.sort_values(by='birthYear', ascending=True)

        return filtered_ip
    # Created the dataset to use to create the questions and answers, the next step is to create a 'pattern' of the
    # questions we want to ask the user. This is the purpose of the following 7 functions.

    # As before the functions are pratically identical and the only difference is the dataset used. The first 2
    # functions defined two different types of question: they are built with a fixed structure which doesn't change,
    # and it's the frame of the question and with a flexible one that is represented by the title of the movie. This
    # is chosen randomly and identified by its id. The right answers are identified with the use of the id and the wrong
    # ones are chosen randomly(but they can't be equal to the right ones or to each other). All the answer are stored
    # in a dictionary: in this way we can distinguish them and keep the right ones separated from the wrongs ones
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
    # Same as the one before: it changes only the fixated part
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
    # This function is useful to keep together all the questions of one dataset
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
    # These 3 functions are identical to the ones before: it only changes the dataset
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
    # This function keep together all the questions and the answers, independently on the dataset. It's useful because
    # generates the number of the question that we want to implement and keep together and mix the questions and
    # answers, without compromising the pairs of question-answer. In this way we have all the questions and answers
    # paired and ready to use
    def q_a(self, level):
        title_basics_questions, title_basics_answers = self.title_basics_qa(self.filter_sort_data_tb(level), 2, 2)
        info_person_questions, info_person_answers = self.info_person_qa(self.filter_sort_data_ip(level), 2, 2)

        title_basics_pairs = list(zip(title_basics_questions, title_basics_answers))
        info_person_pairs = list(zip(info_person_questions, info_person_answers))
        pairs = title_basics_pairs + info_person_pairs
        np.random.shuffle(pairs)
        questions, answers = zip(*pairs)
        return questions, answers
    # This is the difference between the quiz_with_streamlit and the quiz_without_streamlit.
    # This is the function that implement the web application of the quiz: it has a first part that is the choice of the
    # quiz by the user, a second part that is the play of the game (that uses the questions and answers found before)
    # and finally there is the final part that is the one with the score and the graphic.
    def run_quiz(self):
        global color, final_score
        # Initializing the quiz state
        if 'quiz_started' not in st.session_state:
            st.session_state.quiz_started = False
            st.session_state.current_index = 0
            st.session_state.score = 0
            st.session_state.selected_level = None
            st.session_state.user_answer = None

        # Form for selecting the quiz level
        if not st.session_state.quiz_started:
            st.title('WELCOME TO IMDB QUIZ!')
            st.subheader(':red[DISCLAIMER!]')
            st.write(
                'Before you start the quiz remember that there is only 1 correct answer. Also once you click the button'
                ' the answer is saved so beware! The quiz is composed by 8 questions and you can choose the level of the quiz.'
                'If you play the easy one you will have movies and/or tv series that are more recent: the more difficult '
                'the quiz is, the more obscure the titles are. Enjoy it! ')
            selected_level = st.selectbox("Choose the level of the quiz", ['EASY', 'MEDIUM', 'DIFFICULT'])
            start_button = st.button('Start Quiz')

            if start_button:
                st.session_state.quiz_started = True
                st.session_state.current_index = 0
                st.session_state.score = 0
                st.session_state.selected_level = selected_level
                st.session_state.user_answer = None

        # Quiz's logic
        if st.session_state.quiz_started:
            questions, answers = self.q_a(st.session_state.selected_level)

            if st.session_state.current_index < len(questions):
                question = questions[st.session_state.current_index]
                answer = answers[st.session_state.current_index]

                st.markdown(f"**Question {st.session_state.current_index + 1}: {question}**", )
                options = [answer['correct']] + answer['incorrect']
                np.random.shuffle(options)

                # Show the radio button only if no response has been given yet
                if st.session_state.user_answer is None:
                    st.session_state.user_answer = st.radio("Select your answer", options,
                                                            key=f"question_{st.session_state.current_index}")
                    if st.session_state.user_answer == answer['correct']:
                        st.session_state.score += 1
                    st.session_state.current_index += 1
                    st.session_state.user_answer = None  # Reset the answer for the next question

            else:
                st.header(f"Your :red[final score]: {st.session_state.score} out of {len(questions)}")
                final_score = (st.session_state.score / len(questions)) * 100

                # This is another difference between the quizzes that increases the difficulty.
                # I have implemented 3 different passing thresholds for the different level of the quiz: the more
                # difficult the quiz is, the higher the rate for which the user pass the test is.
                if st.session_state.selected_level == 'EASY':
                    color = 'green' if final_score >= 50 else 'red'
                    if final_score >= 50:
                        st.write(f"Congratulations! You have passed the easy quiz with {final_score}%")
                        if 50 <= final_score <= 80:
                            st.write(f"Good job! You have passed the test but there is still room for improvement.")
                        elif 80 < final_score <= 100:
                            st.write(f"Fantastic! You have a nice knowledge of film. Too easy? Try the medium quiz")
                    else:
                        st.write(
                    f"Fail! You have done {final_score}% and you haven't passed the easy quiz. Are you living in a cave?Try "
                    f"again!")

                if st.session_state.selected_level == 'MEDIUM':
                    color = 'green' if final_score >= 60 else 'red'
                    if final_score >= 60:
                        st.write(f"Congratulations! You have passed the medium quiz with {final_score}%")
                        if 60 <= final_score <= 80:
                            st.write(
                                f"Good job! You have passed the test but there is still room for improvement. Try again!")
                        elif 80 < final_score <= 100:
                            st.write(
                                f"Fantastic! You have a very good knowledge of film. Too easy? Try the difficult quiz")
                    else:
                        st.write(
                            f"Fail! You have done {final_score}% and you haven't passed the medium quiz ( at least it was the medium "
                            f"and not the easy :) )Try again!")

                if st.session_state.selected_level == 'DIFFICULT':
                    color = 'green' if final_score >= 70 else 'red'
                    if final_score >= 70:
                        st.write(f"Congratulations! You have passed the difficult quiz with {final_score}%")
                        if 70 <= final_score <= 90:
                            st.write(
                                f"Good job! You have passed the test but there is still room for improvement. Try again!")
                        elif 90 < final_score <= 100:
                            st.write(
                                f"Fantastic! You have an extraordinary knowledge of film. Too easy? I'm sorry but no room for "
                                f"improvement for you: you are already a God of movies! I mean you know movies from the '800...")
                    else:
                        st.write(
                            f"Fail! You have done {final_score}% and you haven't passed the difficult quiz. I get it I also didn't "
                            f"pass it")
                # In the end this part creates a histogram that shows the user's results visually
                plt.figure(facecolor='none')
                plt.bar(st.session_state.selected_level, final_score, color=color,
                        label=st.session_state.selected_level)
                plt.text(st.session_state.selected_level, final_score, f'{final_score:.2f}%')

                plt.ylim(0, 100)
                plt.ylabel('FINAL SCORE',fontsize=11)
                plt.title('RESULTS', fontweight='bold', fontsize=16)
                plt.legend()
                st.pyplot(plt)

# Usage
# To see the quiz we have to assign the class to a variabile and then call the function 'run_quiz'
quiz = Quiz()
quiz.run_quiz()
