with open("input.txt") as input:
    i = 0
    a, b, c, d = ("", "", "", "")
    for i, e in enumerate(input.readline()):
        a, b, c, d = b, c, d, e
        if i > 3 and len({a, b, c, d}) == 4:
            break
    print(i + 1)
