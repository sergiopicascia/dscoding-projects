# Chess Opening Selection System

By Nikita Olefir

## Goal of the project

To create a system that is to select an opening for a chess player based on several factors:

1) The ELO rating of the player (it shows how skillful the player is).
2) The side person plays (either for white or black pieces).
3) The preferred game type (consult with [this source](https://chessfox.com/13-different-types-of-chess-openings/#Flank-Openings)).
4) Initial steps of the opponent.
5) Preference about the lenght of the game (in terms of turns per game)

## Data

I use the [following Kaggle dataset](https://www.kaggle.com/datasets/datasnaek/chess) that is availabvle online. It contains more that 20 000 chess games played on Lichess website (one of the largest website where people can freely play chess online)

...
:chess_pawn:

## Requirments

- usage of GitHub;
- correct modularization;
- import and output of data;
- usage of pandas;
- usage of numPy;
- usage of matplotlib;
- usage of streamlit;

## Progress track

- [X] Create a GitHub folder for the project.
- [X] Create a README file
- [X] Write a function for dataset opening
- [X] Download the dataset
- [X] Create a function to delete unecessary columns
- [X] Create a column with a calculates average ELO rating of games
- [X] Arrange the games according to the ELO rating of the game (by hundreds)
