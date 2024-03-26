import { Button, Divider, Grid, Stack, Typography } from "@mui/material"
import { gameState } from "./Context";
import { startGame, startGameRes } from "@/API/api";
import { useEffect, useState } from "react";

type props = {
    state: gameState,
    setState: React.Dispatch<React.SetStateAction<gameState>>,
}

export default function SideBar(props: props) {
    const {state, setState} = props;
    const [time, setTime] = useState(Date.now());
    
    //Update the time each second 
    useEffect(() => {
        const interval = setInterval(() => setTime(Math.floor((Date.now() / 1000 / 60) % 60)), 1000);
        return () => clearInterval(interval);
    },[]);

    //Make a new game
    const handleNewGame = () => {
        startGame().then(data => {
            return data as startGameRes;
          }).then(data => {
            setState(prevState => ({
              ...prevState,
              game_id: data.game_id,
              currentArticle: data.start_article,
              endArticle: data.end_article,
              startTime: Date.now(),
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
                </Grid>
                <Divider/>
                <Typography variant="h6">(Top)</Typography>
                <Typography>Start article: {state.currentArticle.title}</Typography>
                <Typography>End Article: {state.endArticle?.title}</Typography>
                <Typography>Time: {time}</Typography>
                <Button variant="text" color="info" onClick={handleNewGame}>New Game</Button>
        </Stack>
    );
}