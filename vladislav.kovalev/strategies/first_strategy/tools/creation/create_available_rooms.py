import pandas as pd


def create_available_rooms(
    *,
    dataHotels: pd.DataFrame,
) -> dict:
    """
    Create a dictionary with whole available rooms

    Parameters
    ----------
    dataHotels : pd.DataFrame
        The dataset of hotels and rooms

    Returns
    -------
    dict
        Generated dictionary

    Examples
    --------
    >>> create_available_rooms(dataHotels=dataHotels)
        {'hotel_1': 13,
         'hotel_2': 18,
         'hotel_3': 12,
         'hotel_4': 18,
         'hotel_5': 7,
        ...
         'hotel_396': 5,
         'hotel_397': 12,
         'hotel_398': 14,
         'hotel_399': 16,
         'hotel_400': 14}
    """
    dataHotelsRows = dataHotels[["hotel", "rooms"]].T
    dataHotelsRows = dataHotelsRows.to_dict().items()
    dataAvailableRooms = {
        row_object[1]["hotel"]: row_object[1]["rooms"] for row_object in dataHotelsRows
    }
    return dataAvailableRooms
