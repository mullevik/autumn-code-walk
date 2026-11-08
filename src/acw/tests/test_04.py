from acw.day_04 import (
    parse_any,
    parse_bool,
    parse_dict,
    parse_int,
    parse_list,
    parse_string,
    solve,
)


def test_solve() -> None:
    assert (
        solve(
            "xcdXCjQKMDAwMDAwMDA1MQowMDAwMDAwMDU0CjAwMDAwMDAxNDQKMDAwMDAwMDE4MQoKMAoKewogICAgImtpbmQiID0+ICJyb29cdCIKICAgICJzaXplIiA9PiAxMTEKICAgICJjb250ZW50IiA9PiBmYWxzZQogICAgImVuY29kaW5nIiA9PiBuaWwKfQoKW3RydWU7IGZhbHNlOyB0cnVlOyB0cnVlOyB0cnVlOyAtMV0KCiJhY3ciCg=="
        )
        == "732"
    )


def test_parse_string() -> None:
    assert parse_string(b'"asd"') == ("asd", b"")
    assert parse_string(b'   "asd"  ') == ("asd", b"  ")
    assert parse_string(b'   "asd\\"f" \n') == ('asd"f', b" \n")
    assert parse_string(b'"roo\\t"') == ("root", b"")


def test_parse_int() -> None:
    assert parse_int(b"1") == (1, b"")
    assert parse_int(b"   1  ") == (1, b"  ")
    assert parse_int(b"   -30  ") == (-30, b"  ")


def test_parse_bool() -> None:
    assert parse_bool(b"true") == (True, b"")
    assert parse_bool(b"   false  ") == (False, b"  ")
    assert parse_bool(b"   false;") == (False, b";")
    assert parse_bool(b" \n true  ") == (True, b"  ")
    assert parse_bool(b"false; true; true; true; -1]\n\n") == (
        False,
        b"; true; true; true; -1]\n\n",
    )


def test_parse_list() -> None:
    assert parse_list(b"[1;2;3]") == ([1, 2, 3], b"")
    assert parse_list(b"  [1; 2;  -3  ] ") == ([1, 2, -3], b" ")
    assert parse_list(b'[ "some"; ["rec";  3]; false  ]') == (
        ["some", ["rec", 3], False],
        b"",
    )
    assert parse_list(b"[true; false; true; true; true; -1]\n\n") == (
        [True, False, True, True, True, -1],
        b"\n\n",
    )
    assert parse_list(b"[]") == ([], b"")


def test_parse_dict() -> None:
    assert parse_dict(b'{"foo" => "bar"}') == ({"foo": "bar"}, b"")
    assert parse_dict(b'    {   "foo"  =>    "bar"   } ') == ({"foo": "bar"}, b" ")
    assert parse_dict(b'    {   "foo"  =>  33   }  ') == ({"foo": 33}, b"  ")
    assert parse_dict(b'    {   "foo"  =>  33 "bar" => true   }  ') == (
        {"foo": 33, "bar": True},
        b"  ",
    )
    assert parse_dict(b"{}") == ({}, b"")


def test_parse_complex() -> None:
    assert parse_any(
        b'{"foo" => 33 "bar" => [1;-3;"true";false] "baz" => {"foobar" => nil}} '
    ) == (
        {"foo": 33, "bar": [1, -3, "true", False], "baz": {"foobar": None}},
        b" ",
    )
