# Examples of enumerate and zip

names = ["Alice", "Bob", "Charlie"]
scores = [85, 90, 78]

# enumerate example
print("Enumerate example:")
for index, name in enumerate(names):
    print(index, name)

# zip example
print("\nZip example:")
for name, score in zip(names, scores):
    print(name, score)

# sorted example
numbers = [5, 2, 9, 1, 7]
print("\nSorted numbers:", sorted(numbers))

# type conversion
num_str = "123"
num = int(num_str)

print("Converted type:", type(num))
print("Float example:", float(5))