import * as React from 'react';
import withStyles from '@material-ui/core/styles/withStyles';
import createStyles from '@material-ui/core/styles/createStyles';
import { Theme } from '@material-ui/core';

const globalStyles = (theme: Theme) =>
  createStyles({
    '@global': {
      '.navItem': {
        '&:after': {
          content: '""',
          position: 'absolute',
          bottom: 0,
          left: `calc(50% - ${theme.spacing(2)}px)`,
          width: theme.spacing(4),
          transition: theme.transitions.create('border-bottom-width'),
          borderBottom: `${theme.palette.primary.main} solid`,
          borderBottomWidth: 0,
        },
        '&:hover:after': {
          borderBottomWidth: theme.spacing(0.5),
        },
      },
      '.navItem-highlight': {
        '&:after': {
          borderBottomWidth: theme.spacing(0.5),
        },
      },
    },
  });

const GlobalClasses = ({ children }: { children: React.ReactNode }) => (
  <>{children}</>
);

export default withStyles(globalStyles)(GlobalClasses);
