import pandas as pd
import random

class Quiz:
    def __init__(self, data):
        self.data = data

    def generate_question_by_difficulty(self, difficulty):
        # Filter data by difficulty
        filtered_data = self.data[self.data['difficulty'] == difficulty]

        # Randomly select a question type
        question_type = random.choice(['director_actor', 'starred_movie'])

        if question_type == 'director_actor':
            return self.generate_director_actor_question(filtered_data)
        elif question_type == 'starred_movie':
            return self.generate_starred_movie_question(filtered_data)

    def generate_director_actor_question(self, filtered_data):
        # Ensure we select a title with a known person in the chosen category
        valid_row = False
        while not valid_row:
            title_row = filtered_data.sample()
            title_type = title_row['titleType'].values[0]
            title_name = title_row['primaryTitle'].values[0]
            title_difficulty = title_row['difficulty'].values[0]
            category = random.choice(['director', 'actor', 'actress'])  # Including actress category
            correct_answer_rows = title_row[title_row['category'] == category]

            if not correct_answer_rows.empty:
                valid_row = True
                correct_answer = correct_answer_rows['primaryName'].values[0]

        # Get other choices
        other_choices = filtered_data[filtered_data['category'] == category]['primaryName'].unique()
        other_choices = [choice for choice in other_choices if choice != correct_answer]
        choices = random.sample(list(other_choices), 3) + [correct_answer]
        random.shuffle(choices)

        if category in ['director', 'actor', 'actress']:
            question = f"\n\nWho is the {category} of the {title_type} {title_name}?   {title_difficulty} Point(s)"

        return question, choices, correct_answer

    def generate_starred_movie_question(self, filtered_data):
        # Ensure we select a person with a known title in the chosen category
        valid_row = False
        while not valid_row:
            person_row = filtered_data[filtered_data['category'].isin(['actor', 'actress'])].sample()
            person_name = person_row['primaryName'].values[0]
            title_type = person_row['titleType'].values[0]
            title_difficulty = person_row['difficulty'].values[0]
            # Get the correct title and create choices
            correct_title = person_row['primaryTitle'].values[0]
            other_titles = filtered_data['primaryTitle'].unique()
            other_titles = [title for title in other_titles if title != correct_title]
            choices = random.sample(list(other_titles), 3) + [correct_title]
            random.shuffle(choices)

            valid_row = True

        question = f"\n\nWhich {title_type} did {person_name} star in?   {title_difficulty} Point(s)"

        return question, choices, correct_title

    def get_number_of_questions(self):
        try:
            num_questions = int(input("How many questions would you like to answer? "))
            return num_questions
        except ValueError:
            print("Please enter a valid number.")
            return self.get_number_of_questions()

    def take_quiz(self):
        num_questions = self.get_number_of_questions()
        total_points = 0
        max_possible_points = 0

        for _ in range(num_questions):
            # Randomly select a difficulty level for each question
            difficulty = random.choice(self.data['difficulty'].unique())
            max_possible_points += difficulty

            question, choices, correct_answer = self.generate_question_by_difficulty(difficulty)
            print(question)
            for i, choice in enumerate(choices, 1):
                print(f"{i}. {choice}")

            while True:
                try:
                    answer = input("Enter your answer (1-4): ")
                    selected_choice = choices[int(answer) - 1]
                    break  # Breaks the loop if the input is valid
                except (ValueError, IndexError):
                    print("Please enter a valid answer to the question above.")


            if selected_choice == correct_answer:
                print("\nCorrect!")
                total_points += difficulty
            else:
                print("\nIncorrect. The correct answer was:", correct_answer)

        print(f"\nQuiz Completed. You scored {total_points} out of {max_possible_points} points.")
