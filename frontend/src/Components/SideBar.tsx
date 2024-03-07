import { Button, Divider, Grid, Stack, Typography } from "@mui/material"
import { gameState } from "./Context";
import { startGame } from "@/API/api";
import { useState } from "react";

type props = {
    stateUpdater: React.Dispatch<React.SetStateAction<gameState>>,
    setHide: React.Dispatch<React.SetStateAction<boolean>>,
}

export default function SideBar(props: props) {
    const handleHide = () => {
        props.setHide(true);
    }

    const handleNewGame = () => {
        startGame(props.stateUpdater);
    }

    return (
        <Stack 
            spacing="1"
            width="25"
            maxHeight="80"
            alignItems="center"
            justifyContent="flex-start"
            p ='5'
            >
                <Grid item>
                    <Typography variant="h6">Contents</Typography>
                    <Button onClick={handleHide} variant="contained" color="secondary">Hide</Button>
                </Grid>
                <Divider/>
                <Typography variant="h6">(Top)</Typography>
                <Button variant="text" color="info" onClick={handleNewGame}>New Game</Button>
                <Typography>Time: 0.00</Typography>
                <Button variant="text"  color="info" onClick={() => null}>Hint</Button>
        </Stack>
    );
}