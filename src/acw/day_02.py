from collections import Counter


def solve(inp: str) -> str:

    lines = [line for line in inp.split("\n") if line.strip()]

    return str(sum(len(compress_line(line)) * (i + 1) for i, line in enumerate(lines)))


def compress_line(line: str) -> str:

    parts = compress_local(line)

    local_c = "".join(parts)
    global_c = compress_global(parts)

    if len(local_c) < len(global_c):
        return local_c
    return global_c


def compress_local(line: str) -> list[str]:

    curr = None
    cnt = 0
    out = []
    for ch in line:
        if ch != curr:
            if curr is not None:
                out.append(f"{curr}{cnt}")
            curr = ch
            cnt = 1
        else:
            cnt += 1

    out.append(f"{curr}{cnt}")

    return out


def compress_global(parts: list[str]) -> str:
    cnt = Counter(parts)

    scores = sorted(
        [(p, len(p) * _cnt) for p, _cnt in cnt.items()],
        key=lambda x: x[1],
        reverse=True,
    )

    alpha_map = {}

    out = ""
    for i, (p, s) in enumerate(scores):
        if i < 26 and s > len(p):
            alpha_map[p] = chr(ord("a") + i)
            out += p

    out += ";;"

    for p in parts:
        if p in alpha_map:
            out += alpha_map[p]
        else:
            out += p

    return out
