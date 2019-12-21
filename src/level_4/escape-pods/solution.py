import collections


def solution(entrances, exits, path):
    """
    Determine how many bunnies figure out how many bunnies can safely make it
    to the escape pods at a time at peak.

    Args:
        entrances: Array of integers denoting where the groups of gathered
            bunnies are.
        exits: Array of integers denoting where the escape pods are located.
        path: Array of an array of integers of the corridor capacities.

    Returns:
        The integer total number of bunnies that can get through at each time
        step.
    """

    num_rooms = len(path)

    graph = [[] for i in xrange(num_rooms)]
    for (i, corridors) in enumerate(path):
        if len(corridors) != num_rooms:
            raise ValueError("Bad input path matrix row.")

        for j in xrange(i + 1, num_rooms):
            edge = None
            capacity = corridors[j]
            if capacity < 0:
                raise ValueError("Negative corridor capacity.")

            if capacity != 0:
                edge = Edge(i, j, capacity)
                graph[i].append(edge)

            reverse_edge = None
            reverse_capacity = path[j][i]
            if reverse_capacity != 0:
                reverse_edge = Edge(j, i, capacity)
                graph[j].append(reverse_edge)

            # link reverse edges
            if edge is not None and reverse_edge is not None:
                edge.reverse_edge = reverse_edge
                reverse_edge.reverse_edge = edge

    # add super-source
    source = num_rooms
    graph.append([])
    for entrance in entrances:
        if not 0 <= entrance < num_rooms:
            raise ValueError("Bad entrance index.")
        graph[source].append(Edge(source, entrance, float("inf")))

    # add super-sink
    sink = num_rooms + 1
    graph.append([])
    for exit in exits:
        if not 0 <= exit < num_rooms:
            raise ValueError("Bad exit index.")
        graph[exit].append(Edge(exit, sink, float("inf")))

    # finally, find max flow
    return edmons_karp(graph, source, sink)


class Edge:
    def __init__(self, a, b, capacity):
        self.a = a
        self.b = b
        self.capacity = capacity
        self.flow = 0
        self.reverse_edge = None

    def has_capacity(self):
        return self.capacity > self.flow

    def available_flow(self):
        return self.capacity - self.flow

    def add_flow(self, flow):
        self.flow += flow
        if self.reverse_edge is not None:
            self.reverse_edge.flow -= flow


def edmons_karp(graph, source, sink):
    num_vertices = len(graph)

    flow = 0
    while True:
        # BFS to find shortest path with available capacity.
        predecessors = [None] * num_vertices
        to_visit = collections.deque([source])

        while len(to_visit) != 0:
            vertex = to_visit.popleft()
            # Iterate through vertex edges, but avoid edges that have reached
            # their capacity.
            for edge in graph[vertex]:
                if edge.b != source \
                        and predecessors[edge.b] is None \
                        and edge.has_capacity():

                    predecessors[edge.b] = edge
                    to_visit.append(edge.b)

        # Recover the path.
        current = sink
        path = []
        while predecessors[current] is not None:
            edge = predecessors[current]
            path.append(edge)
            current = edge.a

        if len(path) == 0:
            # No path found, we're done.
            return flow
        else:
            # Find the most we can send along our path.
            min_flow = None
            for edge in path:
                available_flow = edge.available_flow()
                if min_flow is None or available_flow < min_flow:
                    min_flow = available_flow

            # Then send it.
            for edge in path:
                edge.add_flow(min_flow)

            flow += min_flow
