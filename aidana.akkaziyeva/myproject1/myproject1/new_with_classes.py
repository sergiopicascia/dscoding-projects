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
        question = f"Which of the following belongs to the horror genre?"
        correct_answers_all = []
        incorrect_answers_all = []

        for i in range(len(self.data)):
            genre = self.data.loc[i, 'listed_in']
            if 'Horror' in genre:
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
        print(question)
        for i, answer in enumerate(options, 1):
            print(f"{i}.{answer}")

        user_answer = input("Your choice: ")
        return user_answer

    def play_quiz(self):
            difficulty = input("Choose difficulty (easy, medium, or hard): ")
            num_questions = 5

            for _ in range(num_questions):
                if difficulty == 'easy':
                    question, correct_answers, incorrect_answers = self.generate_genre_question()
                elif difficulty == 'medium':
                    question, correct_answers, incorrect_answers = self.generate_dir_question()
                elif difficulty == 'hard':
                    question, correct_answers, incorrect_answers = self.generate_rating_question()
                else:
                    print("Invalid difficulty level. Please choose from 'easy', 'medium', or 'hard'.")
                    return
                
                user_answer = self.present_question(question, correct_answers, incorrect_answers)

                if user_answer and int(user_answer) == 1:
                    self.score += 1
                    # Store the data consistently in the correct_answers list
                    self.correct_answers.append((question, correct_answers, []))
                else:
                    self.correct_answers.append((question, correct_answers, incorrect_answers))


            print(f"Your final score: {self.score}/{num_questions}")

            print("\nCorrect and Incorrect Answers:")
            for question, *answers in self.correct_answers:
                print(question)
                if len(answers) == 1:
                    print(f"Correct Answer: {answers[0]}")
                else:
                    print(f"Correct Answer: {answers[0]}")
                    print(f"Incorrect Answers: {', '.join(answers[1:])}")
                print("\n")

    """def present_dir_question (self, question, correct_answer, incorrect_answers):
        print(question)
        all_answers = [correct_answer] + incorrect_answers 
        #[]-creating a list from a single string, incorrect answers is already a list of strings

        random.shuffle(all_answers)

        for i, answer in enumerate(all_answers, 1):
            print(f"{i}. {answer}")      #{}placeholders for variables in a string """



    """  def choose_difficulty_level (self, difficulty):
        if difficulty == 'easy':
            return self.generate_genre_question
        elif difficulty == 'medium':
            return self.generate_dir_question
        elif difficulty == 'hard':
            return 
        else: print("Invalid difficulty level. Please choose from 'easy', 'medium', or 'hard'.") """


quiz_generator = NetflixQuiz()
quiz_generator.play_quiz()