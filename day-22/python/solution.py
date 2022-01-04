
def parse_range(s: str):
    s = s[2:]
    f, t = s.split("..")

    return (int(f),int(t))

def parse_step(line: str):
    line = line.strip()

    on, rest = line.split(" ")

    ranges = [parse_range(s) for s in rest.split(",")]

    return (True if on == "on" else False, *ranges)


def get_cubes(x_range, y_range, z_range):
    for x in range(x_range[0], x_range[1] + 1):
        for y in range(y_range[0], y_range[1] + 1):
            for z in range(z_range[0], z_range[1] + 1):
                yield (x,y,z)


def limit_range(range):
    return (max(range[0], -50), min(range[1], 50))

with open("../input") as f:
    steps = [parse_step(line) for line in f.readlines()]

on_values = set()

for step in steps:
    on, *ranges = step
    ranges = [limit_range(r) for r in ranges]
    if on:
        on_values.update(get_cubes(*ranges))
    else:
        on_values.difference_update(get_cubes(*ranges))

print(len(on_values))