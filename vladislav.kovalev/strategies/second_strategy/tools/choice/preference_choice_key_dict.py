def preference_choice_key_dict(
    *,
    preferenceList: list,
    dictionaryForChoice: dict,
) -> str:
    """
    The function iterates through each hotel in the
    preferenceList and checks if it exists as a key in the dictionaryForChoice.
    If a preferred hotel is found in the dictionary, the function returns the hotel.
    If none of the preferred hotels are found in the dictionary, the function returns None.

    Parameters:
    -----------
    preferenceList: list
        Represents a list of preferred hotels.
    dictionaryForChoice: dict
        Represents a dictionary containing hotel choices.

    Returns:
    -------
    str
        Returns a string representing the preferred hotel if it exists in the dictionary, otherwise returns None.

    Examples:
    ---------
    >>> preference_list = ["Hotel A", "Hotel B", "Hotel C"]
    >>> dictionary_for_choice = {
    ...    "Hotel A": "Option 1",
    ...    "Hotel B": "Option 2",
    ...    "Hotel D": "Option 3"
    ... }
    >>> preference_choice_key_dict(
    ...    preferenceList=preference_list,
    ...    dictionaryForChoice=dictionary_for_choice
    ... )
        Hotel A
    """
    for preferencedHotel in preferenceList:
        if preferencedHotel in dictionaryForChoice:
            return preferencedHotel
    return None
