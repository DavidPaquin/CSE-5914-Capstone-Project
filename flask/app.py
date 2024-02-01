from flask import Flask
from flask import request
from elasticsearch import Elasticsearch, helpers
import uuid
import os

#Searches title field for given phrase
def search_title(ES, query):
    resp = es.search( index="articles",
    body={
        "query": {
            "match_phrase": {
                "title": {
                    "query": query}
            }
        }
    },
    )
    return resp

app = Flask(__name__)
es = Elasticsearch(
        "https://localhost:9200",
        ca_certs=os.environ["PATH_TO_HTTPCA_CERT"],
        basic_auth=("elastic", os.environ["ELASTIC_PASSWORD"]),
    )

#Create an id for one player
player_id = uuid.uuid4()
print(f"The game id is: {player_id}")

#An example response containing the Python Wikipedia page
article_python = {
    "title": "Python (programming language)",
    "source": "Wikipedia",
    "text": r"""Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation.[31]
Python is dynamically typed and garbage-collected. It supports multiple programming paradigms, including structured (particularly procedural), object-oriented and functional programming. It is often described as a "batteries included" language due to its comprehensive standard library.[32][33]
Guido van Rossum began working on Python in the late 1980s as a successor to the ABC programming language and first released it in 1991 as Python 0.9.0.[34] Python 2.0 was released in 2000. Python 3.0, released in 2008, was a major revision not completely backward-compatible with earlier versions. Python 2.7.18, released in 2020, was the last release of Python 2.[35]
Python consistently ranks as one of the most popular programming languages, and has gained widespread use in the machine learning community.[36][37][38][39]"""
}

#An example response containing the C Wikipedia page
article_c = {
    "title": "C (programming language)",
    "source": "Wikipedia",
    "text": r"""C (pronounced /ˈsiː/ – like the letter c)[6] is a general-purpose computer programming language. It was created in the 1970s by Dennis Ritchie, and remains very widely used and influential. By design, C's features cleanly reflect the capabilities of the targeted CPUs. It has found lasting use in operating systems, device drivers, and protocol stacks, but its use in application software has been decreasing.[7] C is commonly used on computer architectures that range from the largest supercomputers to the smallest microcontrollers and embedded systems.
A successor to the programming language B, C was originally developed at Bell Labs by Ritchie between 1972 and 1973 to construct utilities running on Unix. It was applied to re-implementing the kernel of the Unix operating system.[8] During the 1980s, C gradually gained popularity. It has become one of the most widely used programming languages,[9][10] with C compilers available for practically all modern computer architectures and operating systems. The book The C Programming Language, co-authored by the original language designer, served for many years as the de facto standard for the language.[11][1] C has been standardized since 1989 by the American National Standards Institute (ANSI) and the International Organization for Standardization (ISO).
"""
}

#This function runs when a GET request is sent to 127.0.0.1:{port}
@app.route("/")
def index() -> str:
    #Render some html with a link when a user visits the site with no path
    return f"A player was generated with id: {player_id}. Navigate to <a href=\"/serve_article/{player_id}\"> /serve_article/{player_id} </a> to see an example response." 

#This function runs when a GET request is sent to 127.0.0.1:{port}/serve_article/{id}
@app.get("/serve_article/<uuid:id>")
def serve_article_get(id: uuid.UUID) -> dict:
    #Check if the given id matches the player
    if id == player_id:
        #Serve an example article
        return article_python
    else:
        return {"error": "The provided id does not match a valid player id."}

#This function runs when a POST request is sent to 127.0.0.1:{port}/serve_article/{id}
@app.post("/serve_article/<uuid:id>")
def serve_article_post(id: uuid.UUID) -> dict:
    #Check if the given id matches the player
    if id != player_id:
        return {"error": "The provided id does not match a valid player id."}
    
    #Obtain the search query from the request
    if request.content_type != "application/json":
        print(f"The expected request content_type is \"application/json\" - instead got {request.content_type}")
        return {"error": f"The expected request content_type is \"application/json\" - instead got {request.content_type}"}
    
    body = request.get_json()
    print(f"Request body: {body}")

    if "search" not in body:
        return {"error": "The provided request body was malformed, does not contain 'search' key."}
    
    #TODO: We would perform the elasticsearch query here in the real application
    """if body["search"].lower() == "python":
        print("Serving python article.")
        return article_python
    elif body["search"].lower() == "c":
        print("Serving C article.")
        return article_c
    else:
        return body
    """
    #Searches for given title and returns the first result
    resp = search_title(es, body["search"])
    return resp['hits']['hits'][0]["_source"]
        