
# Working with directories

import os

# create directory
os.mkdir("test_dir")

# create nested directories
os.makedirs("test_dir/sub_dir/example")

print("Directories created")

# list files and folders
print("\nDirectory contents:")
print(os.listdir("."))

# current working directory
print("\nCurrent directory:")
print(os.getcwd())

# change directory
os.chdir("test_dir")
print("\nChanged directory:")
print(os.getcwd())