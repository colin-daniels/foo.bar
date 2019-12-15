def solution(x, y):
    """
    Compares two almost identical lists of prisoner IDs where one of the lists contains an additional ID and then
    returns that ID.

    Warnings:
        Since Commander Lambda loves efficiency, very little input checking is done. Crucially, it's assumed that
        the longer of the two lists has exactly one extra ID that is not present in the other list. Input lists are
        also not checked for proper length (between 1 and 99) and ids are not validated to be integers between -1000
        and 1000.

    Args:
        x: A list of non-unique prisoner IDs.
        y: Another list of IDs that is almost identical to `x`.

    Returns:
        int: The additional ID.
    """
    # ensure x is the shorter list
    if len(x) > len(y):
        x, y = y, x

    # To find the extra ID, we just build a set from the (presumed) common ids,
    # and exit when we find the first ID not in our set.
    x_ids = frozenset(x)
    for idx in y:
        if idx not in x_ids:
            return idx

    # Note: Since we exit early, we don't verify that y only has one more extra ID,
    #   and we also don't verify that every ID in x is present in y. One way to do this
    #   would be to build two sets and use symmetric difference, but it takes ~30% longer.
    #     [different_id] = frozenset(y) ^ frozenset(x)
    #     return different_id
    #
    # We do know however that if we got to this point, all of the IDs in the longer list are
    # present in the shorter one.
    raise ValueError('The longer input list must contain one ID not present in the other.')
