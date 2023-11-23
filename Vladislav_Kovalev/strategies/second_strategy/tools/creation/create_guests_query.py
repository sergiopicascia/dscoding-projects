import pandas as pd


def create_guests_query(
    *,
    dataPreferences: pd.DataFrame,
):
    """
    Create a guests query by extracting
    the order number from the guest names.

    Parameters:
    -----------
        dataPreferences (pd.DataFrame): The dataset containing guest information.

    Returns:
    --------
        pd.DataFrame: The updated dataset with an added 'order' column.

    Example:
    --------
    >>> dataPreferences = pd.DataFrame({'guest': ['guest_1', 'guest_2', 'guest_3']})
    >>> create_guests_query(dataPreferences=dataPreferences)
        guest  order
        0  guest_1      1
        1  guest_2      2
        2  guest_3      3

    In this example, the function takes a DataFrame dataPreferences
    with a 'guest' column and adds an 'order' column by extracting
    the order number from each guest name.
    The resulting DataFrame will have the 'order'
    column with corresponding order numbers.
    """
    dataPreferences["order"] = dataPreferences["guest"].apply(
        lambda x: int(x.split("_")[1])
    )
    return dataPreferences
