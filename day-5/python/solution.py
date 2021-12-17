
from typing import Counter
import math


def parse_point(s):
    return tuple(int(x) for x in s.split(","))

def parse_line(line):
    f, t = line.strip().split(" -> ")

    return parse_point(f), parse_point(t)

def add(a, b):
    return a[0] + b[0], a[1] + b[1]

def is_perpendicular(line):
    f, t = line

    return f[0] == t[0] or f[1] == t[1]

with open("../input") as f:
    lines = f.readlines()

def enumerate_points(line):
    f, t = line
    dx = t[0] - f[0]
    dy = t[1] - f[1]

    sX = int(math.copysign(1, dx)) if dx else 0
    sY = int(math.copysign(1, dy)) if dy else 0

    pos = f

    while pos != t:
        yield pos
        pos = add(pos, (sX, sY))
    
    yield t

def get_intersects(lines):
    points = Counter()

    for line in lines:
        points += Counter(enumerate_points(line))

    for p, c in points.items():
        if c > 1:
            yield p


lines = [parse_line(line) for line in lines]

perpendicular_lines = [line for line in lines if is_perpendicular(line)]


print(len(list(get_intersects(perpendicular_lines))))
print(len(list(get_intersects(lines))))

