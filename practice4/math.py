
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


#ex1
# Convert degree to radian
degree = 15
radian = degree * (math.pi / 180)

print("Input degree:", degree)
print("Output radian:", round(radian, 6))


#ex2
# Calculate the area of a trapezoid
height = 5
base1 = 5
base2 = 6

area_trapezoid = (base1 + base2) / 2 * height
print("the area of a trapezoid:", area_trapezoid)


#ex3
# Calculate the area of a regular polygon
n = 4
side = 25

area_polygon = (n * side**2) / (4 * math.tan(math.pi / n))

print("The area of the polygon is:", int(area_polygon))


#ex4
# Calculate the area of a parallelogram
base = 5
height_para = 6

area_parallelogram = base * height_para
print("Expected Output:", float(area_parallelogram))