# app.py
import streamlit as st
import pandas as pd
from modules.preprocessing import preprocess_data
from modules.visualizations import show_visualizations
from modules.quiz import NetflixQuiz


def main():
    data = pd.read_csv('netflix_data.csv')
    quiz_data = NetflixQuiz(data)
    
    movie_length, season_counts, release_year_data = preprocess_data(data)

    # Displaying visualizations
    show_visualizations(movie_length, season_counts, release_year_data)
    
    st.title('Quiz Time!')
    difficulty = st.selectbox("Select Difficulty", ["Easy", "Medium", "Hard"])

    # Initializing session variables
    if 'questions' not in st.session_state or st.session_state.difficulty != difficulty:
        st.session_state.difficulty = difficulty
        st.session_state.questions = [quiz_data.generate_question(difficulty) for _ in range(5)]
        st.session_state.user_answers = [""] * 5
        st.session_state.score = 0
        st.session_state.show_results = False

    for i, (question, correct_option, options) in enumerate(st.session_state.questions):
        st.header(f"{i + 1}. {question}")
        selected_option = st.radio(f"Options:", options, key=f"q{i}")
        st.session_state.user_answers[i] = selected_option

    # Checking answers and calculate score
    if st.button("Submit"):
        st.session_state.show_results = True
        for i, (_, correct_option, _) in enumerate(st.session_state.questions):
            if st.session_state.user_answers[i] == correct_option:
                st.session_state.score += 1

    # Displaying final score after submitting all answers
    if st.session_state.show_results and all(st.session_state.user_answers):
        st.success(f"Your total score: {st.session_state.score}/5")
        st.markdown("Correct Answers:")
        for i, (_, correct_option, _) in enumerate(st.session_state.questions):
            st.write(f"Question {i + 1}: {correct_option}")

if __name__ == "__main__":
    main()
