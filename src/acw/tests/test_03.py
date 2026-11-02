from acw.day_03 import solve


def test_day03() -> None:

    assert (
        solve("""
a -- b
a -- c
a -- d
e -- a
f -- e
g -- f
""")
        == "4"
    )
    assert (
        solve("""
a -- b
b -- c
c -- d
d -- e
e -- f
""")
        == "5"
    )
    assert (
        solve("""
a -- b
b -- c
b -- d
b -- e
b -- f
f -- g
""")
        == "3"
    )
    assert (
        solve("""
a -- b
b -- c
a -- d
d -- e
a -- f
f -- g
""")
        == "4"
    )
