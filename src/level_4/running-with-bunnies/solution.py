import itertools


def solution(times, times_limit):
    """
    Calculate the most bunnies you can save, as a list corresponding to their
    prisoner IDs, within a time limit and given a matrix of travel times to
    each bunny.

    Warnings:
        Note that it's unspecified what to do if we can't even escape with
        no bunnies, so here we will just raise a ValueError.

    Args:
        times: The time it takes to move from your starting point to all of the
            bunnies as list of lists (square matrix) of integers. Size should be
            at least 2-by-2.
        times_limit (int): Positive integer that is at most 999. It should
            always be possible to reach the exit with no bunnies before this.

    Returns:
        A sorted list indicating the prisoner IDs of the most bunnies you can
        pick up. If there are multiple sets of bunnies of the same size, the
        set of bunnies with the lowest prisoner IDs are returned.

    """
    if type(times) != list or type(times_limit) != int:
        raise TypeError("Invalid input argument types.")

    if not 0 <= times_limit <= 999:
        raise ValueError("Invalid times_limit ({}), not in range [0, 999]."
                         .format(times_limit))

    num_locations = len(times)
    num_bunnies = num_locations - 2
    bulkhead_loc = num_locations - 1

    if num_bunnies < 0:
        raise ValueError("Not enough rows in input matrix.")
    elif num_bunnies == 0:
        return []

    # While this problem has some similarities with those in reinforcement
    # learning, all transitions are deterministic and we can just treat it as
    # a shortest-path problem for a weighted digraph.

    # The only particularly complicated part here is the enumeration of all
    # possible states (where we are and how many bunnies we have) as a vertex
    # index. Here we use the first `num_bunnies` bits for recording how many
    # bunnies we have, and the rest for the location. This gives us the
    # following number of vertices:
    num_vertices = 2**num_bunnies * num_locations

    # Next we construct a list of edges + weights (time deltas) in order to use
    # Bellman-Ford to find a minimum cost path
    edges_and_weights = []
    for loc in xrange(num_locations):
        loc_times = times[loc]
        if len(loc_times) != num_locations:
            raise ValueError("Invalid input row length in times matrix.")

        # Note: we technically go through some invalid states (e.g. at bunny 1
        # but without bunny 1 marked as saved) but these aren't reachable from
        # the starting point so its OK.
        for bunnies in xrange(2**num_bunnies):
            current_idx = bunnies | (loc << num_bunnies)
            # new location = start
            edges_and_weights.append((current_idx, bunnies, loc_times[0]))

            # new location = bulkhead
            edges_and_weights.append((
                current_idx,
                bunnies | (bulkhead_loc << num_bunnies),
                loc_times[bulkhead_loc]
            ))

            # new location = bunny
            for bunny_loc in xrange(num_bunnies):
                # Since we're moving to (potentially) new bunnies, we need to
                # make sure to mark that we've visited them
                new_bunnies = (bunnies | (1 << bunny_loc))
                new_loc = bunny_loc + 1
                edges_and_weights.append((
                    current_idx,
                    new_bunnies | (new_loc << num_bunnies),
                    loc_times[new_loc]
                ))

    try:
        # Calculate distances (time needed) to each state from the start via
        # Bellman-Ford.
        distances = bellman_ford_distances(edges_and_weights, 0, num_vertices)

        # Check if we can even get to the bulkhead in time.
        if distances[bulkhead_loc << num_bunnies] > times_limit:
            raise ValueError("Cannot reach bulkhead in time.")

        # Check distances to the bulkhead, and pick the largest number of
        # bunnies that we can save.
        bunnies_saved = []
        # Note: we use [1, 0] here so that the earlier bunny ids are favored
        for bunnies in itertools.product([1, 0], repeat=num_bunnies):
            bulkhead_index = bulkhead_loc << num_bunnies
            # Set bits for each bunny we have and make a list of them
            current_bunnies_saved = []
            for (i, b) in enumerate(bunnies):
                if b == 1:
                    current_bunnies_saved.append(i)
                    bulkhead_index |= 1 << i

            time_needed = distances[bulkhead_index]
            if time_needed > times_limit:
                continue

            # Note: bunnies_saved needs to be first in case of tie
            bunnies_saved = max(bunnies_saved, current_bunnies_saved, key=len)

        return bunnies_saved
    except NegativeCycleException:
        # We have a negative cycle, so we should be able to save all the bunnies
        return range(num_bunnies)


class NegativeCycleException(Exception):
    """Raised when the input graph has a negative weight cycle"""
    pass


def bellman_ford_distances(
        edges_and_weights,
        starting_vertex,
        num_vertices,
):
    # Here we don't actually need to do the full Bellman-Ford algorithm (see:
    # https://en.wikipedia.org/wiki/Bellman%E2%80%93Ford_algorithm) since we
    # don't actually care about the path. So instead we just determine
    # distances.
    #
    # Note: We use this instead of something like Dijkstra's algorithm because
    # we have negative edge weights.

    distances = [float("inf")] * num_vertices
    distances[starting_vertex] = 0

    # Note: in our case, we might be able to get away with less iterations than
    # the full |V| - 1 because we do have some knowledge about the input graph.
    # That said, for now we wont bother.
    for _ in xrange(num_vertices - 1):
        for (u, v, w) in edges_and_weights:
            distances[v] = min(distances[u] + w, distances[v])

    # Detect negative cycles
    for (u, v, w) in edges_and_weights:
        if distances[u] + w < distances[v]:
            raise NegativeCycleException()

    return distances
