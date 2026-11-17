from acw.day_05 import SimState, get_adjacent_states, parse_world, shortest_distance_bfs


def test_shortest_distance_bfs() -> None:
    w, p = parse_world("X#.\n.#T\n...")
    assert shortest_distance_bfs((0, 0), (2, 1), p, w) == 5


def test_shortest_distance_bfs_unreachable() -> None:
    w, p = parse_world("X#.\n.#T\n.*.")
    assert shortest_distance_bfs((0, 0), (2, 1), p, w) == -1


def test_get_adjacent_states_to_package() -> None:
    w, p = parse_world("X..\n..#\n..*")

    adj_states = list(get_adjacent_states(SimState((0, 0), p), w))
    assert adj_states == [(SimState((1, 2), p), 3)]


def test_get_adjacent_states_with_package() -> None:
    w, p = parse_world("X*.\n...\n...")

    adj_states = sorted(get_adjacent_states(SimState((0, 0), p), w), key=lambda x: x[1])
    assert adj_states == [
        (SimState((1, 0), (2, 0)), 1),  # push
        (SimState((1, 1), (1, 0)), 2),  # go under
        (SimState((2, 0), (1, 0)), 4),  # go around
    ]
