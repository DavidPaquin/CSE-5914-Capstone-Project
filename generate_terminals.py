from collections import defaultdict
import requests


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://wikitech.wikimedia.org/",
    "DNT": "1",
}


def process(year, month, ranking):
    url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia.org/all-access/{year}/{month:02d}/all-days"
    resp = requests.get(url=url, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    for d in data["items"][0]["articles"]:
        ranking[d["article"]] += int(d["views"])


def scroll_history():
    ranking = defaultdict(int)
    for year in range(2016, 2021):
        for month in range(1, 13):
            print(f"Processing {year}-{month:02d}...", end="")
            process(year, month, ranking)
            print("done!")
    return ranking


def remove_specials(title):
    return not (
        title.split(":")[0]
        in ("Special", "Help", "Wikipedia", "File", "User", "Template", "Category", "Portal")
        or title in ("Main_Page", "404.php")
        or "disambiguation" in title.lower()
    )


def curate_terminal_articles():
    ranking = scroll_history()
    ranked = sorted(ranking, key=ranking.get, reverse=True)
    curated = filter(remove_specials, ranked)
    final = map(lambda s: s.replace("_", " "), curated)

    with open("terminal_articles.txt", "w", encoding="utf-8") as f:
        for i, x in enumerate(final, 1):
            # print(f"{i:2d}. {x:50s}", ranking[x])
            print(x, file=f)


if __name__ == "__main__":
    curate_terminal_articles()
