import pandas as pd
import numpy as np
import random


class NetflixQuiz:
    def __init__(self, data):
        self.data = data

    def generate_dir_question(self):
        non_empty = self.data[self.data["director"].notnull()]
        show_row = non_empty.sample(n=1).iloc[0]
        show, correct_opt = show_row["title"], show_row["director"]

        question = f"Who directed '{show}'?"

        incorrect_opts = (
            non_empty[non_empty["director"] != correct_opt]
            .sample(n=3)["director"]
            .tolist()
        )

        options = [correct_opt, *incorrect_opts]
        random.shuffle(options)
        return question, correct_opt, options

    def generate_genre_question(self):
        all_genres = [
            "Horror",
            "Comedies",
            "Romantic Movies",
            "Documentaries",
            "Reality TV",
            "Anime Features",
        ]

        target_genre = np.random.choice(all_genres)
        question = f"Which of the following belongs to the genre '{target_genre}'?"

        genre_data = self.data[
            self.data["listed_in"].str.contains(target_genre)
        ]  # dataframe
        correct_opt = genre_data.sample()["title"].iloc[0]

        non_genre_data = self.data[~self.data["listed_in"].str.contains(target_genre)]
        incorrect_opts = non_genre_data.sample(n=3)[
            "title"
        ].tolist()  # convert the pandas Series into a Python list

        options = [correct_opt, *incorrect_opts]  # * is unpacking operator
        random.shuffle(options)
        return question, correct_opt, options

    def generate_rating_question(self):
        question = "Which of these movies has rating 'TV-MA' (Mature Audience Only)?"
        correct_answers_all = self.data[self.data["rating"] == "TV-MA"][
            "title"
        ].tolist()  # list of titles
        incorrect_opts = (
            self.data[self.data["rating"].isin(["TV-Y", "TV-Y7"])]
            .sample(n=3)["title"]
            .tolist()
        )

        correct_opt = random.choice(correct_answers_all)
        options = [correct_opt, *incorrect_opts]
        random.shuffle(options)
        return question, correct_opt, options

    def generate_cast_question(self):
        non_empty = self.data[self.data["cast"].notnull()]
        show_row = non_empty.sample(n=1).iloc[0]

        show, cast = show_row["title"], show_row["cast"]
        question = f"Who starred in '{show}'?"

        cast_list = [actor.strip() for actor in cast.split(",")]
        correct_opt = cast_list[0]

        incorrect_opts_all = set(
            self.data["cast"].str.split(",").explode().str.strip()
        ) - set(cast_list)
        incorrect_opts = random.sample(list(incorrect_opts_all), 3)
        options = [correct_opt, *incorrect_opts]

        random.shuffle(options)
        return question, correct_opt, options

    def generate_country_question(self):
        non_empty = self.data[
            (self.data["type"] == "Movie") & self.data["country"].notnull()
        ]
        show_row = non_empty.sample(n=1).iloc[0]

        show, correct_opt = show_row["title"], show_row["country"].split(",")[0].strip()
        question = f"In which country was the movie '{show}' produced?"

        unique_countries = set(
            country.strip()
            for countries in non_empty["country"]
            for country in countries.split(",")
            if country.strip()
        )  # the latter checks if stripped 'country' is not empty(empty is false)

        incorrect_opts_all = set(unique_countries) - {correct_opt}

        incorrect_opts = random.sample(list(incorrect_opts_all), 3)
        options = [correct_opt, *incorrect_opts]

        random.shuffle(options)
        return question, correct_opt, options

    def generate_question(self, difficulty):
        question_types_medium = [
            self.generate_rating_question,
            self.generate_country_question,
        ]
        question_types_hard = [self.generate_dir_question, self.generate_cast_question]
        if difficulty == "Easy":
            return self.generate_genre_question()
        elif difficulty == "Medium":
            chosen_question = random.choice(question_types_medium)
            return chosen_question()
        elif difficulty == "Hard":
            chosen_question = random.choice(question_types_hard)
            return chosen_question()
