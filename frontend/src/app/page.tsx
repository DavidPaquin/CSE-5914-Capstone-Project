"use client";
import * as React from 'react';
import { Box, Container, Grid, Typography } from "@mui/material";
import Header from '@/Components/Header';
import SideBar from '@/Components/SideBar';
import Body from '@/Components/Body';

const data = {
  title: "Python (programming language)",
  source: "Wikipedia",
  text: `r"""Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability with the use of significant indentation.[31]
  Python is dynamically typed and garbage-collected. It supports multiple programming paradigms, including structured (particularly procedural), object-oriented and functional programming. It is often described as a "batteries included" language due to its comprehensive standard library.[32][33]
  Guido van Rossum began working on Python in the late 1980s as a successor to the ABC programming language and first released it in 1991 as Python 0.9.0.[34] Python 2.0 was released in 2000. Python 3.0, released in 2008, was a major revision not completely backward-compatible with earlier versions. Python 2.7.18, released in 2020, was the last release of Python 2.[35]
  Python consistently ranks as one of the most popular programming languages, and has gained widespread use in the machine learning community.[36][37][38][39]"""`,
}

export default function Home() {
  return (
    <Container maxWidth='lg'>
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
            <SideBar/>
            <Body title={data.title} source={data.source} text={data.text}/>
          </Grid>
      </Box>
    </Container>
  );
}
