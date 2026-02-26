
# Demonstrates iterators and generators

numbers = [1, 2, 3]
iterator = iter(numbers)

print("Using iter() and next():")
print(next(iterator))
print(next(iterator))
print(next(iterator))

#2

mystr = "banana"
myit = iter(mystr)

print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))

#3

mytuple = ("apple", "banana", "cherry")
myit = iter(mytuple)

print(next(myit))
print(next(myit))
print(next(myit))


class CountUp:
    def __init__(self, max_value):
        self.max = max_value
        self.current = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= self.max:
            value = self.current
            self.current += 1
            return value
        else:
            raise StopIteration


print("\nCustom Iterator:")
counter = CountUp(5)
for number in counter:
    print(number)


def square_generator(n):
    for i in range(n):
        yield i * i


print("\nGenerator Function:")
for value in square_generator(5):
    print(value)


print("\nGenerator Expression:")
gen_expr = (x * 2 for x in range(5))
for val in gen_expr:
    print(val)
