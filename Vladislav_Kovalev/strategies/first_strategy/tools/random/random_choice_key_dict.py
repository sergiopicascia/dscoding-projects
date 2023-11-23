import numpy as np


def random_choice_key_dict(
    *,
    dictionaryForChoice: dict,
) -> str:
    """
    Choose a random key from dict

    Parameters
    ----------
    dictionaryForChoice: dict
        The dictionary for choice

    Returns
    -------
    str
        Choosen str

    Examples
    --------
    >>> random_choice_key_dict(
    ... dictionaryForChoice={"item": 10})
        "item"
    """
    keysDictionaryForChoice = list(dictionaryForChoice.keys())
    keyChoosen = np.random.choice(keysDictionaryForChoice)
    return keyChoosen
