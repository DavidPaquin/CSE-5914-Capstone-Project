import { createTheme } from "@mui/material";

const theme = createTheme({
    palette : {
        primary : {
            main: '#FFFFFF',
        },
        secondary : {
            main: '#f8f9fa',
            dark: '#aaa'
        },
        background: {
            default: "#FFFFFF"
        },
    },
    
    typography: {
        fontFamily: [
            'sans-serif',,
        ].join(','),
        h5 : {
           fontStyle : 'bold' 
        },
        h6 : {
            fontStyle: 'bold'
        },
    },

    components : {
        MuiButton : {
            defaultProps : {
                disableRipple : true,
                disableFocusRipple: true,
                disableElevation: true,
            }
        }
    }
})

export default theme;