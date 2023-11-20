import pandas as pd
import random
import streamlit as st


class questions:
    def __init__(self, data):
        self.data = data
    
        
    def generate_dir_question(self):
        non_empty_movies = self.data[self.data['director'].notnull()]
        show = non_empty_movies.sample()['title'].iloc[0]
        question = f"Who directed '{show}'?"

        correct_answers_all = self.data.loc[self.data['title'] == show, 'director'].tolist()
        incorrect_answers_all = non_empty_movies.loc[~non_empty_movies['director'].isin(correct_answers_all), 'director'].unique().tolist()

        correct_opt = random.choice(correct_answers_all)
        options = [correct_opt] + random.sample(incorrect_answers_all, 3)
        random.shuffle(options)
        return question, correct_opt, options



    def generate_genre_question(self):
        correct_answers_all = []
        incorrect_answers_all = []
        all_genres = ['Horror', 'Comedies', 'Romantic Movies', 'Korean TV Shows', 'Documentaries', 'Reality TV', 'Anime Features', 'Action & Adventure']

        target_genre = random.choice(all_genres)
        question = f"Which of the following belongs to the genre '{target_genre}'?"

        correct_answers_all = self.data[self.data['listed_in'].str.contains(target_genre)]['title'].tolist()
        incorrect_answers_all = self.data[~self.data['listed_in'].str.contains(target_genre)]['title'].tolist()

        correct_opt = random.choice(correct_answers_all)
        options = [correct_opt] + random.sample(incorrect_answers_all, 3)
        random.shuffle(options)
        return question, correct_opt, options


    def generate_rating_question(self):
        question = "Which of these movies has rating 'TV-MA' (Mature Audience Only)?"
        correct_answers_all = self.data[self.data['rating'] == 'TV-MA']['title'].tolist()
        incorrect_answers_all = self.data[(self.data['rating'] == 'TV-Y') | (self.data['rating'] == 'TV-Y7')]['title'].tolist()

        correct_opt = random.choice(correct_answers_all)
        options = [correct_opt] + random.sample(incorrect_answers_all, 3)
        random.shuffle(options)
        return question, correct_opt, options
    



"""""
    @staticmethod
    def present_question(question, correct_answers_all, incorrect_answers_all):
        correct_option = random.choice(correct_answers_all)
        incorrect_options = random.sample(incorrect_answers_all, 3)
        
        options = [correct_option]+incorrect_options
        random.shuffle(options)
        print(question)
        for i, answer in enumerate(options, 1):
            print(f"{i}.{answer}")

        st.selectbox("Select your answer:",
                                     options=options,
                                     key=)
        user_answer = st.selectbox('Your choice: ', ())
        correct_index = options.index(correct_option)+1
        return user_answer, correct_option, correct_index
    

    
    

    def play_quiz(self, num_questions, difficulty):
            #difficulty = input("Choose difficulty (easy, medium, or hard): ")

            for _ in range(num_questions):      #you are not interested in how many times the loop is run,just that it should run some specific number of times overall.
                if difficulty == 'easy':
                    question, correct_answers_all, incorrect_answers_all = self.generate_genre_question()
                elif difficulty == 'medium':
                    question, correct_answers_all, incorrect_answers_all = self.generate_rating_question()
                elif difficulty == 'hard':
                    question, correct_answers_all, incorrect_answers_all = self.generate_dir_question()
                else:
                    print("Invalid difficulty level. Please choose from 'easy', 'medium', or 'hard'.")
                    return
                
                user_answer, correct_option,  correct_index = self.present_question(question, correct_answers_all, incorrect_answers_all)
                self.correct_answers.append(correct_option)
                if int(user_answer) == correct_index:
                    self.score += 1
                else: pass
                
            #print(f"Your final score is {self.score}/{num_questions}")
            #print(f"Correct answers were {', '.join(self.correct_answers)}")
           
            return {
            'score': self.score,
            'num_questions': num_questions,
            'correct_answers': self.correct_answers
        }
#netflix_data = pd.read_csv('netflix_data.csv')
#quiz_generator = NetflixQuiz(netflix_data)
#quiz_generator.play_quiz()

"""