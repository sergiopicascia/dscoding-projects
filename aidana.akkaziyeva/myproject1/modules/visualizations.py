import streamlit as st


def show_movie_durations_histogram(movie_length):
    st.subheader("Distribution of Movies by Duration")
    st.bar_chart(movie_length)


def shows_by_season_chart(season_counts):
    st.subheader("Distribution of TV shows by Seasons")
    st.bar_chart(season_counts)


def release_year_chart(release_year_data):
    st.subheader("Distribution of Movies and TV shows by Year")
    st.line_chart(release_year_data)


def show_visualizations(movie_length, season_counts, release_year_data):
    show_movie_durations_histogram(movie_length)
    shows_by_season_chart(season_counts)
    release_year_chart(release_year_data)
