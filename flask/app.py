from flask import Flask, request, jsonify
from flask_cors import CORS,cross_origin
from elasticsearch import Elasticsearch, helpers
import uuid
from game import Game
from queries import *
import os
import random

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
es = Elasticsearch(
        "https://localhost:9200",
        ca_certs=os.environ["PATH_TO_HTTPCA_CERT"],
        basic_auth=("elastic", os.environ["ELASTIC_PASSWORD"]),
    )

#Create a dictionary of game_id: Game
games = dict()
#Load terminal articles into memory
with open("../terminal_articles.txt", encoding="utf-8") as f:
    top_articles = [title.strip() for title in f.readlines()]
    top_count = len(top_articles)

#Randomly sample 2 articles from the top articles list, with denom limiting the allowed minimum popularity
def pick_top_articles(denom=1):
    start_title, end_title = random.sample(top_articles[0:top_count//denom], 2)
    return [search_title_exact(es, start_title)['hits']['hits'][0], search_title_match(es, end_title)['hits']['hits'][0]]

#Define endpoints for Flask API

#This function runs when a GET request is sent to 127.0.0.1:{port}
@app.route("/")
def index() -> str:
    #Render some html with a link when a user visits the site with no path
    if len(games) > 0:
        return f"There are {len(games)} games currently running. <br />Navigate to <a href=\"/search_article/{list(games.keys())[0]}\"> /search_article/{list(games.keys())[0]} </a> to search the database. <br />Navigate to <a href=\"/start_article/{list(games.keys())[0]}\"> /start_article/{list(games.keys())[0]} </a> to get a random start article.<br /> <form action = \"/api/start_game\" method =\"post\"> <input type=\"submit\" value = \"Create New Game\"></form>" 
    else:
        return "There are no games currently running. <br /> <form action = \"/api/start_game\" method =\"post\"> <input type=\"radio\" id=\"easy\" name=\"difficulty\" value=\"easy\"> <label for=\"easy\">Easy</label>  <input type=\"radio\" id=\"medium\" name=\"difficulty\" value=\"medium\"> <label for=\"medium\">Medium</label>  <input type=\"radio\" id=\"hard\" name=\"difficulty\" value=\"hard\"> <label for=\"hard\">Hard</label> <input type=\"radio\" id=\"impossible\" name=\"difficulty\" value=\"impossible\"> <label for=\"impossible\">Impossible</label> <input type=\"submit\" value = \"Create New Game\"></form>"     

#This function runs when a POST request is sent to 127.0.0.1:{port}/serve_article/{id}
@app.post("/serve_article/<uuid:id>")
@cross_origin()
def serve_article_post(id: uuid.UUID) -> dict:
    #Check if the given id matches the player
    if id not in games:
        print(f"Got an id of {id} which is not a valid game.")
        return jsonify({"error": "The provided id does not match a valid game id."})
    
    #Obtain the search query from the request
    if request.content_type != "application/json":
        print(f"The expected request content_type is \"application/json\" - instead got {request.content_type}")
        return jsonify({"error": f"The expected request content_type is \"application/json\" - instead got {request.content_type}"})
    
    body = request.get_json()
    print(f"Request body: {body}")

    if "search" not in body:
        return jsonify({"error": "The provided request body was malformed, does not contain 'search' key."})
    
    #Searches for given title and returns the first result
    resp = search_title_match_phrase(es, body["search"])
    return jsonify(resp['hits']['hits'][0]["_source"])
    
@app.get("/search_article/<uuid:id>")
def search_article_get(id: uuid.UUID):
    if id not in games:
        return jsonify({"error": "The provided id does not match a valid game id."})
    return "<form method =\"post\">  <label for=\"title\">Term:</label><br> <input type=\"text\" id=\"Term\" name = \"Term\"> <input type=\"submit\" value = \"Submit\"></form>"

@app.post("/search_article/<uuid:id>")
@cross_origin()
def search_article_post(id: uuid.UUID):
    if id not in games:
        return jsonify({"error": "The provided id does not match a valid game id."})
    resp = search_title_match_phrase(es, request.form['Term'])
    if len(resp["hits"]["hits"]):
        title = resp['hits']['hits'][0]["_source"]["title"]
        text = resp['hits']['hits'][0]["_source"]["text"]
        print(f"_id of Searched Article: {resp['hits']['hits'][0]['_id']}")
        # print(f"Attribute 'id' of Searched Article: {resp['hits']['hits'][0]['_source']['id']}")
        return "<form method =\"post\">  <label for=\"title\">Term:</label><br> <input type=\"text\" id=\"Term\" name = \"Term\"> <input type=\"submit\" value = \"Submit\"></form> <br> <h1>"+title+"</h1><br><p>"+text+"</p>"
    return "<form method =\"post\">  <label for=\"title\">Term:</label><br> <input type=\"text\" id=\"Term\" name = \"Term\"> <input type=\"submit\" value = \"Submit\"></form> <br> <h1>No results found</h1>"

@app.get("/start_article/<uuid:id>")
def start_article_get(id: uuid.UUID):
    if id not in games:
        return jsonify({"error": "The provided id does not match a valid game id."})
    game = games[id]
    start_article = search_id(es, game.start_article)
    title = start_article["_source"]["title"]
    text = start_article["_source"]["text"]
    return "<p>This is a random article found when the app is run</p><br><h2>"+title+"</h2><br><p>"+text+"</p>"+f"<form action = \"/api/new_articles/{id}\" method =\"post\">  <label for=\"title\">Term:</label><br> <input type=\"text\" id=\"query\" name = \"query\"> <input type=\"submit\" value = \"Submit\"></form>"

@app.post("/api/start_game")
@cross_origin()
def start_game_post():
    #Create a new id and matching Game object
    new_id = uuid.uuid4()
    #Choose articles based on difficulty
    difficulty = request.form["difficulty"].strip().lower()
    if difficulty == "impossible":
        start_article, end_article = search_random(es)['hits']['hits'][0:2]
    elif difficulty == "easy":
        start_article, end_article = pick_top_articles(4)
    elif difficulty == "medium":
        start_article, end_article = pick_top_articles(2)
    elif difficulty == "hard":
        start_article, end_article = pick_top_articles()

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
    return jsonify(resp)

@app.post("/api/debug_start_game")
@cross_origin()
def debug_start_game_post():
    #Create a new id and matching Game object
    new_id = uuid.uuid4()
    # start_article = search_id_match(es, "22217")['hits']['hits'][0] #OSU
    # end_article = search_id_match(es, "21255")['hits']['hits'][0] #North Korea
    start_article = search_title_exact(es, "Ohio State University")['hits']['hits'][0]
    end_article = search_title_exact(es, "North Korea")['hits']['hits'][0]
    #Path: OSU;"research university" -> Research University;"nuclear weapons" -> Nuclear Weapons convention;"North Korea" -> North Korea 
    games[new_id] = Game(new_id, start_article["_id"], end_article["_id"])
    print(f"A new DEBUG game was created: {games[new_id]}")
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
    return jsonify(resp)

@app.post("/api/new_turn/<uuid:id>")
@cross_origin()
def new_turn_post(id: uuid.UUID):
    if id not in games:
        return jsonify({"error": "The provided id does not match a valid game id."})
    #retrieve article id to be compared
    data = request.get_json()
    game = games[id]
    if not game.hop(data["article_id"]):
        return jsonify({"error": "The chosen article does is not a valid choice."})
    resp = {"game_id":id,
            "check_win":str(game.check_win(data["article_id"])),
            "history": game.history
    }
    return jsonify(resp)

@app.post("/api/new_articles/<uuid:id>")
@cross_origin()
def new_articles(id: uuid.UUID):
    if id not in games:
        return jsonify({"error": "The provided id does not match a valid game id."})
    article_count = 3 #return 3 articles
    game = games[id]
    query = request.form["query"].strip()
    #Anti cheat ensure query is actually in current article text
    current_article = search_id(es, game.history[-1])
    if query not in current_article["_source"]["text"]:
        #Query wasn't found in the current article
        print(f"ANTICHEAT: Query not in current article.\n  GAME ID: {id}\n   ARTICLE ID: {game.history[-1]}\n  QUERY: \"{query}\"")
        return jsonify({"error": "The query was not found in the current article."})
    #Get the articles from the ES database based
    articles = search_title_match_phrase(es, query, article_count)
    #Build the response dynamically and update game object
    game.choices = []
    resp = {
        "game_id": id,
        "articles": []
    }
    for article in articles['hits']['hits']:
        article_dict = {
            "id": article["_id"],
            "title": article["_source"]["title"],
            "text": article["_source"]["text"],
            "source": "Wikipedia"
        }
        resp["articles"].append(article_dict)
        game.choices.append(article["_id"])
    return jsonify(resp)