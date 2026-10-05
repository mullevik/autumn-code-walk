import argparse
from pathlib import Path
from urllib.request import urlopen


def main():

    p = argparse.ArgumentParser()
    p.add_argument("day", type=str)
    _args = p.parse_args()

    python_path = Path(f"./acw/{_args.day}.py")
    if not python_path.is_file():
        python_path.write_text("def solve(inp: str) -> str:\n    ...")
    else:
        print(f"Skipping {python_path=} because it exists")

    year = "0"
    day = str(int(_args.day) - 1)

    url = f"https://autumncodewalk.github.io/problem/{year}/{day}/input.txt"
    content = urlopen(url).read().decode()
    input_path = Path(f"inputs/{_args.day}")
    if not input_path.is_file():
        input_path.write_text(content)
    else:
        print(f"Skipping {input_path=} because it exists")


if __name__ == "__main__":
    main()
