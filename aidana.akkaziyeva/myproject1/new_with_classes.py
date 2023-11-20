import pandas as pd
import random


class NetflixQuiz:
    def __init__(self):
        self.data = pd.read_csv('netflix_data.csv')
        self.score = 0
        self.correct_answers = []

    def generate_dir_question(self):
        non_empty_movies = self.data[self.data['director'].notnull()]
        show = random.choice(non_empty_movies['title'])
        question = f"Who directed '{show}'?"             #{}placeholders for variables in a string
        
        correct_answers_all = self.data.loc[self.data['title']==show, 'director'].values[0]
        incorrect_answers_all = non_empty_movies.loc[non_empty_movies['director'] != correct_answers_all, 'director'].unique()
        
    
        return question, correct_answers_all, incorrect_answers_all
        

    def generate_genre_question(self):
        
        correct_answers_all = []
        incorrect_answers_all = []
        all_genres = ['Horror', 'Comedies', 'Romantic Movies', 'Korean TV Shows', 'Documentaries', 'Reality TV','Anime Features', 'Action & Adventure']

        for _ in range(len(self.data)):
            target_genre = random.choice(all_genres)
            question = f"Which of the following belongs to the genre '{target_genre}'?"

            for i in range(len(self.data)):
                genre = self.data.loc[i, 'listed_in']
                if target_genre in genre:
                    correct_answers_all.append(self.data.loc[i, 'title'])
                else: incorrect_answers_all.append(self.data.loc[i, 'title'])
            
            return question, correct_answers_all, incorrect_answers_all



    def generate_rating_question(self):
        question = f"Which of these movies has rating 'TV-MA'(Mature Audience Only)?"
        correct_answers_all = []
        incorrect_answers_all = []
        
        for i in range(len(self.data)):
            if self.data.loc[i, 'rating']=='TV-MA':
                correct_answers_all.append(self.data.loc[i,'title'])
            elif  self.data.loc[i, 'rating']=='TV-Y' or self.data.loc[i, 'rating']=='TV-Y7':
                incorrect_answers_all.append(self.data.loc[i,'title'])
            else: pass
        
        return question, correct_answers_all, incorrect_answers_all


    @staticmethod
    def present_question(question, correct_answers_all, incorrect_answers_all):
        correct_option = random.choice(correct_answers_all)
        incorrect_options = random.sample(incorrect_answers_all, 3)
        
        options = [correct_option]+incorrect_options
        random.shuffle(options)
        print(question)
        for i, answer in enumerate(options, 1):
            print(f"{i}.{answer}")

        user_answer = input("Your choice: ")
        correct_index = options.index(correct_option)+1
        return user_answer, correct_option, correct_index
    


    def play_quiz(self):
            difficulty = input("Choose difficulty (easy, medium, or hard): ")
            num_questions = 3

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
                
            print(f"Your final score is {self.score}/{num_questions}")
            print(f"Correct answers were {', '.join(self.correct_answers)}")


quiz_generator = NetflixQuiz()
quiz_generator.play_quiz()