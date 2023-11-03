import pandas as pd


def construct_result(
    *,
    dataGuests: pd.DataFrame,
    dataHotels: pd.DataFrame,
    resultFrame: pd.DataFrame,
) -> pd.DataFrame:
    """
    Construction of result frame with prices, guests and hotels

    Parameters
    ----------
    dataHotels: pd.DataFrame
        dataframe of hotels and rooms
    resultDict: dict
        dataframe of preferences
    dataGuests: pd.DataFrame
        dataframe of guests

    Returns
    -------
    pd.DataFrame
        DataFrame with guests, prices and hotels
    """
    resultFrame = resultFrame.merge(dataGuests[["guest", "discount"]], how="left")
    resultFrame = resultFrame.merge(dataHotels[["hotel", "price"]], how="left")

    resultFrame.columns = [nameColumn.upper() for nameColumn in resultFrame.columns]
    resultFrame["NETTO"] = resultFrame["PRICE"] * (1 - resultFrame["DISCOUNT"])

    return resultFrame.sort_values("GUEST")
