# iter() and next()
numbers = [1, 2, 3]
iterator = iter(numbers)

print("Iterator example:")
print(next(iterator))
print(next(iterator))

#ex2
mystr = "banana"
myit = iter(mystr)

print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))
print(next(myit))

#ex3
mytuple = ("apple", "banana", "cherry")
myit = iter(mytuple)

print(next(myit))
print(next(myit))
print(next(myit))

# 2. Loop through an iterator
for num in numbers:
    print(num)

#ex2
mytuple = ("apple", "banana", "cherry")

for x in mytuple:
  print(x)

#ex3
mystr = "banana"

for x in mystr:
  print(x)


# 3. Create a custom iterator
class CountUp:
    def __init__(self, max_value):
        self.max = max_value
        self.current = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= self.max:
            num = self.current
            self.current += 1
            return num
        else:
            raise StopIteration

print("\nCustom Iterator:")
counter = CountUp(5)
for number in counter:
    print(number)


# 4. Generator function using yield
def square_generator(n):
    for i in range(n):
        yield i * i

print("\nGenerator function:")
for value in square_generator(5):
    print(value)


# 5. Generator expression
print("\nGenerator expression:")
gen_expr = (x * 2 for x in range(5))
for val in gen_expr:
    print(val)