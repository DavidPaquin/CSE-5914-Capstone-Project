import { Box, Button, Divider, Grid, List, ListItem, Popover, PopoverProps, Typography } from "@mui/material";
import { useState } from "react";
import { getMoves } from "@/API/api";
import { article, gameState } from "./Context";

type props = {
    game_id?: number,
    currentArticle?: article,
    setState: React.Dispatch<React.SetStateAction<gameState>>,
}

export default function Body(props: props) {
    const {game_id, currentArticle, setState} = props;
    const [articles, setArticles] = useState<Array<article>>();
    const [open, setOpen] = useState(false);
    const [anchorEl, setAnchorEl] = useState<PopoverProps['anchorEl']>(null);

    function handleClick(article: article){
        setState(prevState => ({
            ...prevState,
            currentArticle: article,
          }));
    }

    const handleClose = () => {
        setOpen(false);
    };

    //The highlighting stuff
    const handleMouseUp = async () => {
        const selection = window.getSelection();
        
        if (!selection || selection.anchorOffset === selection.focusOffset) {
          return;
        }
        const getBoundingClientRect = () => {
          return selection.getRangeAt(0).getBoundingClientRect();
        };

        //Get a list of articles similar to the query
        getMoves(game_id || 0, selection.toString()).then(data => {
            return data as Array<article>;
        }).then(articles => setArticles(articles))
    
        setOpen(true);
        setAnchorEl({ getBoundingClientRect, nodeType: 1 });
    };

    return(
        <Box sx={{
            width:'75',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'start',
            alignItems: 'start',
            }}>
                <Typography variant="h5">{currentArticle?.title}</Typography>
                <Divider/>
                <Typography>From {currentArticle?.source}</Typography>
                <Typography onMouseUp={handleMouseUp}>{currentArticle?.text}</Typography>
                <Popover
                    open={open}
                    anchorEl={anchorEl}
                    anchorOrigin={{ vertical: 'bottom', horizontal: 'left' }}
                    onClose={handleClose}
                    disableAutoFocus
                >
                    <List>
                        {articles?.map(article => {
                            return (
                                <Button onClick={() => handleClick(article)}>
                                    <ListItem>{article.title}</ListItem>
                                </Button>
                            )
                        })}
                    </List>
                </Popover>
        </Box>
    );
}