export interface article {
    id: number,
    title: string,
    text: string,
    source: string
}

export interface gameState {
    game_id?: number,
    currentArticle?: article,
    endArticle?: article,
}

export function  getInitGameState():gameState{
    return gameState;
}

export const gameState: gameState = {
}

/* 
In case we want to use a context instead of prop drilling
const setGameState: Dispatch<any> = () => null
export const state = createContext({gameState, setGameState});
*/