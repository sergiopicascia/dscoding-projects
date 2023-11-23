import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from board_game_project.Data import DataSet
from board_game_project.Data_Visualization import DataVisualization

df = pd.read_csv('bgg.csv')
full_table, average_table, bayesian_table = DataSet(df).calculate_game_statistics()

st.title('Board Games ranking')
st.markdown("#### Game list:\n "
            "* There are 23,264 different Board Games")

full_table.rename(columns={'title': 'Game'}, inplace=True)
full_table.index += 1
st.dataframe(full_table['Game'], width=2000)

viz = DataVisualization(x=full_table['Number of votes'], y=full_table['Average rating score'],
                        z=full_table['Bayesian Average rating score'], title=full_table['Game'])

title = full_table['Game']
x = full_table['Number of votes']
y = full_table['Average rating score']
z = full_table['Bayesian Average rating score']

bayesian_table.rename(columns={'title': 'Game'}, inplace=True)
bayesian_table.index += 1

st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot(viz.plot_bayesian_ranking())

search_game = st.text_input(
    label="Search for your game's ranking",
    value='',
    placeholder="Search for your game's ranking ...",
    label_visibility="collapsed"
)
search_game = search_game.lower()

bayesian_score_result = bayesian_table[bayesian_table['Game'].str.lower().str.contains(search_game)]


def display_data(search_game, bayesian_table, bayesian_score_result):
    st.subheader("Bayesian Average score ranking")
    if search_game != '':
        st.write(f"**The game's ranking based on the Bayesian Average rating score:**")
        st.dataframe(bayesian_score_result[['Game', 'Number of votes', 'Bayesian Average rating score']], width=2000)
    else:
        st.warning(f"No data found for {search_game}")

    fig_bayesian, ax_bayesian = plt.subplots()
    ax_bayesian.scatter(bayesian_table['Number of votes'], bayesian_table['Bayesian Average rating score'],
                        label='All Games', alpha=0.5)
    if not bayesian_score_result.empty:
        bayesian_score_result = bayesian_score_result.head()
        ax_bayesian.scatter(bayesian_score_result['Number of votes'],
                            bayesian_score_result['Bayesian Average rating score'],
                            color='red', label=f'Searched Game: {search_game}', marker='o')
    ax_bayesian.set_xlabel('Number of votes')
    ax_bayesian.set_ylabel('Bayesian Average rating score')
    ax_bayesian.legend()
    st.pyplot(fig_bayesian)


display_data(search_game, bayesian_table, bayesian_score_result)

