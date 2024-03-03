'use client'
import Image from "next/image";
import styles from "./page.module.css";
import React, { useState, useEffect } from "react";



export default function Home() {

  const [articles, setArticles] = useState([])
  const [searchArticles, setSearchArticles] = useState([])
  const [win, setWin] = useState([])
  const [selectedArticle, setSelectedArticle] = useState([])



  const fetchData = () => {
    fetch("http://127.0.0.1:5000/api/start_game", {method: 'POST'})

      .then(response => {
        return response.json()

      })

      .then(data => {

        setArticles(data)

      })

  }


  useEffect(() => {
    fetchData()

  }, [])
  if (articles.length == 0) { return (<div><h1>Loading</h1></div>)}
  const game_id =articles.game_id
  function submitForm(event) {
    event.preventDefault();
    const sendData = new FormData(event.target)
    const link = "http://127.0.0.1:5000/api/new_articles/"+game_id
    fetch(link,
      {
        method: 'POST',
        mode: 'cors',
        body: sendData
      })
      .then(response => {
        return response.json()
      })

      .then(data => {
        if (data.articles) {
          setSearchArticles(data)
          setSelectedArticle([])
        }

      })
  }

  function selectArticle(ind) {
    const article = searchArticles.articles[ind]
    setSelectedArticle(article)
    const id = article.id
    const link = "http://127.0.0.1:5000/api/new_turn/"+game_id
    fetch(link,
      {
        method: 'POST',
        mode: 'cors',
        headers: {'Content-Type' : 'application/json'},

        body: JSON.stringify({article_id : id})
      })
      .then(response => {
        return response.json()
      })

      .then(data => {

        setWin(data)

      })
  }
  if (searchArticles.length == 0){
    return (
      <div>
        <p>End Article: {articles.end_article.title}</p>
        <form onSubmit={submitForm}>
          <label>
            Title:
          </label>
          <input type="text" id="query" name ="query"></input> <br></br>
          <input type="submit"  value="submit"></input>
        </form>
        <h1>
        {articles.start_article.title}
        </h1>
        <p>{articles.start_article.text}</p>

      </div>

    )
  }

  if (win.length != 0 && win.check_win == "True" )
    return (<h1>YOU WIN!</h1>)

  if (selectedArticle.length == 0) {
    return (
      <div>
        <p>End Article: {articles.end_article.title}</p>
        <form onSubmit={submitForm}>
            <label>
              Title:
            </label>
            <input type="text" id="query" name ="query"></input> <br></br>
            <input type="submit"  value="submit"></input>
          </form>
        <h1>
          {searchArticles.articles[0].title}
        </h1>
        <button onClick={() => selectArticle(0)}>Select Article 1</button>
        <h1>
          {searchArticles.articles.length >1 ? searchArticles.articles[1].title : undefined}
        </h1>
        <button onClick={() => selectArticle(1)}>Select Article 2</button>
        <h1>
          {searchArticles.articles.length >2 ? searchArticles.articles[2].title : undefined}
        </h1>
        <button onClick={() => selectArticle(2)}>Select Article 3</button>
      </div>
    )
  }
  return (
    
    <div>
      <p>End Article: {articles.end_article.title}</p>
      <form onSubmit={submitForm}>
        <label>
          Title:
        </label>
        <input type="text" id="query" name ="query"></input> <br></br>
        <input type="submit"  value="submit"></input>
      </form>
      <h1>
      {selectedArticle.title}
      </h1>
      <p>{selectedArticle.text}</p>

    </div>

  )
}



