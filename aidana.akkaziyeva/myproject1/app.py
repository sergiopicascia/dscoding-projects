import streamlit as st
import pandas as pd
from netflix_quiz import questions
import visualisations

def load_data():
    return pd.read_csv('netflix_data.csv')

netflix_data = load_data()
q_data = questions(netflix_data)

def difficulty_match(difficulty):
    if difficulty == 'Easy':
        return q_data.generate_genre_question()
    elif difficulty == 'Medium':
        return q_data.generate_rating_question()
    elif difficulty == 'Hard':
        return q_data.generate_dir_question()

def main():
    visualisations.display_visualizations(netflix_data)

    difficulty = st.selectbox("Select Difficulty", ["Easy", "Medium", "Hard"])

    # Initialize session variables
    if 'questions' not in st.session_state or st.session_state.difficulty != difficulty:
        st.session_state.difficulty = difficulty
        st.session_state.questions = [difficulty_match(difficulty) for _ in range(5)]
        st.session_state.user_answers = [""] * 5
        st.session_state.score = 0
        st.session_state.show_results = False

    for i, (question, correct_option, options) in enumerate(st.session_state.questions):
        st.header(f"Question {i + 1}: {question}")
        selected_option = st.radio(f"Options:", options, key=f"q{i}")
        st.session_state.user_answers[i] = selected_option

    # Check answers and calculate score
    if st.button("Submit"):
        st.session_state.show_results = True
        for i, (_, correct_option, _) in enumerate(st.session_state.questions):
            if st.session_state.user_answers[i] == correct_option:
                st.session_state.score += 1

    # Display final score after submitting all answers
    if st.session_state.show_results and all(st.session_state.user_answers):
        st.success(f"Your total score: {st.session_state.score}")
        st.markdown("Correct Answers:")
        for i, (_, correct_option, _) in enumerate(st.session_state.questions):
            st.write(f"Question {i + 1}: {correct_option}")
            
if __name__ == "__main__":
    main()
