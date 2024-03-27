"use client";
import * as React from 'react';
import { Box, Container, Dialog, Grid, Typography } from "@mui/material";
import Header from '@/Components/Header';
import SideBar from '@/Components/SideBar';
import Body from '@/Components/Body';
import { startGame, startGameRes } from '@/API/api';
import { useEffect, useState } from 'react';
import { getInitGameState, gameState } from '@/Components/Context';

export default function Home() {
  const [gameState, setGameState] = useState<gameState>(getInitGameState);

  //Create a new game at initialization and when win
  /*useEffect(() => {
    startGame().then(data => {
      return data as startGameRes;
    }).then(data => {
      setGameState(prevState => ({
        ...prevState,
        game_id: data.game_id,
        currentArticle: data.start_article,
        endArticle: data.end_article,
        startTime: Date.now(),
      }));
    })
  },[gameState.win]);
  */

  return (
    <Container maxWidth='lg'>
      {console.log(gameState.win)}
      {console.log(gameState)}
      {console.log(gameState.win == "True")}
      <Box
        sx={{
          my: 4,
          display: 'start',
          flexDirection: 'column',
          justifyContent: 'start',
          alignItems: 'center',
        }}
      >
        <Header/>
        <Grid
          sx={{
            display: 'flex',
            flexDirection: 'row',
            justifyContent: 'center',
            alignItems: 'center'
          }}
        >
            <SideBar state={gameState} setState={setGameState}/>
            <Body game_id={gameState.game_id} currentArticle={gameState.currentArticle} setState={setGameState}/>
          </Grid>
      </Box>
      <Dialog open={gameState.win == "True"} onClose={() => setGameState(getInitGameState)}>
          <Typography variant={'h5'}>Congrats!</Typography> 
          <Typography>You've gone from {gameState.startTitle} to {gameState.endArticle?.title} in {gameState.history.length} moves!</Typography>
      </Dialog>
    </Container>
  );
}
