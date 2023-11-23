import streamlit as st
from createQuiz import MovieQuiz
from visual import VisualData
import pandas as pd

class FinalData:

    def __init__(self, file_path):
        self.file_path = file_path
        self.data_movie = None
        self.quiz = None
        self.data_visual = None

    #check if attribute 'quiz' is in session state so that web page won't clear session again and again
    #then user selects difficulty level of a quiz
    def start_quiz(self):
        if 'quiz' not in st.session_state:
            st.session_state.quiz = None

        difficulty_level = st.selectbox("Select difficulty level:", ['easy', 'medium', 'hard'])

        if st.session_state.quiz is None or st.session_state.quiz.difficulty_level != difficulty_level:
            st.session_state.quiz = MovieQuiz(self.data_movie, difficulty_level)

    #show question and possible answers as radio buttons
    def show_questions(self):
        for i, question in enumerate(st.session_state.quiz.questions):
            st.write(f"#{i + 1}: {question}")
            selected_answer = st.radio("Please, choose the answer:", st.session_state.quiz.answers[i])
            st.session_state.quiz.selected_answers[i] = selected_answer
            st.write(f"Chosen answer: {selected_answer}")

    #calculate user's final score
    def calculate_score(self):
        score = sum(selected_answer == st.session_state.quiz.answers[i][st.session_state.quiz.correct_indices[i]]
            for i, selected_answer in enumerate(st.session_state.quiz.selected_answers))
        return score

    #format of results displayed to user
    def show_results(self, score):
        st.subheader(f"Your result is: {score}/{st.session_state.quiz.number_questions}")
        for i, correct_index in enumerate(st.session_state.quiz.correct_indices):
            st.write(f"#{i + 1}: Correct Answer - **{st.session_state.quiz.answers[i][correct_index]}**")

    #collect whole quiz with choosing difficulty level, showing question and showing final score with correct answers
    def show_quiz(self):
        st.title("Movie Quiz Project")

        self.data_movie = pd.read_csv(self.file_path)

        self.start_quiz()
        self.show_questions()

        if st.button("Submit"):
            score = self.calculate_score()
            self.show_results(score)

    #show visualisation data of dataset
    def show_visual(self):
        self.data_visual = VisualData(self.file_path)

        st.subheader("Original dataset")
        st.write(self.data_visual.dataset)

        st.subheader("The line chart illustrates the number of movies produced in a specific year.")
        line_chart_figure = self.data_visual.create_line_chart()
        st.pyplot(line_chart_figure)

        st.subheader("The pie chart illustrates the distribution of movies based on durations (in minutes).")
        pie_chart_runtime_figure = self.data_visual.create_pie_chart_runtime()
        st.pyplot(pie_chart_runtime_figure)

        st.subheader("The scatter plot illustrates relationship between 'Vote Count' and 'Vote Average'")
        scatter_plot_figure = self.data_visual.create_scatter_plot()
        st.pyplot(scatter_plot_figure)

if __name__ == "__main__":

    file_path = "/Users/apple/Documents/GitHub/dscoding-projects/ayagoz.shayakhmetova/CISI-project/cisi_project/new_movies_1.csv"
    final_data = FinalData(file_path)

    final_data.show_quiz()
    final_data.show_visual()
