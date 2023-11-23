## BGG project
###### _by Chi Hoang_

##### Introduction to the project
- The project aims to propose a different method in sorting various types of board games besides focusing on the comparison between their Average scores.
- The project is going to use the data of 23,264 different board games provided on https://boardgamegeek.com/ website, in which players are going to give comments and rates those games on the scale from 0 to 10
  - Link to the dataset: https://island.ricerca.di.unimi.it/~alfio/shared/bgg.csv.zip

##### The idea on the project
- Instead of creating a ranking table based on the Average scores of the games, the project is using the Bayesian Average to make comparisons.
  - `Bayesian Average = (Prior weight * Prior mean + Average score * Number of votes) / (Prior weight + Number of votes)`
    - **Prior weight:** The weight assigned to the prior belief or information.
    - **Prior mean:** The mean of the prior belief or information.
    - **Average score:** The average score or rating given by users.
    - **Number of votes:** The total number of votes or observations.
- In fact, there are lots of cases in which people use Bayesian Average in costume ranking, for example on movies or a specific product.

##### Brief description about the steps:
- Sorting the data
  - The goal is to sort the data which is necessary for calculating Prior weight, Prior mean, Average score, Number of votes and thus, The Bayesian Average score of each game. 
- Visualizing the data
  - The goal is to graphically spot the difference between using Average scores and Bayesian Average scores in sorting the ranking.

##### Structure of the project:
- **`Data.py`:** This python file contains the dataset sorted that is used during the project
- **`Data_visualization.py`:** This file contains the data visualization of the dataset
- **`App.py`:** This file provides codes to run Streamlit app






