elf_calories = [0]

with open("input.txt", "r") as input:
    for line in input.readlines():
        if line == "\n":
            elf_calories.append(0)
        else:
            elf_calories[-1] += int(line)

elf_calories.sort(reverse=True)

print(sum(elf_calories[0:3]))
