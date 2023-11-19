import streamlit as st
import pandas as pd
import plotly.express as px

st.title('Board Games ranking')

average_table = pd.read_csv('average_table.csv')
average_table.rename(columns={'title': 'Title', 'rating_average': 'Average rating score'}, inplace=True)
average_table.index += 1

bayesian_table = pd.read_csv('bayesian_table.csv')
bayesian_table.rename(columns={'title': 'Title', 'bayesian_average': 'Bayesian Average rating score'}, inplace=True)
bayesian_table.index += 1

full_table = pd.read_csv('game_name.csv')
full_table.rename(columns={'title': 'Game'}, inplace=True)
full_table.index += 1

st.markdown("#### Game list")
st.write(full_table[['Game']])

search_game = st.text_input(
    label="Search for your game's ranking",
    value='',
    placeholder="Search for your game's ranking ...",
    label_visibility="collapsed"
)
search_game = search_game.lower()

average_score_result = average_table[average_table['Title'].str.lower().str.contains(search_game)]
bayesian_score_result = bayesian_table[bayesian_table['Title'].str.lower().str.contains(search_game)]

if not average_score_result.empty and not bayesian_score_result.empty:
    st.write(f"**The game's ranking based on the Bayesian Average rating score:**")
    st.write(bayesian_score_result[['Title', 'Bayesian Average rating score']])
    fig = px.scatter(x=bayesian_table['rating_number'], y=bayesian_table['Bayesian Average rating score'])
    fig.update_layout(
        xaxis_title='Number of votes',
        yaxis_title='Bayesian Average score',
    )
    st.plotly_chart(fig, use_container_width=True)

    st.write(f"**The game's ranking based on the Average score:**")
    st.write(average_score_result[['Title', 'Average rating score']])
    fig = px.scatter(x=average_table['rating_number'], y=average_table['Average rating score'])
    fig.update_layout(
        xaxis_title='Number of votes',
        yaxis_title='Average score',
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning(f"No data found for {search_game}")
