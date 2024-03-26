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
            text: "Welcome to the Wiki game! EXPLAIN GAME HERE",
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