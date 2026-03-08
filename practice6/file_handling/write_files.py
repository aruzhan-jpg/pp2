
# Writing and appending data to a file

# create and write file
with open("sample.txt", "w") as file:
    file.write("Hello Python\n")
    file.write("This is file handling practice\n")

print("File created and data written")

# append new lines
with open("sample.txt", "a") as file:
    file.write("Appending a new line\n")
    file.write("Python is easy to learn\n")

print("New lines appended")

# read file to verify
with open("sample.txt", "r") as file:
    print("\nFile content:")
    print(file.read())