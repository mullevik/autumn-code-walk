from collections import deque
from collections.abc import Iterable
from dataclasses import dataclass
from heapq import heappop, heappush

type Vec2 = tuple[int, int]


def solve(inp: str) -> str:
    w, s, p, g = parse_world(inp)
    return str(shortest_distance_a_star(SimState(s, p), g, w))


@dataclass(frozen=True, order=True)
class SimState:
    person: Vec2
    package: Vec2

    def is_goal(self, goal: Vec2) -> bool:
        return self.package == goal


WALKABLE = ".XT"


def get_adjacent_states(
    curr: SimState, world: dict[Vec2, str]
) -> Iterable[tuple[SimState, int]]:
    adj_package_positions = set(
        get_adjacent_walkable(curr.package, curr.package, world)
    )
    if curr.person in adj_package_positions:
        d = (curr.package[0] - curr.person[0], curr.package[1] - curr.person[1])
        pushed_package = (curr.package[0] + d[0], curr.package[1] + d[1])

        if world.get(pushed_package, "#") in WALKABLE:
            yield SimState(curr.package, pushed_package), 1

    for adj in adj_package_positions:
        if curr.person != adj:
            person_dist_to_adj = shortest_distance_bfs(
                curr.person, adj, curr.package, world
            )
            if person_dist_to_adj > 0:
                yield SimState(adj, curr.package), person_dist_to_adj


def get_adjacent_walkable(
    a: Vec2, package: Vec2, world: dict[Vec2, str]
) -> Iterable[Vec2]:
    for adj in [
        (a[0] + 1, a[1] + 0),
        (a[0] - 1, a[1] + 0),
        (a[0] + 0, a[1] + 1),
        (a[0] + 0, a[1] - 1),
    ]:
        if world.get(adj, "#") in WALKABLE and adj != package:
            yield adj


def shortest_distance_a_star(
    start: SimState, goal: Vec2, world: dict[Vec2, str]
) -> int:
    priority_queue = [(manhattan_dist(start.package, goal), start)]

    g_scores = {start: 0}

    while priority_queue:
        _, curr = heappop(priority_queue)

        if curr.package == goal:
            return g_scores[curr]

        for adj, adj_dist in get_adjacent_states(curr, world):
            adj_g_score = g_scores[curr] + adj_dist

            if adj_g_score < g_scores.get(adj, float("inf")):
                g_scores[adj] = adj_g_score
                f_score = adj_g_score + manhattan_dist(adj.package, goal)
                heappush(priority_queue, (f_score, adj))

    return -1


def shortest_distance_bfs(
    start: Vec2, goal: Vec2, package: Vec2, world: dict[Vec2, str]
) -> int:
    distances = {start: 0}
    bfs_queue = deque([start])

    while bfs_queue:
        curr = bfs_queue.popleft()

        if curr == goal:
            return distances[curr]

        for adj in get_adjacent_walkable(curr, package, world):
            if adj not in distances:
                distances[adj] = distances[curr] + 1

                bfs_queue.append(adj)

    return -1


def manhattan_dist(a: Vec2, b: Vec2) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def parse_world(inp: str) -> tuple[dict[Vec2, str], Vec2, Vec2, Vec2]:
    world = {}
    package = (-1, -1)
    start = (-1, -1)
    goal = (-1, -1)
    for y, row in enumerate(inp.split("\n")):
        for x, char in enumerate(row):
            if char in "*":
                world[(x, y)] = "."
                package = (x, y)
            elif char in "X":
                world[(x, y)] = "."
                start = (x, y)
            elif char in "T":
                world[(x, y)] = "."
                goal = (x, y)
            else:
                world[(x, y)] = char

    return world, start, package, goal
