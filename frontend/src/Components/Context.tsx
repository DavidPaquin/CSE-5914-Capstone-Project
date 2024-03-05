import { Dispatch, createContext, useState } from "react";

export type gameState = {
    game_id?: number,
    currentArticle?: {
        id: number,
        title: string,
        text: string,
        source: string,
    }
    endArticleTitle?: string
    numClicks: number,
    currentQuery?: string,
}

export function  getInitGameState():gameState{
    return gameState;
}

export const gameState: gameState = {
    numClicks: 0,
    currentQuery: "",
}

const setGameState: Dispatch<any> = () => null

export const state = createContext({gameState, setGameState});


