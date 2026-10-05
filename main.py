import argparse
import importlib
from pathlib import Path


def main():

    p = argparse.ArgumentParser()
    p.add_argument("day", type=str)
    p.add_argument("input", type=Path, default=None)
    _args = p.parse_args()

    m = importlib.import_module(f"acw.{_args.day}")

    x = _args.input.read_text()
    res = m.solve(x)
    print(f"{_args.day} ({_args.input}): {res}")


if __name__ == "__main__":
    main()
