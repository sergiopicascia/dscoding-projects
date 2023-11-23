# AC Milan fans' comments analysis

By Nikita Olefir

## Goal of the project

I intend to analyze how the fans of AC Milan reacted on the results of two games with PSG in the UEFA Champions Leauge 2023/2024. Milan lost 0-3 in the first game, but won 2-1 in the next one.

The goal is to answer the following research questions:

1) Were Milan's fans happier when their favourite team won than are sadder when it lost?
2) Who they adressed during and after the games in their comments?
3) Did they to blamed/praised the team in general or they address individual players + coach?

However, the main goal of the project is to use a variery of libraries for text analysis. The implications of the analysis are limited, but the usage of concepts and instuments are much more valuable.

## Data

To get the information about the fans' reactions, I collect comments from Reddit's threads on the respective topics. To do so, I use Reddit (get yourself familiar with the [documentation](https://www.reddit.com/dev/api/)).

I collect comments from two threads:

1) [Thread](https://www.reddit.com/r/ACMilan/comments/17gb1xz/match_thread_psg_vs_milan_champions_league_202324/) when Milan lost to PSG 0-3.
2) [Thread](https://www.reddit.com/r/ACMilan/comments/17pzwvv/scoreboard_paris_saintgermain_ac_milan/) when Milan won PSG 2-1.

## What is used in the project

### Libraries

Data Manipulation and Analysis: `numpy`, `pandas`. 
Natural Language Processing: `nltk`, `gensim`, `spacy`, `textblob`. 
Data Visualization: `matplotlib`. 
Text Vizualization: `wordcloud`. 
Web Scrapping:`praw`. 
Image processing: `Pillow`. 
Web Application Development: `streamlit`. 

### Topics covered

`Git`, `OOP`, `Modularization`, `Data Manipulation`, `Data Analysis`, `Data Visualization`, `Text Preprocessing`, `Web Application Development`, `API`, `Sentiment Analysis`, `WordCloud`, `Word Embedding`, `Natural Language Processing`.

All the requirments are met.

## Guidlines

All the code is executed in `Main.ipynb`. So, while looking at the actual results, search them there.
There are three folders that contain code.

1) `API_Reddit`: how to use Reddit API + function to extract comments from a thread in a subreddit. There is a README file inside, so follow it if something is unclear.
2) `TextAnalysis`: contains numerous functions for preprocessing and analyzing text data. It does not have a separate README file, but the usage of functions is described in the `Main.ipynb`. Anyway, for each module and function there is documentation written.
3) `Streamlit`: contains the script for streamlit app for analyzing sentiment of the text data and for generating wordclouds. README file describes everything.

## Note

I have not added the csv files of the comments that I get after using Reddit API here in the repository as during classes it was said not to do so. However, if they are needed, I can provide them by email. Tell me if you need them.
