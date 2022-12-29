current_elf_calories = 0
max_calories = 0

with open("input.txt", "r") as input:
    for line in input.readlines():
        if line == "\n":
            max_calories = max(max_calories, current_elf_calories)
            current_elf_calories = 0
        else:
            current_elf_calories += int(line)
    max_calories = max(max_calories, current_elf_calories)

print(max_calories)
