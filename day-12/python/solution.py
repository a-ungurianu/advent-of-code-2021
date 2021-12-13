from collections import defaultdict
from typing import Set, Tuple


START_CAVE = "start"
END_CAVE = "end"


def is_large_cave(cave: str):
    return cave.isupper()


def is_small_cave(cave: str):
    return cave.islower()


def line_to_edge(line):
    return tuple(line.strip().split("-"))

class State(object):

    def __init__(self, can_double_visit: bool = False, small_caves_visited = None, double_visited_node = None):
        self.small_caves_visited: Set[str] = small_caves_visited or set()
        self.can_double_visit = can_double_visit
        self.double_visited_node = double_visited_node

    def next(self, node):
        if node == START_CAVE:
            return None

        if is_small_cave(node):
            if node in self.small_caves_visited:
                if self.can_double_visit and self.double_visited_node is None:
                    return State(self.can_double_visit, self.small_caves_visited, node)
                else:
                    return None
            else:
                return State(self.can_double_visit, self.small_caves_visited | {node}, self.double_visited_node)
        else:
            return self

def count_paths(graph, can_double_visit: bool = False):
    def _count_paths(node: str, state: State):
        if node == END_CAVE:
            return 1
        neighbours = graph[node]

        next_states = [(neighbour, state.next(neighbour)) for neighbour in neighbours]

        return sum(_count_paths(neighbour, next_state) for neighbour, next_state in next_states if next_state is not None)

    return _count_paths(START_CAVE, State(can_double_visit))

with open("../input", "r") as f:
    lines = f.readlines()

edges = [line_to_edge(line) for line in lines]

graph = defaultdict(set)

for edge in edges:
    a, b = edge
    graph[a].add(b)
    graph[b].add(a)

print(count_paths(graph))
print(count_paths(graph, True))