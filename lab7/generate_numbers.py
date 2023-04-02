# This program generates a list of numbers and writes them to a file.
import random

##### Generate list of numbers #####
n = 1000 # Max is 2000 due to memory constraints with quicksort
L = [random.randint(0, n) for _ in range(n)] # noqa: S311

##### Create file to write to #####
with open("./numbers.txt", "w") as f:
    ##### Write numbers to file #####
    for item in L:
        f.write(str(item))
        f.write(" ")
