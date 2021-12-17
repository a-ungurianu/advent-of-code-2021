
from typing import Tuple, List

import matplotlib.pyplot as plt

from matplotlib.patches import Rectangle

Vec2 = Tuple[int, int]

def add(p1: Vec2, p2: Vec2):
    return (p1[0] + p2[0], p1[1] + p2[1])

def point_in_rect(point: Vec2, rect: Tuple[Vec2, Vec2]):
    x,y = point
    x_lim, y_lim = rect

    return x_lim[0] <= x <= x_lim[1] and y_lim[0] <= y <= y_lim[1]

def point_to_the_bottom_right_of_rect(point: Vec2, rect: Tuple[Vec2, Vec2]):
    x,y = point
    x_lim, y_lim = rect

    return x_lim[1] < x or y_lim[0] > y

def apply_forces_to_vel(vel: Vec2):
    vx, vy = vel

    if vx > 0:
        vx -= 1
    elif vx < 0:
        vx += 1

    vy -= 1

    return (vx ,vy)

def simulate(vel: Vec2, target: Tuple[Vec2, Vec2]):
    pos = (0,0)
    path = [pos]

    while (not point_to_the_bottom_right_of_rect(pos, target)) and (not (vel[0] == 0 and pos[0] < target[0][0])) :
        pos = add(pos, vel)
        path.append(pos)
        vel = apply_forces_to_vel(vel)

        if point_in_rect(pos, target):
            return True, path

    return False, path

def plot(path: List[Vec2], target: Tuple[Vec2, Vec2]):
    plt.style.use('_mpl-gallery')

    # plot
    fig, ax = plt.subplots()

    ax.plot([p[0] for p in path], [p[1] for p in path], linewidth=2.0)

    ax.add_patch(Rectangle((target[0][0], target[1][0]), target[0][1] - target[0][0], target[1][1] - target[1][0]))
    plt.show()



PREFIX = "target area: "
with open("../input") as f:
    line = f.readline()

line = line[len(PREFIX):]

area_x, area_y = [ tuple(map(int, comp[2:].split(".."))) for comp in line.split(", ")]

# Brute force ftw
max_height = 0
count = 0
for vx in range(1, 3*area_x[1]):
    for vy in range(area_y[0], 2000):
        did_hit, path = simulate((vx, vy), (area_x, area_y))
        if did_hit:
            max_height = max(max_height, max(p[1] for p in path))
            count += 1

print(max_height)
print(count)