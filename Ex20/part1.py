def switch(arr: list[tuple[int, int]], i, number: tuple[int, int]):
    v, _ = number
    new_arr = arr.copy()
    del new_arr[i]
    n = (i + v) % len(new_arr)
    ni = len(new_arr) + n if n < 0 else n
    new_arr.insert(ni, number)
    return new_arr


def score(arr: list[int]):
    l = len(arr)
    zi = arr.index(0)
    return arr[(zi + 1000) % l] + arr[(zi + 2000) % l] + arr[(zi + 3000) % l]


numbers = [
    (int(s), i) for i, s in enumerate(open("input.txt").read().strip().splitlines())
]
decrypted = numbers.copy()

for num in numbers:
    i = decrypted.index(num)
    decrypted = switch(decrypted, i, num)

zero = 0
for original_index, number in enumerate(decrypted):
    if number == 0:
        zero = original_index

print(score([n for n, _ in decrypted]))
