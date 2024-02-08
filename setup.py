from generate_keywords import generate_keywords
import os
from string import ascii_lowercase
import subprocess

# install necessary modules from requirements.txt
print("\n1. Install necessary requirements\n")
subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)


# verify that all of the data files exist
print("\n2. Verify all data files exist\n")
for c in list(ascii_lowercase) + ["number", "other"]:
    if not os.path.isfile(f"data/{c}.json"):
        print(
            f"ERROR: missing file 'data/{c}.json'\n",
            "Please read 'data/README.txt' to download the data properly.",
        )
        exit()

# generate and store the keywords to keywords.txt
print("\n3. Generate/verify keywords list file\n")
if not os.path.isfile("keywords.txt"):
    generate_keywords()


print("\n*** Setup complete! ***\n")
