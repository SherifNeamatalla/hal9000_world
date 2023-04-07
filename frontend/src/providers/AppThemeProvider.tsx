import React from 'react';
import { createTheme, CssBaseline, ThemeProvider } from '@mui/material';
import darkTheme from '../theme';

function AppThemeProvider({ children }: { children: React.ReactNode }) {


  // @ts-ignore
  const theme = createTheme(darkTheme);

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      {children}
    </ThemeProvider>
  );
}

export default AppThemeProvider;
