import json

class Node(object):
    def __init__(self,  depth, value=None, children=None):
        self.depth = depth
        self.value = value
        self.parent = None
        self.next_leaf = None
        self.prev_leaf = None
        self.children = children or []
        for child in self.children:
            child.parent = self

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        prefix = "  " * self.depth
        if self.value is not None:
            return f"{prefix}Node({self.depth}, value={self.value})"
        else:
            children_s = [str(child) + "\n" for child in self.children]
            s = f"{prefix}Node({self.depth}, children=[\n"
            for child in children_s:
                s += str(child)

            s += f"{prefix}])"
            return s

def convert_arr_to_tree(arr, depth = 0):
    if isinstance(arr, list):
        return Node(depth, children=[convert_arr_to_tree(node, depth + 1) for node in arr])
    else:
        return Node(depth, value=arr)

def connect_leaves(root):
    def traverse(node):
        if node.value is None:
            for child in node.children:
                yield from traverse(child)
        else:
            yield node

    flat = list(traverse(root))

    for i in range(0, len(flat) - 1):
        c = flat[i]
        next = flat[i+1]
        
        c.next_leaf = next

    for i in range(1, len(flat)):
        c = flat[i]
        prev = flat[i-1]
        
        c.prev_leaf = prev

    return flat[0]

def find_next_explode(leftmost):
    cur = leftmost

    while cur is not None:
        parent = cur.parent
        if parent and parent.depth >= 4:
            return parent
        cur = cur.next_leaf

    return None
        
def find_next_split(leftmost):
    cur = leftmost

    while cur is not None:
        if cur.value >= 10:
            return cur
        cur = cur.next_leaf

    return None

def find_next_operation(leftmost):
    explode = find_next_explode(leftmost)
    if explode:
        return ("EXPLODE", explode)
    split = find_next_split(leftmost)
    if split:
        return ("SPLIT", split)
    return None

def apply_explode(node):
    left, right = node.children

    if left.prev_leaf:
        left.prev_leaf.value += left.value
    if right.next_leaf:
        right.next_leaf.value += right.value

    node.value = 0
    node.children = []

def apply_split(node):
    v = node.value
    lv = v // 2
    rv = v - lv

    node.value = None
    left, right = Node(node.depth + 1, lv), Node(node.depth + 1, rv)
    left.parent = node
    right.parent = node

    node.children = [left, right] 

def apply_operation(operation, node):

    if operation == "SPLIT":
        apply_split(node)
    else:
        apply_explode(node)

def tree_to_arr(tree):
    if tree.value is None:
        return [tree_to_arr(n) for n in tree.children]
    else:
        return tree.value

def reduce(arr):
    tree = convert_arr_to_tree(arr)

    leftmost = connect_leaves(tree)
    next_op = find_next_operation(leftmost)

    while next_op:
        apply_operation(*next_op)
        leftmost = connect_leaves(tree)
        next_op = find_next_operation(leftmost)

    return tree   

def calculate_magnitude(arr):
    if isinstance(arr, list):
        return 3 * calculate_magnitude(arr[0]) + 2 * calculate_magnitude(arr[1]) 
    else:
        return arr

with open("../input") as f:
    lines = f.readlines()


snailfishes = [json.loads(line) for line in lines]


res = snailfishes[0]

for fish in snailfishes[1:]:
    res = tree_to_arr(reduce([res, fish]))

print(calculate_magnitude(res))

max_mag = 0

for x in snailfishes:
    for y in snailfishes:
        if x != y:
            mag = calculate_magnitude(tree_to_arr(reduce([x,y])))
            max_mag = max(mag, max_mag)

print(max_mag)
