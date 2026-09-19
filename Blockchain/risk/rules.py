def is_round_number(amount):
    """
    Return True when an amount is a round whole-number value.

    Examples:
        10.0  -> True
        100.0 -> True
        7.5   -> False
        4.25  -> False
    """

    if amount is None:
        return False

    try:
        amount = float(amount)
    except (TypeError, ValueError):
        return False

    return amount > 0 and amount.is_integer()