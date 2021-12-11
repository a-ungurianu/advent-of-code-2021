
CLOSE_MAP = {
    "{": "}",
    "(": ")",
    "[": "]",
    "<": ">",
}

ERROR_SCORE = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137 
}

REMAINING_SCORE = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4 
}

def get_illegal_bracket(s):
    stack = []

    for c in s:
        if c in CLOSE_MAP:
            stack.append(c)
        else:
            o = stack.pop()
            if c != CLOSE_MAP[o]:
                return (None, c)
    
    remaining = ""
    for c in reversed(stack):
        remaining += CLOSE_MAP[c]

    return (remaining, None)


with open("../input", "r") as f:
    lines = list(map(lambda l: l.strip(), f.readlines()))


def score(remaining):
    res = 0
    for c in remaining:
        res = res * 5 + REMAINING_SCORE[c]

    return res

print(sum(map( lambda v: ERROR_SCORE[v[1]], filter(lambda v:v[1], map(get_illegal_bracket, lines)))))

sorted_res = sorted(map( lambda v: score(v[0]), filter(lambda v:v[0], map(get_illegal_bracket, lines))))

print(sorted_res[len(sorted_res) // 2])

