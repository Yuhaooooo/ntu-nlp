import React from 'react';
import { Theme } from '@material-ui/core';
import { makeStyles } from '@material-ui/styles';

const useStyles = makeStyles((theme: Theme) => ({
  toolbar: theme.mixins.toolbar,
}));

const HeaderPlaceHolder = () => {
  const classes = useStyles();
  return <div className={classes.toolbar} />;
};

export default HeaderPlaceHolder;
