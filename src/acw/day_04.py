import base64
from types import NoneType
from typing import Any


def solve(inp: str) -> str:
    return str(parse(inp))


def fingerprint(obj: object) -> int:

    if isinstance(obj, str):
        return len(obj)
    elif isinstance(obj, int):
        return abs(obj)
    elif isinstance(obj, bool):
        return int(obj)
    elif obj is None:
        return 31
    elif isinstance(obj, dict):
        return sum(fingerprint(k) * fingerprint(v) for k, v in obj.items()) + 3
    elif isinstance(obj, list):
        return sum(fingerprint(i) for i in obj) + 1
    else:
        raise ValueError(f"Unknown object {obj=}")


def parse(inp: str) -> int:

    raw_bytes = base64.b64decode(inp)
    _header, _, rest = chop(raw_bytes, b"\n")

    n, _, rest = chop(rest, b"\n")

    n = int(n.decode())

    starting_offsets = []
    for i in range(n):
        num, _, rest = chop(rest, b"\n")
        starting_offsets.append(int(num.decode()))

    sorted_offsets = sorted([x for x in starting_offsets])
    sorted_offsets.append(len(raw_bytes))

    checksum = 0

    for obj_id, start in enumerate(starting_offsets):
        end_idx = sorted_offsets.index(start)
        end = sorted_offsets[end_idx + 1]
        obj_bytes = raw_bytes[start:end]
        print(f"{start=} {end=} {obj_id=} {obj_bytes=}")
        obj, _ = parse_any(obj_bytes)
        obj_fgp = fingerprint(obj)
        checksum += obj_fgp * obj_id

    return checksum


def chop(inp: bytes, pattern: bytes) -> tuple[bytes, bytes, bytes]:

    idx = inp.find(pattern)

    return inp[:idx], inp[idx : idx + len(pattern)], inp[idx + len(pattern) :]


def parse_any(inp: bytes) -> tuple[Any, bytes]:
    rest = consume(inp, ignore=WS)
    curr = rest[0:1]
    match curr:
        case b'"':
            return parse_string(rest)
        case (
            b"+"
            | b"-"
            | b"0"
            | b"1"
            | b"2"
            | b"3"
            | b"4"
            | b"5"
            | b"6"
            | b"7"
            | b"8"
            | b"9"
        ):
            return parse_int(rest)
        case b"t" | b"f":
            return parse_bool(rest)
        case b"[":
            return parse_list(rest)
        case b"{":
            return parse_dict(rest)
        case b"n":
            return parse_nil(rest)
        case _:
            raise ValueError(f"unexpected {rest[:20]=}")


def parse_int(inp: bytes) -> tuple[int, bytes]:
    sign = ""
    num = ""
    for i in range(len(inp)):
        curr = inp[i : i + 1]

        if curr in b"+-":
            if sign:
                raise ValueError("double sign")
            else:
                sign = curr.decode()
        elif curr in b"0123456789":
            num += curr.decode()
        elif curr in WS:
            if num:
                return int(f"{sign}{num}"), inp[i:]
            else:
                ...
        else:
            if num:
                return int(f"{sign}{num}"), inp[i:]
            else:
                raise ValueError("no digit found")

    if num:
        return int(f"{sign}{num}"), b""
    else:
        raise ValueError("eof")


WS: set[bytes] = {b" ", b"\n"}


def parse_string(inp: bytes) -> tuple[str, bytes]:
    out = ""

    quotes = False
    escape = False

    for i in range(len(inp)):
        curr = inp[i : i + 1]

        if quotes:
            if escape:
                out += curr.decode()
                escape = False
            elif curr == b"\\":
                escape = True
            elif curr == b'"':
                quotes = False
                return out, inp[i + 1 :]
            else:
                out += curr.decode()
        else:
            if curr in WS:
                ...
            elif curr == b'"':
                quotes = True
            else:
                raise ValueError(f"String parsing fail for {curr=}")
    raise ValueError("string eof")


def parse_bool(inp: bytes) -> tuple[bool, bytes]:
    rest = consume(inp, ignore=WS)
    if rest.startswith(b"true"):
        return True, rest[len(b"true") :]
    elif rest.startswith(b"false"):
        return False, rest[len(b"false") :]
    else:
        raise ValueError(f"Bool parsing fail for {inp=}")


def parse_nil(inp: bytes) -> tuple[NoneType, bytes]:
    rest = consume(inp, ignore=WS)
    if rest.startswith(b"nil"):
        return None, rest[3:]
    raise ValueError(f"Nil parsing failed for {inp=}")


def parse_list(inp: bytes) -> tuple[list[Any], bytes]:
    out = []

    rest = consume(inp, ignore=WS)
    if not rest.startswith(b"["):
        raise ValueError("not a list")
    rest = rest[1:]  # eat b"["

    while True:
        rest = consume(rest, ignore=WS)

        if rest.startswith(b"]"):
            return out, rest[1:]
        elif rest.startswith(b";"):
            rest = rest[1:]
        else:
            item, rest = parse_any(rest)
            out.append(item)


def parse_dict(inp: bytes) -> tuple[dict[str, Any], bytes]:

    rest = consume(inp, ignore=WS)
    if not rest.startswith(b"{"):
        raise ValueError(f"not a dict {inp[:20]=}")
    rest = rest[1:]  # eat b"{"
    out = {}

    while True:
        rest = consume(rest, ignore=WS)
        if rest.startswith(b"}"):
            return out, rest[1:]
        else:
            key, rest = parse_string(rest)
            rest = consume(rest, ignore=WS)
            if not rest.startswith(b"=>"):
                raise ValueError(f"expected =>, found {rest[:20]=}")
            rest = rest[2:]
            rest = consume(rest, ignore=WS)
            obj, rest = parse_any(rest)
            out[key] = obj


def consume(inp: bytes, ignore: set[bytes]) -> bytes:
    for i in range(len(inp)):
        curr = inp[i : i + 1]

        if curr not in ignore:
            return inp[i:]

    raise ValueError("eof")
