
# Example of reading files in different ways

# read() - reads the whole file
file = open("sample.txt", "r")
content = file.read()
print("Using read():")
print(content)
file.close()

# readline() - reads one line
file = open("sample.txt", "r")
print("\nUsing readline():")
print(file.readline())
file.close()

# readlines() - reads all lines into list
file = open("sample.txt", "r")
lines = file.readlines()
print("\nUsing readlines():")
print(lines)
file.close()

# using context manager
print("\nUsing with statement:")
with open("sample.txt", "r") as file:
    print(file.read())