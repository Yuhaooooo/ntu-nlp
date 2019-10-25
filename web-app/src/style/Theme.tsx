import React from 'react';
import { createMuiTheme } from '@material-ui/core/styles';
import { ThemeProvider } from '@material-ui/styles';

const theme = createMuiTheme({
  mixins: {
    toolbar: {
      minHeight: 48,
      '@media (min-width:0px) and (orientation: landscape)': {
        minHeight: 36,
      },
      '@media (min-width:600px)': {
        minHeight: 56,
      },
    },
  },
  palette: {
    primary: { main: '#33ACFF', contrastText: '#f9f9f9' },
    secondary: { main: '#66EFEF', contrastText: '#363D4E' },
    error: { main: '#F4606C' },
  },
  shape: {
    borderRadius: 8,
  },
  overrides: {
    MuiButton: {
      root: {
        borderRadius: 4,
      },
    },
  },
});

export interface Props {
  children: React.ReactElement;
}

const Theme = ({ children }: Props) => (
  <ThemeProvider theme={theme}>{children}</ThemeProvider>
);

export default Theme;
