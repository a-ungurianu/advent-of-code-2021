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

def get_local_risk(board, rowIdx, colIdx):
    is_min = True
    here = board[rowIdx][colIdx]
    for dR, dC in dirs:
        oR, oC = rowIdx + dR, colIdx + dC
        if is_valid(oR, oC) and not here < board[oR][oC]:
            is_min = False

    if is_min:
        return here + 1
    return 0

total_risk = 0

for rIdx in range(R):
    for cIdx in range(C):
        total_risk += get_local_risk(board, rIdx, cIdx)

print(total_risk)
