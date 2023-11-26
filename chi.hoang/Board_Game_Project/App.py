import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from board_game_project.Data import DataSet


def plot_scatter(ax, data_table, x_col, y_col, label, color='blue', marker='o'):
    ax.scatter(data_table[x_col], data_table[y_col], label=label, alpha=0.5, color=color)
    ax.set_xlabel('Number of votes')
    ax.set_ylabel(y_col)
    ax.legend()


def display_data(search_game, data_table, score_result, title):
    """
    Display game rankings and plot scatter plots.

    :parameter search_game: Game title to search for
    :parameter data_table: Pandas DataFrame containing the full data
    :parameter score_result: Pandas DataFrame containing the search results
    :parameter title: Title for the ranking
    """
    st.subheader(f"{title} Ranking")
    if search_game != '':
        st.write(f"**The game's ranking based on the {title}:**")
        st.dataframe(score_result[['Game', 'Number of votes', title]], width=2000)
    else:
        st.warning(f"No data found for {search_game}")

    # Plot ranking with the searched game highlighted in red
    fig, ax = plt.subplots()
    plot_scatter(ax, data_table, 'Number of votes', title, 'All Games')
    if not score_result.empty:
        score_result = score_result.head(5)
        plot_scatter(ax, score_result, 'Number of votes', title, f'Searched Game: {search_game}', 'red', 'o')
    st.pyplot(fig)


# Load the dataset and calculate game statistics
df = pd.read_csv('bgg.csv')
full_table, average_table, bayesian_table, wilson_table = DataSet(df).calculate_game_statistics()

st.title('Board Games ranking')
st.markdown("#### Game list:\n "
            "* There are 23,264 different Board Games")

full_table.rename(columns={'title': 'Game'}, inplace=True)
full_table.index += 1
st.dataframe(full_table['Game'], width=2000)

average_table.rename(columns={'title': 'Game'}, inplace=True)
average_table.index += 1

bayesian_table.rename(columns={'title': 'Game'}, inplace=True)
bayesian_table.index += 1

wilson_table.rename(columns={'title': 'Game'}, inplace=True)
wilson_table.index += 1

search_game = st.text_input(
    label="Search for your game's ranking",
    value='',
    placeholder="Search for your game's ranking ...",
    label_visibility="collapsed"
)
search_game = search_game.lower()

bayesian_score_result = bayesian_table[bayesian_table['Game'].str.lower().str.contains(search_game)]
average_score_result = average_table[average_table['Game'].str.lower().str.contains(search_game)]
wilson_score_result = wilson_table[wilson_table['Game'].str.lower().str.contains(search_game)]

display_data(search_game, bayesian_table, bayesian_score_result, 'Bayesian Average rating score')
display_data(search_game, average_table, average_score_result, 'Average rating score')
display_data(search_game, wilson_table, wilson_score_result, 'Wilson lower bound')
