from elasticsearch import Elasticsearch, helpers
import os
import pandas as pd
import json


def batched(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx : min(ndx + n, l)]


def hydrate(es, index_name, csv_file):
    try:
        es.indices.delete(index=index_name)
    except:
        pass

    # TODO: once we have the actual dataset, we should
    # add a mapping here to make sure types are set correctly
    es.indices.create(index=index_name)

    print("Reading CSV file...", end="", flush=True)
    df = pd.read_csv(csv_file)
    print("done!")
    json_records = json.loads(df.to_json(orient="records"))
    count, total = 0, len(df)
    for batch in batched(json_records, 25_000):
        action_list = [
            {"_op_type": "index", "_index": index_name, "_source": data_row}
            for data_row in batch
        ]
        helpers.bulk(es, action_list)
        count += len(batch)
        print(f"\rProgress: {count}/{total} rows indexed", end="")

    es.indices.refresh(index=index_name)
    print("\nHydration completed successfully")


if __name__ == "__main__":
    # NOTE: Make sure ES is running in Docker before running
    es = Elasticsearch(
        "https://localhost:9200",
        ca_certs=os.environ["PATH_TO_HTTPCA_CERT"],
        basic_auth=("elastic", os.environ["ELASTIC_PASSWORD"]),
    )
    index_name = "test"
    csv_file = "sample_data.csv"
    hydrate(es, index_name, csv_file)
