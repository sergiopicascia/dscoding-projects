import pandas as pd


def dataframe_unnecessary_columns_deletion(dataframe: pd.DataFrame):
    """This function deletes the necessary columns from
    the pandas dataframe with data about chess games

    Argumenst:
        dataframe (pd.dataframe): the pandas dataframe that was created from the csv file with information about chess games

    Returns:
       pd.DataFrame: returns a pandas dataframe. It returns only rated games with only necessary columns:
       1)id
       2)turns
       3)victory_status
       4)winner
       5)white_rating
       6)black_rating
       7)moves
       8)opening_eco
       9)opening_name
       10)opening_ply

       columns that are deleted:
       1)rated
       2)created_at
       3)last_move_at
       4)increment_code
       5)white_id
       6)black_id
    ---

    Examples:
        dataframe_unnecessary_columns_deletion(dataframe)
    """
    dataframe = dataframe[dataframe["rated"]]
    
    return dataframe.drop(
        columns=[
            "rated",
            "created_at",
            "last_move_at",
            "increment_code",
            "white_id",
            "black_id",
        ],
        axis=1,
    )
