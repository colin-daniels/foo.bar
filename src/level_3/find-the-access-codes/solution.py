def solution(l):
    """
    Get the number of "lucky triples" that a list of integers contains.

    Warnings:
        Since Commander Lambda loves efficiency, essentially no input checking
        is done.

    Args:
        l: List of length between 2 and 2000 inclusive containing positive
           integers between 1 and 999999 inclusive.

    Returns:
        Number of "lucky triples" (l[i], l[j], l[k]) where i < j < k
        and l[i] divides l[j] which divides l[k].

    """
    n = len(l)
    triples = 0

    # keeps track of how many elements each entry in the list divides that are
    # past it in the list
    num_divides = [0] * n

    # here we iterate backwards because we need to calculate num_divides for
    # later entries before earlier ones
    for i in range(n - 1, -1, -1):
        x = l[i]

        # how many elements that `x` divides which are past it in the list
        divides = 0

        # now go through the rest of the list forwards
        for j in range(i + 1, n):
            y = l[j]
            if y % x == 0:
                divides += 1
                # because we're iterating backwards, we can already calculate
                # the number of "lucky triples" formed by (x, y, z) where z is
                # just any of the numbers that y can divide
                triples += num_divides[j]

        num_divides[i] = divides

    return triples

