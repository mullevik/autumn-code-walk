import enum
from collections import defaultdict, deque


def solve(inp: str) -> str:

    lines = [line for line in inp.split("\n") if line.strip()]

    g = defaultdict(list)
    for line in lines:
        tmp = line.split(" -- ")
        g[tmp[0]].append(tmp[1])
        g[tmp[1]].append(tmp[0])

    tot = 0
    for i, (v, _) in enumerate(g.items()):
        x = find_longest_path(v, g)
        print(f"{i}/{len(g)} {x=}")
        if x > tot:
            tot = x

    return str(tot)


def find_longest_path(v: str, g: dict[str, list[str]]) -> int:

    bfs_queue = deque([v])

    dist = {v: 0}

    while bfs_queue:
        curr = bfs_queue.popleft()

        for adj in g[curr]:
            if adj not in dist:
                dist[adj] = dist[curr] + 1
                bfs_queue.append(adj)

    return max(dist.values())
