
# Examples of map, filter and reduce

from functools import reduce

numbers = [1, 2, 3, 4, 5]

# map() example (square numbers)
squared = list(map(lambda x: x**2, numbers))
print("Squared numbers:", squared)

# filter() example (even numbers)
even = list(filter(lambda x: x % 2 == 0, numbers))
print("Even numbers:", even)

# reduce() example (sum of numbers)
total = reduce(lambda a, b: a + b, numbers)
print("Sum using reduce:", total)

# built-in functions
print("Length:", len(numbers))
print("Max:", max(numbers))
print("Min:", min(numbers))
print("Sum:", sum(numbers))