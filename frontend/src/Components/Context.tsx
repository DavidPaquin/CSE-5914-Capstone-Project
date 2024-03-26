export interface article {
    id: number,
    title: string,
    text: string,
    source: string
}

export interface gameState {
    game_id: number,
    currentArticle: article,
    endArticle?: article,
    win: boolean,
    history: Array<article>,
    startTime: number,
}

export function getInitGameState():gameState{
    return {
        game_id: -1,
        currentArticle: {
            id: -1,
            title: "The Wiki Game",
            text: "Welcome to the Wiki game! The objective of the wiki game is to get from one article to another by highlighting text and selecting articles related to the end article.To start a new game, click \"New Game\".",
            source: "The Wiki wanders"
        },
        win: false,
        history: [],
        startTime: Date.now(),
    };
}

/* 
In case we want to use a context instead of prop drilling
const setGameState: Dispatch<any> = () => null
export const state = createContext({gameState, setGameState});
*/