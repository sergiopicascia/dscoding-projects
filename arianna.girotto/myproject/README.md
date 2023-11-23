# QUIZ PROJECT

## ASSIGNMENT
The purpose of the project is to automatically create multiple-choice film-related quizzes, exploiting data from IMDb. Each quiz must consist of one question and four possible answers, only one of which must be correct. The program that generates the quizzes must also implement a criterion to generate the possible answers proportional to the difficulty of the desired quiz. The program must also allow a human player to answer the quiz and must measure his/her performance with an overall score that takes into account the difficulty of each individual question. IMDb data can be acquired through specific APIs (such as Cinemagoer) or existing datasets, such as IMDb Dataset.

## HOW TO
My project is divided in two different files, called 'quiz_with_Streamlit' and 'quiz_without_Streamlit'. The name of the files underline the difference between the two but there is a deeper difference that is not so obvious.
When I started doing the project, I left at the end the implementation of the web application with Streamlit: so when I first approached Streamlit I already had done the writing of the code. Since the beginning I have realized that the code I wrote, which worked well, wasn't the best to adapt in Streamlit and this was because the original code had many loops in the functions and I discovered this is not the best cup of tea for Streamlit. 

For this reason I had to modify a part of the code so that it would work with Streamlit. But since there are some details that I couldn't include in the Streamlit version I included also the version of the code Strealit-free, the original one, with loops and a couple more functionalities.

I have used the IMBD Dataset but not all the files, just 'title_basics' and 'name_basics'.

## STREAMLIT 
The web application is very simple, intuitive and user-friendly. It's divided in 3 parts:
- Choose the quiz that you want to play
- Play the quiz
- Show the results with the final score and graphic

I've added a disclaimer so that the user has the right instruction to play the game and also I've added a few mini comments on the final result that depend on the score and on the type of quiz choosen.





