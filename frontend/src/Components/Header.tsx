import { Box, Button, Divider, Grid, InputAdornment, TextField, Typography } from "@mui/material";
import SearchIcon from '@mui/icons-material/Search';
import MoreHorizIcon from '@mui/icons-material/MoreHoriz';


type props = {

}

export default function Header(props: props) {
    return (
        <Box 
            width='100%' 
            height='8%'
            component='header'
            display='flex'
            alignItems='center'
            justifyContent='space-around'
            marginTop="1%"
            marginBottom="1%"
        >
            <Grid item alignItems="flex-start">
                <Typography variant="h5">The Wikipedia Game</Typography>
            </Grid>
            <Grid item paddingX="0" height="5%">
                <TextField
                    variant="outlined"
                    InputProps={{
                        startAdornment: (
                            <InputAdornment position="start">
                                <SearchIcon />
                            </InputAdornment>
                        ),
                    }}
                    size="small"
                    value="Search Wikipedia"
                />
                <Button variant="contained" color="secondary">Search</Button>
            </Grid>
            <Grid item>
                    <Button variant="text" color="info">Create account</Button>
                    <Button variant="text" color="info"> Log in</Button>
                    <Button>
                        <MoreHorizIcon color="primary"/>
                    </Button>
            </Grid>
        </Box>
    );
}