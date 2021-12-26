from collections import defaultdict
from types import new_class
from typing import TextIO
import numpy as np
from math import pi, cos, sin
import itertools
from functools import lru_cache


def x_rotation(quarter_turns: int):
    rads = quarter_turns * (pi / 2)

    return np.array(
        [
            [1, 0, 0],
            [0, int(cos(rads)), -int(sin(rads))],
            [0, int(sin(rads)), int(cos(rads))],
        ]
    )


def y_rotation(quarter_turns: int):
    rads = quarter_turns * (pi / 2)

    return np.array(
        [
            [int(cos(rads)), 0, int(sin(rads))],
            [0, 1, 0],
            [-int(sin(rads)), 0, int(cos(rads))],
        ]
    )


def z_rotation(quarter_turns: int):
    rads = quarter_turns * (pi / 2)

    return np.array(
        [
            [int(cos(rads)), -int(sin(rads)), 0],
            [int(sin(rads)), int(cos(rads)), 0],
            [0, 0, 1],
        ]
    )


ROTATIONS_X = [x_rotation(turns) for turns in range(4)]
ROTATIONS_Y = [y_rotation(turns) for turns in range(4)]
ROTATIONS_Z = [z_rotation(turns) for turns in range(4)]

ROTATIONS = [
    x @ y @ z for x, y, z in itertools.product(ROTATIONS_X, ROTATIONS_Y, ROTATIONS_Z)
]

UNIQUE_ROTATIONS = []

for rot in ROTATIONS:
    if all((rot != other_rot).any() for other_rot in UNIQUE_ROTATIONS):
        UNIQUE_ROTATIONS.append(rot)


class Scanner(object):
    def __init__(self, id, relative_beacons):
        self.relative_beacons = relative_beacons
        self.id = id
        self._rotated_beacons = None

    def __repr__(self):
        beacon_repr = [
            self.relative_beacons[0],
            f"other {len(self.relative_beacons)-2} beacons",
            self.relative_beacons[-1],
        ]
        return f"Scanner(id={self.id}, relative_beacons={beacon_repr})"

    def get_rotated_beacons(self):
        if self._rotated_beacons is None:
            self._rotated_beacons = [
                    {rotate_pos(beacon, rotate) for beacon in self.relative_beacons}
                for rotate in ROTATIONS
            ]

        return self._rotated_beacons


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def read_scanner(f: TextIO):
    header = f.readline().strip("- \n")

    if not header.startswith("scanner"):
        return None

    scanner_id = header[len("scanner") :]

    beacons = set()

    while (line := f.readline().strip()) != "":
        x, y, z = line.split(",")

        beacons.add((int(x), int(y), int(z)))

    return Scanner(scanner_id, beacons)


def rotate_pos(pos, rotation):
    pos_v = np.array(pos, dtype=np.int_).reshape(3, 1)
    res = rotation @ pos_v

    res = tuple(res.reshape(1, 3)[0])
    return res


def compute_lines(points):
    lines = {}

    for tup in ((a, b) for a, b in itertools.product(points, points) if a != b):
        a, b = tup
        lines[sub(a, b)] = tup

    return lines


def get_transposition_offset(aLines, bLines):
    
    intersect = set(aLines.keys()) & set(bLines.keys())

    aNodes = set(aLines[i][0] for i in intersect) | set(aLines[i][1] for i in intersect)
    bNodes = set(bLines[i][0] for i in intersect) | set(bLines[i][1] for i in intersect)

    if len(aNodes) >= 12 and len(bNodes) >= 12:

        first_intersect = next(iter(intersect))

        offset = sub(bLines[first_intersect][0], aLines[first_intersect][0])

        return offset
    return None


def get_scanner_intersect(a: Scanner, b: Scanner):

    aLines = compute_lines(a.relative_beacons)
    for b_rot in b.get_rotated_beacons():
        bLines = compute_lines(b_rot)
        offset = get_transposition_offset(aLines, bLines)
        if offset:
            return Scanner(
                a.id + " " + b.id,
                a.relative_beacons | {sub(bb, offset) for bb in b_rot},
            ), offset

def manhattan_distance(a,b):
    return sum(abs(ai - bi) for ai, bi in zip(a,b))

with open("../input") as f:

    scanners = []
    while scanner := read_scanner(f):
        scanners.append(scanner)

big_scanner = scanners[0]

offsets_from_big_scan = [(0,0,0)]

for iteration in range(len(scanners)):
    print(f"Iteration {iteration + 1}, {len(scanners)} remaining")
    for i, scanner in enumerate(list(scanners)):
        if res := get_scanner_intersect(big_scanner, scanner):
            new_scanner, offset = res
            big_scanner = new_scanner
            scanners.remove(scanner)
            offsets_from_big_scan.append(offset)
            break
    else:
        print("Couldn't find match")

print(len(big_scanner.relative_beacons))

max_offset = 0
for a in offsets_from_big_scan:
    for b in offsets_from_big_scan:
        max_offset = max(max_offset, manhattan_distance(a, b))

print(max_offset)