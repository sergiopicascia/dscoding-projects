import random
import pandas as pd
import data_generator
import matplotlib.pyplot as plt

genres_expanded = pd.read_csv('genres_expanded.csv')
netflix_data = pd.read_csv('netflix_data.csv')



question, correct_answer, incorrect_answers = data_generator.generate_genre_question(netflix_data)

print(f"Question: {question}")
print(f"Correct Answer: {correct_answer}")
print(f"Incorrect Answers: {incorrect_answers}")

#data_generator.present_dir_question(question, correct_answer, incorrect_answers)



"""
def main():
    score = 0
    for _ in range(4):
        question, correct_answer, incorrect_answers = data_generator.generate_genre_question(netflix_data)
        data_generator.present_genre_question(question, correct_answer, incorrect_answers)

        user_answer = int(input("Enter your answer(1-4):"))
        if data_generator.evaluate_answer(user_answer, correct_answer):
            score = score + 1
    print(f"Your final score is {score}. The correct answers are...")  #nado dodelat'


    

main()
"""

