import React from 'react';
import { Card, Theme } from '@material-ui/core';
import { makeStyles } from '@material-ui/styles';
import TextInput from './container/TextInputContainer';
import ReviewResult from './container/StarResultContainer';

const useStyles = makeStyles((theme: Theme) => ({
  root: {
    margin: 'auto',
    backgroundColor: theme.palette.grey[100],
  },
}));

const NERPanel = () => {
  const classes = useStyles();

  return (
    <Card className={classes.root} elevation={0}>
      <TextInput />
      <ReviewResult />
    </Card>
  );
};

export default NERPanel;
