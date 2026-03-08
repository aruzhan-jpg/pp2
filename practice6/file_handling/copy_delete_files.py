
# Copying and deleting files

import shutil
import os

# copy file
shutil.copy("sample.txt", "sample_backup.txt")
print("File copied successfully")

# check if file exists before deleting
if os.path.exists("sample_backup.txt"):
    os.remove("sample_backup.txt")
    print("Backup file deleted")
else:
    print("File does not exist")