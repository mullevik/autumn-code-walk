import base64
import enum
from itertools import pairwise
from typing import Any


def solve(inp: str) -> str:

    parse(inp)

    raise NotImplementedError()


class ObjType(enum.Enum):
    STRING = 0
    INT = 1
    BOOL = 2
    DICT = 3
    LIST = 4


def parse(inp: str) -> None:

    raw_bytes = base64.b64decode(inp)
    print(raw_bytes)

    _header, _, rest = chop(raw_bytes, b"\n")

    n, _, rest = chop(rest, b"\n")

    n = int(n.decode())

    offsets = []
    for i in range(n):
        num, _, rest = chop(rest, b"\n")
        offsets.append(int(num.decode()))

    for a, b in pairwise(offsets):
        obj_bytes = raw_bytes[a:b]

        match decide(obj_bytes):
            case ObjType.STRING:
                print(obj_bytes, "string")
            case ObjType.INT:
                print(int(obj_bytes.decode()), "int")
            case ObjType.LIST:
                print(obj_bytes, "list")
            case ObjType.DICT:
                print(obj_bytes, "dict")

        print(raw_bytes[a:b])


def chop(inp: bytes, pattern: bytes) -> tuple[bytes, bytes, bytes]:

    idx = inp.find(pattern)

    return inp[:idx], inp[idx : idx + len(pattern)], inp[idx + len(pattern) :]


def parse_any(inp: bytes) -> tuple[Any, bytes]:

    match decide(inp):
        case ObjType.STRING:
            return parse_string(inp)
        case ObjType.INT:
            return parse_int(inp)
        case ObjType.BOOL:
            return parse_bool(inp)
        case ObjType.LIST:
            return parse_list(inp)
        case ObjType.DICT:
            return parse_dict(inp)


def decide(inp: bytes) -> ObjType:
    for i in range(len(inp)):
        match inp[i : i + 1]:
            case b'"':
                return ObjType.STRING
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
                return ObjType.INT
            case b"t" | b"f":
                return ObjType.BOOL
            case b"[" | b"]":
                return ObjType.LIST
            case b"{" | b"}":
                return ObjType.DICT
    raise ValueError("eof")


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


WS = (b" ", b"\n")


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
    if (start := inp.find(b"true")) != -1:
        return True, inp[start + len(b"true") :]
    elif (start := inp.find(b"false")) != -1:
        return False, inp[start + len(b"false") :]
    else:
        raise ValueError(f"Bool parsing fail for {inp=}")


def parse_list(inp: bytes) -> tuple[list[Any], bytes]:

    start = inp.find(b"[")
    if start == -1:
        raise ValueError("not a list")

    items = []

    rest = inp[start + 1 :]

    while True:
        item, rest = parse_any(rest)
        items.append(item)

        print(f"{items=} {rest=}")
        for i in range(len(rest)):
            curr = rest[i : i + 1]

            if curr in WS:
                ...
            elif curr == b";":
                rest = rest[i + 1 :]
                break
            elif curr == b"]":
                return items, rest[i + 1 :]
            else:
                raise ValueError(f"Unexpected {curr=}")


def parse_dict(inp: bytes) -> tuple[dict[Any], bytes]:
    raise NotImplementedError()
