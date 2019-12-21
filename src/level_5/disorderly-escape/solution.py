# coding=utf-8
from collections import defaultdict
from fractions import Fraction, gcd
from operator import mul
from math import factorial


def product(iterable, init=1):
    return reduce(mul, iterable, init)


class Poly:
    """
    Very simple class representing a polynomial in terms of its exponents and
    coefficients.
    """

    def __init__(self, coeffs=None):
        if coeffs is None:
            coeffs = []

        # map of exponent -> coefficient
        self.coeff = defaultdict(lambda: 0)
        for (coeff, exponent) in coeffs:
            if coeff != 0:
                self.coeff[exponent] = coeff

    def max_exponent(self):
        return max((e for (e, c) in [(0, 1)] + self.coeff.items() if c != 0))

    def __add__(self, other):
        ret = Poly()
        ret.coeff = self.coeff.copy()
        for exponent, coeff in other.coeff.items():
            ret.coeff[exponent] += coeff

        return ret

    def __hash__(self):
        return hash(tuple(self.coeff.items()))

    def __str__(self):
        return " + ".join([
            "{}x^{}".format(c, e)
            for (e, c) in self.coeff.items()
        ])


def solution(w, h, s):
    """
    Calculate the number of unique, non-equivalent configurations that can be
    found on a star grid w blocks wide and h blocks tall where each celestial
    body has s possible states.

    References:
        http://oeis.org/A028657 for the NxK binary case
        http://oeis.org/A246106 for the NxN general case
        https://en.wikipedia.org/wiki/P%C3%B3lya_enumeration_theorem

    Args:
        w: Width of the star grid, between 1 and 12 inclusive.
        h: Height of the star grid, between 1 and 12 inclusive.
        s: Number of possible states for each celestial body, between 2 and 20
           inclusive.

    Returns:
        The number of unique, non-equivalent configurations that can be found
        on a star grid as a string.
    """

    # The initial approach for this problem was to simply write a function
    # to brute force this problem, and then look up the sequences on OEIS
    # (in particular, see http://oeis.org/A028657 and http://oeis.org/A246106).
    #
    # I won't pretend to completely understand the mathematics behind this,
    # but the problem in math terms is to determine the number of orbits
    # of a group action (our action is permutations of rows/columns) on a set.
    # For the general idea, see https://en.wikipedia.org/wiki/Burnside%27s_lemma
    # and https://en.wikipedia.org/wiki/P%C3%B3lya_enumeration_theorem.
    #
    min_grid = 1
    max_grid = 12
    min_states = 2
    max_states = 20

    if not min_grid <= w <= max_grid:
        raise ValueError("Invalid star grid width {}, not between {} and {}"
                         .format(w, min_grid, max_grid))
    if not min_grid <= h <= max_grid:
        raise ValueError("Invalid star grid height {}, not between {} and {}"
                         .format(h, min_grid, max_grid))
    if not min_states <= s <= max_states:
        raise ValueError("Invalid number of states {}, not between {} and {}"
                         .format(s, min_states, max_states))

    # ensure width < height (matters for our calculation method)
    if w > h:
        w, h = h, w

    # actually do the calculation
    return str(g(w, h - w, s))


def g(n, k, num_states):
    """
    Mostly adapted from Mathematica code by Jean-François Alcover (after
    Alois P. Heinz) at http://oeis.org/A028657.
    """
    def exponent(poly_s, poly_t):
        return sum((
            gcd(i, j) * coeff_s * coeff_t
            for (i, coeff_s) in poly_s.coeff.items()
            for (j, coeff_t) in poly_t.coeff.items()
        ))

    def divisor(poly):
        return product((
            factorial(poly.coeff[i]) * (i ** poly.coeff[i])
            for i in xrange(1, poly.max_exponent() + 1)
        ))

    return sum((
        Fraction(
            numerator=num_states ** exponent(poly_s, poly_t),
            denominator=divisor(poly_s) * divisor(poly_t),
        )
        for poly_s in b(n, n)
        for poly_t in b(n + k, n + k)
    ))


def b(n, i):
    """
    Returns:
        A set of Poly objects (polynomials).
    """
    if n == 0:
        return {Poly()}
    elif i < 1:
        return {}

    polynomials = set()
    for j in xrange(0, n // i + 1):
        for poly in b(n - i * j, i - 1):
            # poly + j*x^i
            polynomials.add(poly + Poly([(j, i)]))

    return polynomials
