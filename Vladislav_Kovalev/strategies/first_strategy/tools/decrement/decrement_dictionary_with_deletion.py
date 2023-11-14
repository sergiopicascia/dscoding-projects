def decrement_dictionary_with_deletion(
    *,
    dictionaryForUpdate: dict,
    keyDecrement: str,
) -> dict:
    """
    Decrement key's value in dictionary
    if it's bigger than 1 else pop the key

    Parameters
    ----------
    dictionaryForUpdate: dict
        The dictionary for update
    keyDecrement: str
        The key for update

    Returns
    -------
    dict
        Updated dictionary

    Examples
    --------
    >>> decrement_dictionary_with_deletion(
    ... dictionaryForUpdate=dictionaryForUpdate,
    ... keyDecrement="rooms")
        {"hotels_1": 13,
         "hotels_2": 17,
         "hotels_3": 12}
    """
    if dictionaryForUpdate[keyDecrement] > 1:
        dictionaryForUpdate[keyDecrement] -= 1
        return dictionaryForUpdate
    else:
        dictionaryForUpdate.pop(keyDecrement)
        return dictionaryForUpdate
