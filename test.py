dict = {}
for i in range(3000):
    for j in range(3000):
        dict[f"{i},{j}"] = 10
    
l = [[10] * 3000 for _ in range(3000)]

import timeit

print(timeit.timeit('dict["2342,434"]', number=100, globals=globals()))
print(timeit.timeit('l[2342][434]', number=100, globals=globals()))