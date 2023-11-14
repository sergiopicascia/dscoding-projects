import pandas as pd


def average_elo(dataframe: pd.DataFrame):
    """This functions creates a column that contains the ELO of each game (the average of the ratings of players)

    Argumens:
        dataframe (pd.DataFrame): a pandas dataframe that contains information about the ELO rating of players

    Returns:
        pd.DataFrame: returns a pandas dataframe that has a "average_elo" column, represening the average rating of a rated game among two chess players

    ---

    Examples:
        average_elo(dataframe_name)
    """
    
    dataframe["average_elo"] = (
        dataframe["white_rating"] + dataframe["black_rating"]
    ) / 2
    return dataframe
