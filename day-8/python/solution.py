
from collections import defaultdict

DIGITS = {
    0: "abcefg",
    1: "cf",
    2: "acdeg",
    3: "acdfg",
    4: "bcdf",
    5: "abdfg",
    6: "abdefg",
    7: "acf",
    8: "abcdefg",
    9: "abcdfg",
}

REVERSE_DIGITS = {
    v: k for k, v in DIGITS.items()    
}

SEGMENTS = "abcdefg"

def get_blank_wiring():
    return {
        segment: set(SEGMENTS) for segment in SEGMENTS
    }


def find_mapping(samples):
    wiring = get_blank_wiring()
    
    sample_mapping = {
        1: [sample for sample in samples if len(sample) == 2][0],
        4: [sample for sample in samples if len(sample) == 4][0],
        7: [sample for sample in samples if len(sample) == 3][0],
        8: [sample for sample in samples if len(sample) == 7][0], 
    }

    sixes = [sample for sample in samples if len(sample) == 6]

    dd = defaultdict(int)
    
    for s in sixes:
        for c in s:
            dd[c] += 1

    cde = set(key for key, value in dd.items() if value == 2)

    for val, sample in sample_mapping.items():
        segments = DIGITS[val]
        for segment in segments:
            wiring[segment] &= set(sample)

    CF_PASS = set(SEGMENTS) - set("cf")

    for segment in CF_PASS:
        wiring[segment] -= wiring["c"]

    A_PASS = set(SEGMENTS) - set("a")

    for segment in A_PASS:
        wiring[segment] -= wiring["a"]

    BD_PASS = set(SEGMENTS) - set("bd")

    for segment in BD_PASS:
        wiring[segment] -= wiring["b"]

    wiring["c"] &= cde
    wiring["d"] &= cde
    wiring["e"] &= cde

    C_PASS = set(SEGMENTS) - set("c")

    for segment in C_PASS:
        wiring[segment] -= wiring["c"]


    E_PASS = set(SEGMENTS) - set("e")

    for segment in E_PASS:
        wiring[segment] -= wiring["e"]

    D_PASS = set(SEGMENTS) - set("d")

    for segment in D_PASS:
        wiring[segment] -= wiring["d"]


    return {next(iter(val)): key  for key, val in wiring.items()}

def decode(mapping, number):
    res = ""

    for segment in number:
        res += mapping[segment]

    return REVERSE_DIGITS["".join(sorted(res))]


def parse_line(line):
    samples, to_decode = line.split("|")

    return samples.strip().split(" "), to_decode.strip().split(" ")

with open("../input", "r") as f:
    lines = f.readlines()


tasks = [parse_line(line) for line in lines]

count1478 = 0
sum = 0

for samples, to_decode in tasks:
    mapping = find_mapping(samples)

    decoded = [decode(mapping, number) for number in to_decode]
    
    count1478 += len([n for n in decoded if n in {1,4,7,8}])
    
    sum += int("".join(str(s) for s in decoded))

print(count1478)
print(sum)