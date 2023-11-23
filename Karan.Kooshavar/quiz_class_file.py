import random
from questions import generate_director_actor_question, generate_starred_movie_question


class quiz_class:
    def __init__(self, data):
        self.data = data

    def generate_question_by_difficulty(self, difficulty):
        # Filter data by difficulty
        filtered_data = self.data[self.data['difficulty'] == difficulty]

        # Randomly select a question type
        question_type = random.choice(['director_actor', 'starred_movie'])

        if question_type == 'director_actor':
            return generate_director_actor_question(filtered_data)
        elif question_type == 'starred_movie':
            return generate_starred_movie_question(filtered_data)

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
