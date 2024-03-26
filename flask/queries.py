# Queries to search into the ES database
from elasticsearch import Elasticsearch, helpers

#Searches title field for given phrase
def search_title_match_phrase(es, query, size=10):
    resp = es.search( index="articles",
    body={
        "query": {
            "match_phrase": {
                "title": {
                    "query": query}
            }
        }
    },
    size=size
    )
    return resp

def search_title_match(es, query):
    resp = es.search( index="articles",
    body={
        "query": {
            "match": {
                "title": {
                    "query": query}
            }
        }
    },
    )
    return resp

def search_title_exact(es, query):
    resp = es.search( index="articles",
    body={
        "query": {
            "term": {
                "title.keyword": query
            }
        }
    },
    )
    return resp

#Get 10 random articles
def search_random(es):
    resp = es.search( index="articles",
    body={
        "query": {
            "function_score": {
                "random_score": {}
            }
        }
    },
    )
    return resp

def search_similar(es, query):
    resp = es.search(index = "articles",
    body={
        "query": {
            "more_like_this": {
                "fields": ["text"],
                "like": query,
                "min_term_freq": 1,
                "min_doc_freq": 1    
            }
        }
    },
    )
    return resp

#Get the article with _id = id
def search_id(es, id):
    return es.get(index="articles", id=id)

#Get the article with ATTRIBUTE id = id
def search_id_match(es, id):
    resp = es.search( index="articles",
    body={
        "query": {
            "match": {
                "id": {
                    "query": id}
            }
        }
    },
    )
    return resp