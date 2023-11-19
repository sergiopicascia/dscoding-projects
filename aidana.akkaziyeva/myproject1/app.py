import streamlit as st
import pandas as pd
from netflix_quiz import questions
import matplotlib.pyplot as plt
import random

# Loading data once and cache the result
@st.cache_data
def load_data():
    return pd.read_csv('netflix_data.csv')

# Preprocessing data and cache the result
@st.cache_data
def preprocess_data(data):
    data['duration'] = data['duration'].str.replace(' Seasons', '').str.replace(' min', '').str.replace(' Season', '')
    data['duration'] = pd.to_numeric(data['duration'], errors='coerce')
    movies_data = data[(data['type'] == 'Movie') & (data['duration'] <= 180)]
    tv_shows_data = data[(data['type'] == 'TV Show') & (data['duration'] <= 11)]
    season_counts = tv_shows_data['duration'].value_counts().sort_index()
    show_release_year = data.loc[data['type'] == 'TV Show','release_year'].value_counts()
    movie_release_year = data.loc[data['type'] == 'Movie','release_year'].value_counts()
    release_year_data = pd.DataFrame({'TV Shows': show_release_year, 'Movies': movie_release_year})

    return movies_data, tv_shows_data, season_counts, release_year_data

def show_movie_durations_histogram(movies_data):
    st.subheader('Movie Durations')
    fig, ax = plt.subplots()
    ax.hist(movies_data['duration'], bins=20, edgecolor='black')
    ax.set_xlabel('Duration (minutes)')
    ax.set_ylabel('Frequency')
    ax.set_xticks(range(0, 180, 30))
    st.pyplot(fig)

def shows_by_season_chart(season_counts):
    st.subheader('Distribution of TV shows by Seasons')
    st.bar_chart(season_counts)

def release_year_chart(release_year_data):
    st.subheader('Distribution of TV shows by Year')
    st.line_chart(release_year_data)


def display_visualizations(data):
    st.title('Netflix Data Visualizations')
    movies_data, tv_shows_data, season_counts, release_year_data = preprocess_data(data)
    show_movie_durations_histogram(movies_data)
    shows_by_season_chart(season_counts)
    release_year_chart(release_year_data)







def main():
    netflix_data = load_data()
    q_data=questions(netflix_data)
    # Initialize session variables
    if 'questions' not in st.session_state:
        st.session_state.questions = [q_data.generate_rating_question() for _ in range(3)]
        st.session_state.user_answers = [""] * 3
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




