import React from 'react';
import { Card, Grid, Theme } from '@material-ui/core';
import { makeStyles } from '@material-ui/styles';
import TextInput from './container/TextInputContainer';
import HighlightText from './container/HighlightTextContainer';

const useStyles = makeStyles((theme: Theme) => ({
  separator: {
    borderRight: `${theme.palette.common.white} solid 2px`,
  },
  root: {
    margin: 'auto',
    backgroundColor: theme.palette.grey[100],
  },
}));

const NERPanel = () => {
  const classes = useStyles();

  return (
    <Card className={classes.root} elevation={0}>
      <Grid direction='row' container>
        <Grid className={classes.separator} xs={12} md={6} item>
          <TextInput />
        </Grid>
        <Grid xs={12} md={6} item>
          <HighlightText />
        </Grid>
      </Grid>
    </Card>
  );
};

export default NERPanel;
