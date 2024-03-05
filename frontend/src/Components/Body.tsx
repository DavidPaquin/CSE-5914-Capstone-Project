import { Box, Divider, Grid, Typography } from "@mui/material";

type props = {
    title?: string,
    text?: string,
    source?: string,
}

export default function Body(props: props) {
    return(
        <Box sx={{
            width:'75',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'start',
            alignItems: 'start',
        }}>
            <Typography variant="h5">{props.title}</Typography>
            <Divider/>
            <Typography>From {props.source}</Typography>
            <Typography>{props.text}</Typography>
        </Box>
    );
}