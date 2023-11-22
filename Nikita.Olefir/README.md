# AC Milan fans' comments analysis

By Nikita Olefir

## Goal of the project

I intend to analyze how the fans of AC Milan reacted on the results of two games with PSG in the UEFA Champions Leauge 2023/2024. Milan lost 0-3 in the first game, but won 2-1 in the next one.

The goal is to answer the following research questions:

1) Are Milan's fans  happier when their favourite team wins than are sadder when it loses?
2) Do fans of Milan tend to 'forgive' the coach of the Milan (Stefano Pioli) after victories
3) Do they ten to blame/praise the team in general or they address individual players + coach?

## Data

To get the information about the fans' reactions, I collect comments from Reddit's threads on the respective topics. To do so, I use Reddit (get yourself familiar with the [documentation](https://www.reddit.com/dev/api/)).

I collect comments from two threads:

1) [Thread](https://www.reddit.com/r/ACMilan/comments/17gb1xz/match_thread_psg_vs_milan_champions_league_202324/) when Milan lost to PSG 0-3.
2) [Thread](https://www.reddit.com/r/ACMilan/comments/17pzwvv/scoreboard_paris_saintgermain_ac_milan/) when Milan won PSG 2-1.

## Requirments

- usage of GitHub;
- correct modularization;
- import and output of data;
- usage of pandas;
- usage of numPy;
- usage of matplotlib;
- usage of streamlit;

## Guidlines


## Progress track

- [X] Create a GitHub folder for the project.
- [X] Create a README file
- [X] Develop Reddit API application
- [X] Write a function to extract all comments of particular threads on Reddit
- [X] Collect all comments of users written in the threads.
- [X] Write functions to preprocess text data
- [X] Add documentation to the TextPreprocessor class
- [X] Find the most frequent words in the dataframes
- [X] Add documentatio to the WordReplacer class
- [X] Add documentation to the functions from "descriptive_statistics" module
- [X] Create functions to add stemmed words and lemmatized words
- [X] Create a function to hash the names of the authors
- [X] Create a function to change the date format of the time when comments were created
- [ ] Create a wordcloud for both of the dataframes
- [ ] Add documentation to the module with streamlit usage
- [ ] Add a README file for the streamlit folder
- [X] Make a sentiment analysis over time
- [X] Create a column to the datatable to indicate whether comment was given what Milan lost or won
- [X] Make words embedding and visualize it
- [ ] Add guidelines for users
- [ ] Add requirments file
- [ ] Redact gitigrnore file
- [ ] Redact README file
- [ ] Create a Jupyter Notebook to present the code
- [ ] Redact the whole project
- [ ] Add a list of concepts/topics/packages covered in this project
