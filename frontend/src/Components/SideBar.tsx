import { Button, Divider, Grid, Stack, Typography } from "@mui/material"
import { gameState } from "./Context";
import { startGame, startGameRes } from "@/API/api";
import { useState } from "react";

type props = {
    state: gameState,
    setState: React.Dispatch<React.SetStateAction<gameState>>,
    setHide: React.Dispatch<React.SetStateAction<boolean>>,
}

export default function SideBar(props: props) {
    const {state, setState, setHide} = props;
    const handleHide = () => {
        props.setHide(true);
    }

    const handleNewGame = () => {
        startGame().then(data => {
            return data as startGameRes;
          }).then(data => {
            setState(prevState => ({
              ...prevState,
              game_id: data.game_id,
              currentArticle: data.start_article,
              endArticle: data.end_article
            }));
          })
    }

    return (
        <Stack 
            spacing="1"
            width="25"
            maxHeight="80"
            alignItems="left"
            justifyContent="flex-start"
            p ='5'
            >
                <Grid item>
                    <Typography variant="h6">Contents</Typography>
                    <Button onClick={handleHide} variant="contained" color="secondary">Hide</Button>
                </Grid>
                <Divider/>
                <Typography variant="h6">(Top)</Typography>
                <Typography>Start article: {state.currentArticle.title}</Typography>
                <Typography>End Article: {state.endArticle?.title}</Typography>
                <Button variant="text" color="info" onClick={handleNewGame}>New Game</Button>
                <Button variant="text"  color="info" onClick={() => null}>Hint</Button>
        </Stack>
    );
}