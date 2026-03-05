
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
#-----------------------------------

#ex1
# squares of numbers up to N

def square_generator(N):
    for i in range(N + 1):
        yield i * i

print("Squares up to 5:")
for value in square_generator(5):
    print(value)


#ex2
# print even numbers between 0 and n (comma separated)

def even_numbers(n):
    for i in range(n + 1):
        if i % 2 == 0:
            yield i

n = int(input("Enter n for even numbers: "))

for num in even_numbers(n):
    print(num, end=",")


#ex3
#numbers divisible by 3 and 4 between 0 and n

def divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i

print("Numbers divisible by 3 and 4 up to 100:")
for num in divisible_by_3_and_4(100):
    print(num)


#ex4
# Generator squares from a to b

def squares(a, b):
    for i in range(a, b + 1):
        yield i * i

print("Squares from 3 to 7:")
for value in squares(3, 7):
    print(value)


#ex5
# returns numbers from n down to 0

def countdown(n):
    while n >= 0:
        yield n
        n -= 1

print("Countdown from 5:")
for number in countdown(5):
    print(number)