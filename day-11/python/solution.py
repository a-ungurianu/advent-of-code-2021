
import itertools
from os import cpu_count


class Signal:

    def __init__(self):
        self.listeners = []

    def bind(self, f):
        self.listeners.append(f)
    
    def trigger(self):
        for f in self.listeners:
            f()


class Cell:
    def __init__(self, power: int, step_signal: Signal, clear_signal: Signal, flashed_signal: Signal):
        self.power = power
        self.flashed = False
        step_signal.bind(lambda: self.bump())
        clear_signal.bind(lambda: self.clear())
        self.adjacent_signal = Signal()
        self.flashed_signal = flashed_signal

    def clear(self):
        if self.power > 9:
            self.power = 0
        self.flashed = False

    def bump(self):
        self.power += 1
        if not self.flashed and self.power > 9:
            self.flashed = True
            self.adjacent_signal.trigger()
            self.flashed_signal.trigger()
    
    def __repr__(self):
        return f"Cell({self.power}, {self.flashed})"

def attach_neighbour_cells(cellA: Cell, cellB: Cell):
    cellA.adjacent_signal.bind(lambda: cellB.bump())


with open("../input") as f:
    board = list(map(lambda l: l.strip(), f.readlines()))

def print_board(board):
    for row in board:
        print("".join(map(lambda c: str(c.power), row)))

step_signal = Signal()
clear_signal = Signal()
flashed_signal = Signal()

board = [[Cell(int(c), step_signal, clear_signal, flashed_signal) for c in  row] for row in  board]


dirs = [(-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1),]

R, C = len(board), len(board[0])

def is_valid(rowIdx, colIdx):
    return 0 <= rowIdx < R and 0 <= colIdx < C

for rIdx in range(R):
    for cIdx in range(C):
        thisCell = board[rIdx][cIdx]
        for dR, dC in dirs:
            oRIDx, oCIdx = rIdx + dR, cIdx + dC
            if is_valid(oRIDx, oCIdx):
                otherCell = board[oRIDx][oCIdx]
                attach_neighbour_cells(thisCell, otherCell)


counter = 0

def flash():
    global counter
    counter += 1

flashed_signal.bind(flash)

# STEP 1
# STEPS = 100

# for _ in range(STEPS):
#     step_signal.trigger()
#     clear_signal.trigger()

# print_board(board)
# print(counter)

# STEP 2

for stepIdx in itertools.count():
    counter = 0
    step_signal.trigger()
    clear_signal.trigger()
    if counter == 100:
        print(stepIdx + 1)
        break
