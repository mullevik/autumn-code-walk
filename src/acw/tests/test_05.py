from acw.day_05 import (
    SimState,
    get_adjacent_states,
    parse_world,
    shortest_distance_a_star,
    shortest_distance_bfs,
    solve,
)


def test_solve() -> None:
    assert (
        solve(
            """..X..
...*.
.....
.#..#
....T"""
        )
        == "7"
    )


def test_shortest_distance_a_star_trivial() -> None:
    w, s, p, g = parse_world("X..\n.*.\n..T")

    assert shortest_distance_a_star(SimState(s, p), g, w) == 5


def test_shortest_distance_a_star_involved() -> None:
    w, s, p, g = parse_world(".X#T\n.*..\n..#.\n.....")

    assert shortest_distance_a_star(SimState(s, p), g, w) == 11


def test_shortest_distance_a_star_unreachable() -> None:
    w, s, p, g = parse_world("X..\n*..\n..T")

    assert shortest_distance_a_star(SimState(s, p), g, w) == -1


def test_shortest_distance_bfs() -> None:
    w, s, p, g = parse_world("X#.\n.#T\n...")
    assert shortest_distance_bfs(s, g, p, w) == 5


def test_shortest_distance_bfs_unreachable() -> None:
    w, s, p, g = parse_world("X#.\n.#T\n.*.")
    assert shortest_distance_bfs(s, g, p, w) == -1


def test_get_adjacent_states_to_package() -> None:
    w, s, p, _ = parse_world("X..\n..#\n..*")

    adj_states = list(get_adjacent_states(SimState(s, p), w))
    assert adj_states == [(SimState((1, 2), p), 3)]


def test_get_adjacent_states_with_package() -> None:
    w, s, p, _ = parse_world("X*.\n...\n...")

    adj_states = sorted(get_adjacent_states(SimState(s, p), w), key=lambda x: x[1])
    assert adj_states == [
        (SimState((1, 0), (2, 0)), 1),  # push
        (SimState((1, 1), (1, 0)), 2),  # go under
        (SimState((2, 0), (1, 0)), 4),  # go around
    ]
