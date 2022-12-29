from pathlib import Path


def dir_size(dir: dict[str, dict | int]) -> int:
    size = 0
    for name, value in dir.items():
        if name == "..":
            continue
        if isinstance(value, int):
            size += value
        else:
            child_size = dir_size(value)
            size += child_size
    return size


def dir_stats(path: Path, dir: dict[str, dict | int]) -> dict[str, int]:
    stats = {}
    for name, value in dir.items():
        if name == ".." or not isinstance(value, dict):
            continue
        else:
            stats[path / name] = dir_size(value)
            stats |= dir_stats(path / name, value)
    return stats


with open("input.txt") as input:
    root = {}
    current_dir = root

    def cmd_exec(cmd: list[str]):
        global current_dir
        match cmd:
            case ["ls"]:
                pass
            case ["cd", "/"]:
                current_dir = root
            case ["cd", dir]:
                current_dir = current_dir[dir]

    for line in input.read().splitlines():
        prompt, *args = line.split(" ")
        match prompt:
            case "$":
                cmd_exec(args)
            case "dir":
                current_dir[args[0]] = {"..": current_dir}
            case _:
                current_dir[args[0]] = int(prompt)

    total_space = 70_000_000
    stats = dir_stats(Path(), root)
    dir_sizes = stats.values()
    occupied_space = dir_size(root)
    free_space = total_space - occupied_space
    space_to_free = 30_000_000 - free_space
    candidates = list(filter(lambda n: n >= space_to_free, dir_sizes))
    candidates.sort(reverse=True)
    print(candidates.pop())
