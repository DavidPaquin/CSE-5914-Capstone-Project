import os
from string import ascii_lowercase
import subprocess

# install necessary modules from requirements.txt
print("\n1. Install necessary requirements\n")
subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)


# verify that all of the data files exist
print("\n2. Verify all data files exist\n")
file_count = 0
desired_file_count = 605
directory = "data/"
for _, _, files in os.walk(directory):
    for file in files:
        if file.lower().endswith(".json"):
            file_count += 1

if file_count != desired_file_count:
    print(
        f"Improper # of files. Expected {file_count} files, but found {desired_file_count}\n"
        + "Read the data/README.txt for instructions on how to download the necessary data files"
    )
    exit()



print("\n*** Setup complete! ***\n")
