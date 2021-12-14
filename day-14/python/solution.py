from collections import Counter

from functools import lru_cache

def extract_result(counter: Counter):
    first_c = next(iter(counter.keys()))
    minc, maxc = first_c, first_c

    for k, v in c.items():
        if c[minc] > v:
            minc = k
        
        if c[maxc] < v:
            maxc = k
    return c[maxc] - c[minc]

def apply_ruleset_optimized(polymer, rule_set, depth):
    
    @lru_cache(maxsize=None)
    def _expand_pair(pair, depth):
        if depth == 0:
            return Counter(pair[0])
        else:
            middle = rule_set[pair]
            if middle:
                return _expand_pair(pair[0] + middle, depth - 1) + _expand_pair(middle + pair[1], depth - 1)
            else:
                return Counter(pair[0])

    res = Counter()
    res[polymer[-1]] += 1

    for i in range(len(polymer) - 1):
        res += _expand_pair(polymer[i:i+2], depth)

    return res

def parse_rule(line):
    line = line.strip()

    vals = line.split(" -> ")

    return vals[0], vals[1]

with open("../input") as f:
    lines = f.readlines()

initial_state = lines[0].strip()

rules = [parse_rule(line) for line in lines[1:] if line.strip()]

rule_set = {k:v for k,v in rules}


c = apply_ruleset_optimized(initial_state, rule_set, 10)
print("10 steps:", extract_result(c))

c = apply_ruleset_optimized(initial_state, rule_set, 40)
print("40 steps:", extract_result(c))
