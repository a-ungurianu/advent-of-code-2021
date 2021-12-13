from functools import reduce


with open("../input") as f:
    board = [ [ int(c) for c in line.strip()] for line in f.readlines()]

def print_board(board):
    for row in board:
        print("".join(map(lambda c: str(c), row)))


dirs = [          (-1, 0), 
        ( 0, -1),          ( 0, 1),
                  ( 1, 0),         ]

R, C = len(board), len(board[0])

def is_valid(rowIdx, colIdx):
    return 0 <= rowIdx < R and 0 <= colIdx < C

def get_neighbours(pos):
    rowIdx, colIdx = pos
    for dR, dC in dirs:
        oR, oC = rowIdx + dR, colIdx + dC
        if is_valid(oR, oC):
            yield (oR, oC)


def get_local_risk(board, pos):
    is_min = True
    rowIdx, colIdx = pos
    here = board[rowIdx][colIdx]
    for oR, oC in get_neighbours(pos):
        if not here < board[oR][oC]:
            is_min = False

    if is_min:
        return here + 1
    return 0

total_risk = 0

for rIdx in range(R):
    for cIdx in range(C):
        total_risk += get_local_risk(board, (rIdx, cIdx))

print(total_risk)

def find_basins(board):
    visited = set()

    def fill_basin(pos):
        basin_visited = set()
        q = [pos]
        while q:
            cPos = q.pop(0)
            basin_visited.add(cPos)
            for nPos in get_neighbours(cPos):
                if nPos not in basin_visited and board[nPos[0]][nPos[1]] != 9:
                    q.append(nPos)
        
        visited.update(basin_visited)
        return len(basin_visited)

    for rowIdx in range(R):
        for colIdx in range(C):
            pos = (rowIdx, colIdx)

            if pos not in visited and board[rowIdx][colIdx] != 9:
                yield fill_basin(pos)


print(reduce(lambda acc, x: acc * x, sorted(list(find_basins(board)))[-3:]))