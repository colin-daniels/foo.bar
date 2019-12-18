def solution(n):
    """
    Get the number of operations needed to reduce number of pellets to 1.

    Warnings:
        Since Commander Lambda loves efficiency, essentially no input checking
        is done.

    Args:
        n: A positive integer (number of pellets) as a string, containing at
        most 309 digits.

    Returns:
        The minimum number of operations needed to transform the number of
        pellets to 1.
    """
    n = long(n)
    ops = 0

    # Interestingly, this seems (?) to follow http://oeis.org/A003313 for n up
    # to 26, although I have not looked into it further.
    while n != 1:
        ops += 1

        # The easiest way of looking at this is to consider the binary
        # representation of n, and what the operations do to change it.
        #
        # If n is even, aka the binary representation ends in a 0, we
        # just go ahead and divide by two
        if n & 0b1 == 0:
            n = n // 2
        else:
            # If n is odd, we decide whether to add or subtract one based on
            # the tail end of the binary representation of n. Essentially we
            # have two cases where it's better to add one:
            #
            # 1. The binary representation ends with ....111
            # 2. The binary representation ends with ...1011
            if n & 0b111 == 0b111 or n & 0b1111 == 0b1011:
                n += 1
            else:
                n -= 1

    return ops
