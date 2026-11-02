


from acw.day_03 import solve


def test_day03() -> None:

    inp_a = """
a -- b
a -- c
a -- d
e -- a
f -- e
g -- f
"""
    assert solve(inp_a) == "4"
