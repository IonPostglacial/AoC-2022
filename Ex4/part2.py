import re

r = re.compile(r"\d+")

with open("input.txt", "r") as input:
    nb_overlap = 0
    for elf_pair_txt in input.readlines():
        a, b, y, z = map(int, r.findall(elf_pair_txt))
        r1 = set(range(a, b + 1))
        r2 = set(range(y, z + 1))
        if len(r1 & r2) > 0:
            nb_overlap += 1
    print(nb_overlap)
