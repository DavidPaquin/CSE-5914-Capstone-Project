from collections import defaultdict
import requests
from heapq import nlargest

ranking = defaultdict(int)


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://wikitech.wikimedia.org/",
    "DNT": "1",
}


def process(year, month):
    url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia.org/all-access/{year}/{month:02d}/all-days"
    resp = requests.get(url=url, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    for d in data["items"][0]["articles"]:
        ranking[d["article"]] += int(d["views"])


def scroll_history():
    for year in range(2016, 2024):
        for month in range(1, 13):
            print(f"Processing {year}-{month:02d}...", end="")
            process(year, month)
            print("done!")


if __name__ == "__main__":
    scroll_history()
    biggest = sorted(ranking, key=ranking.get, reverse=True)
    with open("terminal_articles.txt", "w") as f:
        for i, x in enumerate(biggest, 1):
            # print(f"{i:2d}. {x:50s}", ranking[x])
            print(x.replace("_", " "), file=f)

