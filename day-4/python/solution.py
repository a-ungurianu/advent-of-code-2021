import re
import itertools

SPACES = re.compile("\s+")

def has_bingo(board, drawn_numbers):
    marked_numbers = []

    def mark_number(number):
        for rIdx, row in enumerate(board):
            for cIdx, boardNumber in enumerate(row):
                if boardNumber == number:
                    mark = (rIdx, cIdx, boardNumber)
                    marked_numbers.append(mark)
                    return mark 
        return None

    def find_bingo_around(row, col):
        if len(list(filter(lambda p: p[0] == row, marked_numbers))) == 5:
            return True
        
        if len(list(filter(lambda p: p[1] == col, marked_numbers))) == 5:
            return True
        return False

    for idx, number in enumerate(drawn_numbers):
        mark = mark_number(number)
        if mark:
            if find_bingo_around(mark[0], mark[1]):
                return idx
    return None

with open("../input", "r") as f:
    drawn_numbers = f.readline().strip().split(",")

    boards = []

    while f:
        f.readline()
        board = []

        for _ in range(5):
            board.append(SPACES.split(f.readline().strip()))
        if board[0][0] == "":
            break
        boards.append(board)

def get_result(win_state, drawn_numbers):
    winner_board, winner_number_idx = win_state

    winner_number = drawn_numbers[winner_number_idx]

    winning_drawn = drawn_numbers[:winner_number_idx+1]

    return sum(map(int, filter(lambda n: n not in winning_drawn, itertools.chain(*winner_board)))) * int(winner_number)


winner = min(map(lambda board: (board,has_bingo(board, drawn_numbers)), boards), key= lambda x: x[1])
loser  = max(map(lambda board: (board,has_bingo(board, drawn_numbers)), boards), key= lambda x: x[1])



print(get_result(winner, drawn_numbers))
print(get_result(loser, drawn_numbers))