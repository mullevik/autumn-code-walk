# Autumn code walk

My solutions for the famous [Autumn code walk](https://autumncodewalk.github.io/) problems.

## Install

```
uv sync
```

## Use

Execute a daily task:

```
uv run solve 01 inputs/01
```

Prepare a daily task:

- loads input content from `https://autumncodewalk.github.io/` and dumps it to `inputs/`
- creates new template in `acw/`

```
uv run prepare 01
```
