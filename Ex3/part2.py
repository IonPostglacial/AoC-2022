def priority(c: str):
    if c.islower():
        return ord(c) - ord("a") + 1
    else:
        return ord(c) - ord("A") + 27


with open("input.txt", "r") as input:
    sum_prios = 0
    rucksacks = input.read().splitlines()
    for group_rucksack in zip(rucksacks[0::3], rucksacks[1::3], rucksacks[2::3]):
        s1, s2, s3 = map(set, group_rucksack)
        badge = (s1 & s2 & s3).pop()
        sum_prios += priority(badge)
    print(sum_prios)
