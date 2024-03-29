from elasticsearch import Elasticsearch, helpers
import tqdm
import os
import json


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
            elif cur == 3:
                words = line.split(":")
                title = words[-1][1:-1] + ","
                if title[0] != '"' or title[-2] != '"':
                    words[-1] = f' "{title}",'
                    line = ":".join(words)
                obj.append(line)
            elif cur == 2:
                obj.append(line)
            elif cur == 4:
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
                        "fields": {"keyword": {"type": "keyword"}},
                    },
                    "text": {"type": "text"},
                }
            }
        },
    )


def hydrate(ES, index_name, json_file):
    for batch in lazy_load(json_file, 5_000):
        action_list = [
            {"_op_type": "index", "_index": index_name, "_source": data_row}
            for data_row in batch
        ]
        helpers.bulk(ES, action_list)
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
    for file in tqdm.tqdm(
        [
            f
            for f in os.listdir("data/")
            if os.path.isfile(os.path.join("data/", f)) and f.lower().endswith(".json")
        ]
    ):
        hydrate(ES, index_name, os.path.join("data/", file))


if __name__ == "__main__":
    # NOTE: Make sure ES is running in Docker before running this script!
    hydrate_all()
