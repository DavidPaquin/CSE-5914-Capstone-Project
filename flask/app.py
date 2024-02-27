from flask import Flask
from flask import request
from elasticsearch import Elasticsearch, helpers
import uuid
from game import Game
import os

#Searches title field for given phrase
def search_title_match_phrase(es, query):
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

#Get the article with _id = id
def search_id(es, id):
    return es.get(index="articles", id=id)

app = Flask(__name__)
es = Elasticsearch(
        "https://localhost:9200",
        ca_certs=os.environ["PATH_TO_HTTPCA_CERT"],
        basic_auth=("elastic", os.environ["ELASTIC_PASSWORD"]),
    )

#Create a dictionary of game_id: Game
games = dict()

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
    if len(games) > 0:
        return f"There are {len(games)} games currently running. Navigate to <a href=\"/serve_article/{list(games.keys())[0]}\"> /serve_article/{list(games.keys())[0]} </a> to see an example response. <br />Navigate to <a href=\"/search_article/{list(games.keys())[0]}\"> /search_article/{list(games.keys())[0]} </a> to search the database. <br />Navigate to <a href=\"/start_article/{list(games.keys())[0]}\"> /start_article/{list(games.keys())[0]} </a> to get a random start article.<br /> <form action = \"/api/start_game\" method =\"post\"> <input type=\"submit\" value = \"Create New Game\"></form>" 
    else:
        return "There are no games currently running. <br /> <form action = \"/api/start_game\" method =\"post\"> <input type=\"submit\" value = \"Create New Game\"></form>"     

#This function runs when a GET request is sent to 127.0.0.1:{port}/serve_article/{id}
@app.get("/serve_article/<uuid:id>")
def serve_article_get(id: uuid.UUID) -> dict:
    #Check if the given id matches the player
    if id in games:
        #Serve an example article
        return article_python
    else:
        return {"error": "The provided id does not match a valid game id."}

#This function runs when a POST request is sent to 127.0.0.1:{port}/serve_article/{id}
@app.post("/serve_article/<uuid:id>")
def serve_article_post(id: uuid.UUID) -> dict:
    #Check if the given id matches the player
    if id not in games:
        print(f"Got an id of {id} which is not a valid game.")
        return {"error": "The provided id does not match a valid game id."}
    
    #Obtain the search query from the request
    if request.content_type != "application/json":
        print(f"The expected request content_type is \"application/json\" - instead got {request.content_type}")
        return {"error": f"The expected request content_type is \"application/json\" - instead got {request.content_type}"}
    
    body = request.get_json()
    print(f"Request body: {body}")

    if "search" not in body:
        return {"error": "The provided request body was malformed, does not contain 'search' key."}
    
    #Searches for given title and returns the first result
    resp = search_title_match_phrase(es, body["search"])
    return resp['hits']['hits'][0]["_source"]
    
@app.get("/search_article/<uuid:id>")
def search_article_get(id: uuid.UUID):
    if id not in games:
        return {"error": "The provided id does not match a valid game id."}
    return "<form method =\"post\">  <label for=\"title\">Term:</label><br> <input type=\"text\" id=\"Term\" name = \"Term\"> <input type=\"submit\" value = \"Submit\"></form>"

@app.post("/search_article/<uuid:id>")
def search_article_post(id: uuid.UUID):
    if id not in games:
        return {"error": "The provided id does not match a valid game id."}
    resp = search_title_match_phrase(es, request.form['Term'])
    if len(resp["hits"]["hits"]):
        title = resp['hits']['hits'][0]["_source"]["title"]
        text = resp['hits']['hits'][0]["_source"]["text"]
        return "<form method =\"post\">  <label for=\"title\">Term:</label><br> <input type=\"text\" id=\"Term\" name = \"Term\"> <input type=\"submit\" value = \"Submit\"></form> <br> <h1>"+title+"</h1><br><p>"+text+"</p>"
    return "<form method =\"post\">  <label for=\"title\">Term:</label><br> <input type=\"text\" id=\"Term\" name = \"Term\"> <input type=\"submit\" value = \"Submit\"></form> <br> <h1>No results found</h1>"

@app.get("/start_article/<uuid:id>")
def start_article_get(id: uuid.UUID):
    if id not in games:
        return {"error": "The provided id does not match a valid game id."}
    game = games[id]
    start_article = search_id(es, game.start_article)
    title = start_article["_source"]["title"]
    text = start_article["_source"]["text"]
    return "<p>This is a random article found when the app is run</p><br><h2>"+title+"</h2><br><p>"+text+"</p>"

@app.post("/api/start_game")
def start_game_post():
    #Create a new id and matching Game object
    new_id = uuid.uuid4()
    start_article, end_article = search_random(es)['hits']['hits'][0:2]
    games[new_id] = Game(new_id, start_article["_id"], end_article["_id"])
    print(f"A new game was created: {games[new_id]}")
    #Create the response
    resp = {
        "game_id": new_id,
        "start_article": {
            "id": games[new_id].start_article,
            "title": start_article["_source"]["title"],
            "text": start_article["_source"]["text"],
            "source": "Wikipedia"
        },
        "end_article": {
            "id": games[new_id].end_article,
            "title": end_article["_source"]["title"],
            "source": "Wikipedia"
        }
    }
    return resp

@app.post("/api/new_turn")
def new_turn_post(id: uuid.UUID):
    if id not in games:
        return {"error": "The provided id does not match a valid game id."}
    #retrieve article id to be compared
    data = request.get_json()
    Game.hop(games[id], data["article_id"])
    if Game.check_win(games[id], data["article_id"]):
        return {"game_id":id, "check_win":"true"}
    return {"game_id":id, "check_win":"false"}

@app.post("/api/new_articles")
def new_articles_post(id: uuid.UUID):
    if id not in games:
        return {"error": "The provided id does not match a valid game id."}
    #retrieve highlighted text for es
    query = request.get_json()
    resp = search_title_match_phrase(es, query["text"])
    return {
        "game_id":id,
        "article_1": {
            "id": resp['hits']['hits'][0]["_id"],
            "title": resp['hits']['hits'][0]["_source"]["title"],
            "text": resp['hits']['hits'][0]["_source"]["text"],
            "source": "Wikipedia"
        },
        "article_2": {
            "id": resp['hits']['hits'][1]["_id"],
            "title": resp['hits']['hits'][1]["_source"]["title"],
            "text": resp['hits']['hits'][1]["_source"]["text"],
            "source": "Wikipedia"
        },
        "article_3": {
            "id": resp['hits']['hits'][2]["_id"],
            "title": resp['hits']['hits'][2]["_source"]["title"],
            "text": resp['hits']['hits'][2]["_source"]["text"],
            "source": "Wikipedia"
        }
    }