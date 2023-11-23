import pandas as pd
import random


def generate_director_actor_question(filtered_data):
        # Ensure we select a title with a known person in the chosen category
        valid_row = False
        while not valid_row:
            title_row = filtered_data.sample()
            title_type = title_row['titleType'].values[0]
            title_name = title_row['primaryTitle'].values[0]
            title_difficulty = title_row['difficulty'].values[0]
            category = random.choice(['director', 'actor', 'actress'])  # Including actress category
            correct_answer_rows = title_row[title_row['category'] == category]

            if not correct_answer_rows.empty:
                valid_row = True
                correct_answer = correct_answer_rows['primaryName'].values[0]

        # Get other choices
        other_choices = filtered_data[filtered_data['category'] == category]['primaryName'].unique()
        other_choices = [choice for choice in other_choices if choice != correct_answer]
        choices = random.sample(list(other_choices), 3) + [correct_answer]
        random.shuffle(choices)

        if category in ['director', 'actor', 'actress']:
            question = f"\n\nWho is the {category} of the {title_type} {title_name}?   {title_difficulty} Point(s)"

        return question, choices, correct_answer

def generate_starred_movie_question(filtered_data):
        # Ensure we select a person with a known title in the chosen category
        valid_row = False
        while not valid_row:
            person_row = filtered_data[filtered_data['category'].isin(['actor', 'actress'])].sample()
            person_name = person_row['primaryName'].values[0]
            title_type = person_row['titleType'].values[0]
            title_difficulty = person_row['difficulty'].values[0]
            # Get the correct title and create choices
            correct_title = person_row['primaryTitle'].values[0]
            other_titles = filtered_data['primaryTitle'].unique()
            other_titles = [title for title in other_titles if title != correct_title]
            choices = random.sample(list(other_titles), 3) + [correct_title]
            random.shuffle(choices)

            valid_row = True

        question = f"\n\nWhich {title_type} did {person_name} star in?   {title_difficulty} Point(s)"

        return question, choices, correct_title