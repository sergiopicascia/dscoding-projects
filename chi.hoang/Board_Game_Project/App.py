import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from Data import DataSet
from Data_Visualization import DataVisualization

df = pd.read_csv('bgg.csv')
full_table, average_table, bayesian_table = DataSet(df).calculate_game_statistics()

st.title('Board Games ranking')
st.markdown("#### Game list:\n "
            "* There are 23,264 different Board Games")

full_table.rename(columns={'title': 'Game'}, inplace=True)
full_table.index += 1
st.write(full_table['Game'])

bayesian_table.rename(columns={'title': 'Game'}, inplace=True)
bayesian_table.index += 1

average_table.rename(columns={'title': 'Game', 'rating_average': 'Average rating score'}, inplace=True)
average_table.index += 1

viz = DataVisualization(average_table['Number of votes'], average_table['Average rating score'], bayesian_table['Bayesian Average rating score'])
search_game = st.text_input(
    label="Search for your game's ranking",
    value='',
    placeholder="Search for your game's ranking ...",
    label_visibility="collapsed"
)
search_game = search_game.lower()

average_score_result = average_table[average_table['Game'].str.lower().str.contains(search_game)]
bayesian_score_result = bayesian_table[bayesian_table['Game'].str.lower().str.contains(search_game)]

if not average_score_result.empty and not bayesian_score_result.empty:
    st.write(f"**The game's ranking based on the Bayesian Average rating score:**")
    st.write(bayesian_score_result[['Game', 'Number of votes', 'Bayesian Average rating score']])
    fig_bayesian, ax_bayesian = plt.subplots()
    ax_bayesian.scatter(bayesian_table['Number of votes'], bayesian_table['Bayesian Average rating score'],
                    label='All Games', alpha=0.5)

    if not bayesian_score_result.empty:
        ax_bayesian.scatter(bayesian_score_result['Number of votes'], bayesian_score_result['Bayesian Average rating score'],
                        color='red', label=f'Searched Game: {search_game}', marker='o')
    ax_bayesian.set_ylabel('Bayesian Average rating score')
    ax_bayesian.legend()
    st.pyplot(fig_bayesian)

    st.write(f"**The game's ranking based on the Average score:**")
    st.write(average_score_result[['Game', 'Number of votes', 'Average rating score']])
    fig_average, ax_average = plt.subplots()
    ax_average.scatter(average_table['Number of votes'], average_table['Average rating score'], label='All Games',
                       alpha=0.5)

    if not average_score_result.empty:
        ax_average.scatter(average_score_result['Number of votes'], average_score_result['Average rating score'],
                           color='red', label=f'Searched Game: {search_game}', marker='o')
    ax_average.set_xlabel('Number of votes')
    ax_average.set_ylabel('Average rating score')
    ax_average.legend()
    st.pyplot(fig_average)

else:
    st.warning(f"No data found for {search_game}")

