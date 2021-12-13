from typing import Set, Tuple


def foldx(points: Set[Tuple[int,int]], x_fold: int):
    def fold_point(point: Tuple[int, int]):
        x,y = point
        if x < x_fold:
            return point
        else:
            offset = x - x_fold
            newX = x_fold - offset
            return (newX,y)

    return {fold_point(point) for point in points}

def foldy(points: Set[int], y_fold: int):
    def fold_point(point: Tuple[int, int]):
        x,y = point
        if y < y_fold:
            return point
        else:
            offset = y - y_fold
            newY = y_fold - offset
            return (x,newY)

    return {fold_point(point) for point in points}


FOLDS = {
    "x": foldx,
    "y": foldy,
}

FOLD_ALONG = "fold along "

def line_to_point(line):
    ps = line.strip().split(",")
    return (int(ps[0]), int(ps[1]))

def line_to_fold(line):
    rem = line[len(FOLD_ALONG):]
    d, magnitude = rem.split("=")

    return (d, int(magnitude))

with open("../input", "r") as f:
    lines = f.readlines()

pointEnd = lines.index("\n")

points = {line_to_point(line) for line in lines[:pointEnd]}

folds = [line_to_fold(line) for line in lines[pointEnd+1:]]

for fold in folds:
    d, val = fold
    fold_f = FOLDS[d]
    points = fold_f(points, val)
    print(len(points))

def plot_points(points):
    max_x = max(point[0] for point in points)
    max_y = max(point[1] for point in points)

    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if (x,y) in points:
                print("#", end="")
            else:
                print(" ", end="")
        print()

plot_points(points)