import collections

with open("input.txt") as input:
    i = 0
    buffer = collections.deque(maxlen=14)
    for _ in range(buffer.maxlen or 0):
        buffer.append("")
    for i, e in enumerate(input.readline()):
        buffer.append(e)
        if i >= len(buffer) and len(set(buffer)) == len(buffer):
            break
    print(i + 1)
