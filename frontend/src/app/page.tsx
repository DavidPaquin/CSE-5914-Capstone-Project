'use client'
import Image from "next/image";
import styles from "./page.module.css";
import React, { useState, useEffect } from "react";



export default function Home() {

  const [articles, setArticles] = useState([])


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
    console.log("1")
    fetchData()

  }, [])
  if (articles.length == 0) { return (<div><h1>Loading</h1></div>)}
  
  return (
    
    <div>
      <h1>
      {articles.start_article.title}
      </h1>
      <p>{articles.start_article.text}</p>

    </div>

  )

}


