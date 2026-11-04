from acw.day_04 import (
    parse_any,
    parse_bool,
    parse_dict,
    parse_int,
    parse_list,
    parse_string,
)


def test_parse_string() -> None:
    assert parse_string(b'"asd"') == ("asd", b"")
    assert parse_string(b'   "asd"  ') == ("asd", b"  ")
    assert parse_string(b'   "asd\\"f" \n') == ('asd"f', b" \n")


def test_parse_int() -> None:
    assert parse_int(b"1") == (1, b"")
    assert parse_int(b"   1  ") == (1, b"  ")
    assert parse_int(b"   -30  ") == (-30, b"  ")


def test_parse_bool() -> None:
    assert parse_bool(b"true") == (True, b"")
    assert parse_bool(b"   false  ") == (False, b"  ")
    assert parse_bool(b" \n true  ") == (True, b"  ")


def test_parse_list() -> None:
    assert parse_list(b"[1;2;3]") == ([1, 2, 3], b"")
    assert parse_list(b"  [1; 2;  -3  ] ") == ([1, 2, -3], b" ")
    assert parse_list(b'[ "some"; ["rec";  3]; false  ]') == (
        ["some", ["rec", 3], False],
        b"",
    )


def test_parse_dict() -> None:
    assert parse_dict(b'{"foo" => "bar"}') == ({"foo": "bar"}, b"")
    assert parse_dict(b'    {   "foo"  =>    "bar"   } ') == ({"foo": "bar"}, b" ")
    assert parse_dict(b'    {   "foo"  =>  33   }  ') == ({"foo": 33}, b"  ")
    assert parse_dict(b'    {   "foo"  =>  33 "bar" => true   }  ') == (
        {"foo": 33, "bar": True},
        b"  ",
    )


def test_parse_complex() -> None:
    assert parse_any(
        b'{"foo" => 33 "bar" => [1;-3;"true";false] "baz" => {"foobar" => 42}} '
    ) == (
        {"foo": 33, "bar": [1, -3, "true", False], "baz": {"foobar": 42}},
        b" ",
    )
