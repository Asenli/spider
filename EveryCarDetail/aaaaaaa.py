def foo():
    for i in range(1,33):
        yield i


print(foo())
list1 = [i for i in foo()]
print(list1)