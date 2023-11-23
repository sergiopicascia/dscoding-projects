import pandas as pd


def preprocess_data(data):
    data["duration"] = (
        data["duration"]
        .str.replace(" Seasons", "")
        .str.replace(" min", "")
        .str.replace(" Season", "")
    )
    data["duration"] = pd.to_numeric(data["duration"], errors="coerce")
    movies_data = data[(data["type"] == "Movie")]
    movie_length = movies_data["duration"].value_counts().sort_index()
    tv_shows_data = data[(data["type"] == "TV Show")]
    season_counts = tv_shows_data["duration"].value_counts().sort_index()
    show_release_year = data.loc[
        data["type"] == "TV Show", "release_year"
    ].value_counts()
    movie_release_year = data.loc[
        data["type"] == "Movie", "release_year"
    ].value_counts()
    release_year_data = pd.DataFrame(
        {"TV Shows": show_release_year, "Movies": movie_release_year}
    )
    return movie_length, season_counts, release_year_data
