def solve(inp: str) -> str:
    lines = [line for line in inp.split("\n") if line.strip()]
    haystack = lines[0]
    needles = lines[1:]

    merged = []
    merged_wc = []
    word_count = 0
    for ch in haystack:
        if ch == " ":
            word_count += 1
        else:
            merged.append(ch)
            merged_wc.append(word_count)

    merged_haystack = "".join(merged)

    return str(
        sum(
            [
                idx if (idx := merged_haystack.find(n)) == -1 else merged_wc[idx]
                for n in needles
            ]
        )
    )
