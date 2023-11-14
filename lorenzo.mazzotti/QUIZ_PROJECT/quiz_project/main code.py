import random
import pandas as pd
df = pd.read_table("namebasic.tsv")


score = []

# Number of questions to ask
number_questions = 3

for i in range(number_questions):
 question = df.sample(2)
 #da rivedere questa parte!!

 # Print the question
 print("when was this person born", question['birthYear'], "?")

 # Getting the answer
 answer = question['birthYear']
 user_answer = input("write your answer here: ")

 # problems with lower/upper case solver
 user_answer = user_answer.lower()
 answer = answer.str.lower()

 # answer correct/wrong
 if user_answer == answer.values[0]:
    print("Correct")
    score.append(1)
 else:
    print("Wrong The correct answer is", answer.values[0])
    score.append(0)


final_score = sum(score)
print("Your score is:", final_score, "congratulations")