from collections import Counter

with open("../input") as f:
    line = f.readline().strip()

data = [int(n) for n in line.split(",")]

state = Counter(data)


def simulate_steps(state, steps):
    for _ in range(steps):
        new_state = Counter()
        for k, v in state.items():
            if k == 0:
                new_state[8] += v
                new_state[6] += v
            else:
                new_state[k-1] += v
        state = new_state
    return state

def count_fish(state):
    return sum(state.values())

print(count_fish(simulate_steps(state, 80)))
print(count_fish(simulate_steps(state, 256)))