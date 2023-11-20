import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st


netflix_data = pd.read_csv('netflix_data.csv')



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


