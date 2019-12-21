# coding=utf-8
from decimal import Context, ROUND_HALF_EVEN, Decimal, ROUND_FLOOR, setcontext, getcontext


def solution(s):
    """
    Given the string representation of an integer n, returns the sum
        ⌊√2⌋ + ⌊2 √2⌋ + ⌊3 √2⌋ + ... + ⌊n √2⌋
    as a string.

    Args:
        s: The number of terms to sum as a string.

    Returns:
        The sum of ⌊i √2⌋ from i = 1...n as a string.
    """

    # If we start by simply generating the sequence by brute force and searching
    # for it on OEIS, we find that it's what's called a "Beatty Sequence" (see:
    # http://oeis.org/A001951, https://en.wikipedia.org/wiki/Beatty_sequence).
    #
    # Noting that from the wiki page it states that if an irrational number
    # r is greater than 1, we can define its complementary sequence for the
    # number s = r / (r - 1). Together, the two sequences include every positive
    # integer. This is important because it means that we know the sum of their
    # partial sums up to some number n is just the sum of integers up to n, aka
    # n(n + 1) / 2. A bit more formally, we have:
    #
    # Given the Beatty sequence for an irrational number u > 1, the irrational v
    #   v = u / (u - 1)
    # defines a complementary sequence. Because the two sequences include every
    # positive number, we know that the sum of the two sequences up to some
    # limit ⌊n u⌋ is:
    #   Σ⌊i u⌋ + Σ⌊i v⌋ = Σ i
    #                   = ⌊n u⌋(⌊n u⌋ + 1) / 2
    # where the sum on the right goes up to ⌊⌊n u⌋/v⌋. Now, defining the sum as
    #   a(x, n) = Σⁿ ⌊i x⌋
    # the previous equation becomes
    #   a(u, n) + a(v, ⌊⌊n u⌋/v⌋) = a(1, ⌊n u⌋)
    #   a(u, n) + a(v, ⌊⌊n u⌋/v⌋) = ⌊n u⌋(⌊n u⌋ + 1) / 2
    #                     a(u, n) = ⌊n u⌋(⌊n u⌋ + 1) / 2 - a(v, ⌊⌊n u⌋/v⌋)
    # Incidentally, it seems like this is what the problem is alluding to
    # "concentrate not on what you have in front of you, but on what you don't"
    #
    # For us we have:
    #   u = √2
    # and
    #   v = √2 / (√2 - 1)
    #     = 2 + u
    #
    #   a(u, n) = ⌊n u⌋(⌊n u⌋ + 1) / 2 - a(2 + u, ⌊⌊n u⌋/(2 + u)⌋)
    #           = ⌊n u⌋(⌊n u⌋ + 1) / 2 - a(u, ⌊⌊n u⌋/(2 + u)⌋)
    #                                  - ⌊⌊n u⌋/(2 + u)⌋(⌊⌊n u⌋/(2 + u)⌋ + 1)
    #
    # So each recursive iteration we decrease n by a factor of ~0.41, which is
    # good enough to be able to calculate for 10^100.

    # keep the old context around so we can restore it afterwards
    old_context = getcontext()
    try:
        setcontext(Context(
            # we can probably live with less precision, but unless
            # runtime is a huge issue, there's not much reason to optimize
            # our operations or anything like that
            prec=256,
            rounding=ROUND_HALF_EVEN,
            Emin=-999999999,
            Emax=999999999,
            capitals=0,
            flags=[],
            traps=[],
        ))
        u = Decimal(2).sqrt()
        v = Decimal(2) + u

        def sqrt_beatty_sum(n):
            nu = (n * u).to_integral_exact(ROUND_FLOOR)
            nv = (nu / v).to_integral_exact(ROUND_FLOOR)

            if n == 0:
                return Decimal(0)
            elif n == 1:
                return nu
            else:
                return nu * (nu + Decimal(1)) / Decimal(2) \
                       - sqrt_beatty_sum(nv) \
                       - nv * (nv + Decimal(1))

        return str(sqrt_beatty_sum(Decimal(s)))
    finally:
        setcontext(old_context)

