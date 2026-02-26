
# Math functions and random module

import math
import random

numbers = [5, 12, -3, 7]

print("Min:", min(numbers))
print("Max:", max(numbers))
print("Absolute value:", abs(-15))
print("Rounded:", round(3.14159, 2))
print("Power:", pow(2, 4))

print("Square root:", math.sqrt(25))
print("Ceil:", math.ceil(4.2))
print("Floor:", math.floor(4.8))
print("Sin 90°:", math.sin(math.radians(90)))
print("Pi:", math.pi)
print("Euler number:", math.e)

print("Random float:", random.random())
print("Random integer (1-10):", random.randint(1, 10))
print("Random choice:", random.choice(numbers))

random.shuffle(numbers)
print("Shuffled list:", numbers)
