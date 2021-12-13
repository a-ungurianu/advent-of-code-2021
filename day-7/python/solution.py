import math

def linear(val):
    return val

def quad(val):
    return val * (val + 1) // 2


def find_mid_point(values, cost_f):
    l, r = min(values), max(values)

    def total_distance(val):
        return sum(cost_f(abs(val - v)) for v in values)

    while l < r:
        mid = (l + r) // 2

        if total_distance(mid - 1) > total_distance(mid) < total_distance(mid + 1):
            return total_distance(mid)
        elif total_distance(mid - 1) > total_distance(mid):
            l = mid
        else:
            r = mid




with open("../input") as f:
    line = f.readline()

values = [int(val) for val in line.strip().split(",")]


print(find_mid_point(values, linear))
print(find_mid_point(values, quad))