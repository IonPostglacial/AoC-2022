def priority(c: str):
    if c.islower():
        return ord(c) - ord("a") + 1
    else:
        return ord(c) - ord("A") + 27


with open("input.txt", "r") as input:
    sum_prios = 0
    for rucksack in input.readlines():
        middle = len(rucksack) // 2
        com1, com2 = rucksack[0:middle], rucksack[middle : len(rucksack)]
        err = (set(com1) & set(com2)).pop()
        sum_prios += priority(err)
    print(sum_prios)
