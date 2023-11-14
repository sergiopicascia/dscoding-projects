import numpy as np
import pandas as pd

def group_elo(dataframe: pd.DataFrame):
    """This function groups the games by the ELO rating. It creates groups in terms of hundres (manimum: 800-8900; maximum: 2400-2499)

    Arguments:
        dataframe (pd.DataFrame): a pandas dataframe that contains the column with the ELo ratings of games

    Returns:
        pd.DataFrame: a pandas dataframe with a column that contains infromation to what group every record(game) belongs
    
    ---

     Examples:
        group_elo(dataframe_name)
    """    
    groups = np.arange(800, 2600, 100)
    labels = [f"{i}-{i+99}" for i in groups[:-1]]
    dataframe['elo_groups'] = pd.cut(dataframe['average_elo'], bins=groups, labels=labels, include_lowest=True)
    return dataframe