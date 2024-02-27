from generate_keywords import generate_keywords
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
directory = 'data/'
for _, _, files in os.walk(directory):
    for file in files:
        if file.lower().endswith(".json"):
            file_count += 1

if file_count != desired_file_count:
    print(f"Improper # of files. You had {file_count} files, there should be {desired_file_count} files.")
    exit()


# generate and store the keywords to keywords.txt
print("\n3. Generate/verify keywords list file\n")
if not os.path.isfile("keywords.txt"):
    generate_keywords()


print("\n*** Setup complete! ***\n")
