import { article, gameState } from "@/Components/Context";

export interface startGameRes {
    game_id: number,
    start_article: article
    end_article: article
}

//Initialize a game state, get a gameID, start article, and end article
export async function startGame(){
    const res = await fetch(`http://127.0.0.1:5000/api/start_game`, {
      method: 'POST'
    });

    return res.json();
}

//Given an string of text, get related articles (1-3 articles currently)
export async function getMoves(game_id: number, currentQuery: string){
    const link = `http://127.0.0.1:5000/api/new_turn/"+game_id` + game_id.toString();
    
    const res = await fetch(link, {
        method: 'POST',
        mode: 'cors',
        headers: {'Content-Type' : 'application/json'},

        body: JSON.stringify({
          article_id : game_id,
          query: currentQuery
        })
      });

      return res.json();
}