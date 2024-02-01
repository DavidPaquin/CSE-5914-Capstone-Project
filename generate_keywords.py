from string import ascii_lowercase
import re
import tqdm


def get_titles(file_name):
    pattern = re.compile(r"^\s*\"title\":\s*\"(.+)\",")
    with open(file_name, "r") as f:
        for line in f:
            if m := pattern.match(line):
                yield m.groups()[0]


def generate_keywords():
    with open("keywords.txt", "w") as f:
        for c in tqdm.tqdm(list(ascii_lowercase) + ["number", "other"]):
            for t in get_titles(f"data/{c}.json"):
                print(t, file=f)


if __name__ == "__main__":
    generate_keywords()
