
# Move and copy files between directories

import shutil
import os

# create directories if they do not exist
os.makedirs("source", exist_ok=True)
os.makedirs("destination", exist_ok=True)

# create a sample file
with open("source/example.txt", "w") as f:
    f.write("This file will be moved")

# move file
shutil.move("source/example.txt", "destination/example.txt")
print("File moved successfully")

# copy file
shutil.copy("destination/example.txt", "source/example_copy.txt")
print("File copied successfully")