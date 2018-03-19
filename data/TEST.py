from itertools import filterfalse

list1 = iter([('a', 'b', 3), ('c', 'd', 5), ('a', 'd', 5), ('g', 'd', 5), ('c', 'd', 5)])
c = next(list1)
print(c)
while True:
    d = next(list1, None)
    print(d)
    if d is None:
        break
    if d[0] == 'c':
        list1 = filterfalse(lambda x: 'c' in x, list1)
