"use client"
import { CssBaseline, ThemeProvider } from "@mui/material";
import { AppRouterCacheProvider } from '@mui/material-nextjs/v14-appRouter';
import  theme from "@/app/theme";

export default function RootLayout(props: {children: React.ReactNode;}) {
  return (
    <html lang="en">
      <body>
      <AppRouterCacheProvider options={{ enableCssLayer: true }}>
        <ThemeProvider theme={theme}>
          <CssBaseline />
            {props.children}
        </ThemeProvider>
        </AppRouterCacheProvider>
      </body>
    </html>
  );
}
