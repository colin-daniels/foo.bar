from fractions import Fraction, gcd
from itertools import chain


def solution(m):
    """
    Predict end states of given ore samples from a matrix of their observed
    transition counts.

    Warnings:
        The specifications mention the order of the resulting list should
        correspond to the terminal states, but it's not specified what order
        those states themselves should be listed in, so it's assumed to follow
        the examples and go in order of topmost row to bottommost row.
        Additionally, since Commander Lambda loves efficiency, essentially no
        input checking is done beyond what python checks on its own.

    Args:
        m: Square matrix of positive integer transition counts. It's required
           that no matter which state the ore is in, there is a path from that
           state to a terminal state. There also must be at least one terminal
           state and the first row cannot be all zeros.

    Returns:
        A list of ints for each terminal state giving the exact probabilities
        of each terminal state, represented as the numerator for each state,
        then the denominator for all of them at the end and in simplest form.
    """

    # Note: for more detail regarding the theoretical basis of the following,
    # see https://en.wikipedia.org/wiki/Absorbing_Markov_chain. Also note that
    # this is based off of the input assumptions that
    #   1. It is guaranteed that no matter which state the ore is in,
    #      there is a path from that state to a terminal (absorbing) state.
    #   2. There is at least one absorbing state.
    #
    # For an absorbing Markov chain with t transient states and r absorbing
    # states, the transition matrix P has the canonical form
    #   P = (Q  R)
    #       (0  I)
    # where Q is a t-by-t matrix, R is a nonzero t-by-r matrix, 0 is a r-by-t
    # matrix, I is the identity matrix.
    #
    # It can be proven that the absorbing probabilities B are the solution to
    # the matrix equation
    #   (I - Q) B = R
    # where the element B(i,j) is the probability of being absorbed in the
    # absorbing state j when starting from transient state i.
    #
    # So here our goal is to just use Gaussian elimination to determine the
    # absorbing probabilities. As such, our first step is to build the augmented
    # matrix [(I - Q) | R] using the Fraction class.

    # Note that in building the matrix, we reorder (and possibly remove) states,
    # so we keep a mapping (but the initial state is always the first row).
    augmented, absorbing_state_map = build_augmented_matrix(m)

    # Since we only care about the absorbing probabilities from starting in the
    # first state, we only need the first row to be totally reduced, so instead
    # of converting to upper triangular form like normal, we just do lower
    # triangular form instead.
    transform_into_lower_triangular(augmented)

    # now just get the probabilities, remembering to normalize by the pivot
    t = len(augmented)
    pivot = augmented[0][0]

    probabilities = []
    for mapped_id in absorbing_state_map:
        if mapped_id is not None:
            probabilities.append(augmented[0][t + mapped_id] / pivot)
        else:
            probabilities.append(Fraction(0))

    # finally, find the least common denominator for the fractions and convert
    # into the required output form
    lcd = least_common_denominator(probabilities)
    return [p.numerator * (lcd / p.denominator) for p in probabilities] + [lcd]


def least_common_denominator(fractions):
    """Get least common denominator for a list of fractions."""
    lcd = 1
    for f in fractions:
        lcd = (lcd * f.denominator) / gcd(lcd, f.denominator)

    return lcd


def reachable_states(m):
    """
    Get list of indices of states reachable from s_0 via DFS, note that
    0 is always the first element in the resulting list.
    """
    visited = [False] * len(m)
    visited[0] = True
    to_visit = [0]
    reachable = []

    while len(to_visit) != 0:
        state = to_visit.pop()
        reachable.append(state)

        for (i, count) in enumerate(m[state]):
            if count != 0 and not visited[i]:
                visited[i] = True
                to_visit.append(i)

    return reachable


def inverse_permutation(permutation, num_ids):
    """Invert a permutation (may not map to all ids)."""
    inverse = [None] * num_ids
    for (i, mapped) in enumerate(permutation):
        inverse[mapped] = i

    return inverse


def build_augmented_matrix(m):
    """
    Build the augmented matrix [(I - Q) | R] of Fractions for a matrix of ore
    transition counts. Potentially removes absorbing states that aren't
    reachable, so also returns a mapping to used absorbing states. May re-order
    as well, but never moves the first row.

    Args:
        m: Matrix of ore transition counts.

    Returns:
        augmented_matrix, absorbing_state_map:
            The augmented matrix [(I - Q) | R] of Fractions and a mapping from
            original absorbing states to reachable ones.
    """

    # get total number of transitions from each state
    totals = [sum(row) for row in m]

    # get states reachable from the initial one
    states = reachable_states(m)

    # partition into absorbing (terminal) and transient (non-terminal) states
    transient_states = []
    absorbing_states = []
    for s in states:
        transition_count = totals[s]
        if transition_count != 0:
            transient_states.append(s)
        else:
            absorbing_states.append(s)

    # build the t-by-(t + r) augmented matrix [(I - Q) | R]
    augmented = [
        list(chain(
            (Fraction(-m[i][j], totals[i]) for j in transient_states),  # -Q
            (Fraction(+m[i][j], totals[i]) for j in absorbing_states),  # R
        )) for i in transient_states
    ]

    # Don't forget to add the 1's from the identity matrix in
    for i in xrange(len(transient_states)):
        augmented[i][i] += Fraction(1)

    # Finally, make the mapping between original and actual terminating states
    # Note: this could be simpler, it was added after the fact.
    inverse_mapping = inverse_permutation(absorbing_states, len(m))
    absorbing_state_map = [
        mapped for (t, mapped) in zip(totals, inverse_mapping) if t == 0]

    return augmented, absorbing_state_map


def transform_into_lower_triangular(matrix):
    """
    Uses Gaussian elimination to convert to *lower* triangular form,
    modifies in-place.
    """
    n = len(matrix)
    for i in xrange(n - 1, -1, -1):
        row_a = matrix[i]
        # we know the values at i are always non-zero because these are
        # transient states (also in our case we can't transition to ourselves)
        pivot = row_a[i]

        for j in xrange(i - 1, -1, -1):
            row_b = matrix[j]
            ratio = row_b[i] / pivot
            if ratio == 0:
                continue

            # zero out the entry at row_b[i] by adding row_a
            matrix[j] = [b - ratio * a for (a, b) in zip(row_a, row_b)]
