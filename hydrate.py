from elasticsearch import Elasticsearch, helpers
import tqdm
import os
from string import ascii_lowercase
import json
import re


def lazy_load(json_file, batch_size):
    first = True
    with open(json_file, "r", encoding="utf-8") as f:
        cur, output = 0, []
        for line in f:
            if first:
                first = False
                continue

            if cur == 0:
                obj = ["{"]
            elif cur == 1:
                words = line.split(":")
                title = words[-1][1:-1]
                if title[0] != '"' or title[-2] != '"':
                    words[-1] = f' "{title}",'
                    line = ":".join(words)
                obj.append(line)
            elif cur == 2:
                obj.append(line)
            elif cur == 3:
                obj.append("}")
                output.append(json.loads("".join(obj), strict=False))
                cur = -1
            cur += 1
            if len(output) == batch_size:
                yield output
                output = []
    yield output


def clean_index(ES, index_name):
    try:
        ES.indices.delete(index=index_name)
    except:
        pass

    ES.indices.create(
        index=index_name,
        body={
            "mappings": {
                    "properties": {
                        "title": {
                            "type": "text",
                            "fields": {
                                "keyword": {
                                    "type": "keyword"
                                }
                            }
                        }, "text": {"type": "text"}}
                    }
                }
    )


def hydrate(ES, index_name, json_file):
    total = 0
    pattern = re.compile(r"^\{$")
    with open(json_file, "r", encoding="utf-8") as f:
        for line in f:
            if pattern.match(line):
                total += 1
    with tqdm.tqdm(total=total) as progress:
        progress.set_description(desc=json_file)
        for batch in lazy_load(json_file, 5_000):
            action_list = [
                {"_op_type": "index", "_index": index_name, "_source": data_row}
                for data_row in batch
            ]
            helpers.bulk(ES, action_list)
            progress.update(len(batch))
    ES.indices.refresh(index=index_name)


def hydrate_all():
    ES = Elasticsearch(
        "https://localhost:9200",
        ca_certs=os.environ["PATH_TO_HTTPCA_CERT"],
        basic_auth=("elastic", os.environ["ELASTIC_PASSWORD"]),
        retry_on_timeout=True,
        request_timeout=100,
    )
    index_name = "articles"
    clean_index(ES, index_name)
    for c in list(ascii_lowercase) + ["number", "other"]:
        hydrate(ES, index_name, f"data/{c}.json")


if __name__ == "__main__":
    # NOTE: Make sure ES is running in Docker before running this script!
    hydrate_all()
