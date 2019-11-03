import React, { useCallback, useEffect, useState } from 'react';
import {
  Box,
  Button,
  Container,
  Grid,
  Hidden,
  Theme,
  Typography,
} from '@material-ui/core';
import { makeStyles } from '@material-ui/styles';
import HeaderPlaceHolder from '../../common/HeaderPlaceHolader';
import { setTitleEffectFactory } from '../../utils/utils';
import Sidebar from '../../common/Sidebar';
import NERPanel from './NERPanel';

const useStyles = makeStyles((theme: Theme) => ({
  container: {
    marginTop: 48,
  },
  button: {
    margin: theme.spacing(1, 0),
  },
}));

const sidebarItemDict = {
  Review: '',
};

const MicroserviceApp: React.FC = () => {
  useEffect(setTitleEffectFactory('Review prediction Testbed'), []);
  const classes = useStyles();
  const [mobileOpen, setMobileOpen] = useState(false);
  const handleDrawerToggle = useCallback(() => setMobileOpen(!mobileOpen), [
    mobileOpen,
  ]);
  return (
    <>
      <HeaderPlaceHolder />
      <Box display='flex'>
        <Sidebar
          itemDict={sidebarItemDict}
          handleDrawerToggle={handleDrawerToggle}
          mobileOpen={mobileOpen}
        />
        <Container className={classes.container} maxWidth='lg'>
          <Grid justify='center' container>
            <Grid item>
              <Typography variant='h3' gutterBottom>
                Review Classification Testbed
              </Typography>
            </Grid>
          </Grid>
          <Hidden smUp>
            <Button
              size='small'
              color='primary'
              className={classes.button}
              onClick={handleDrawerToggle}
            >
              Select models
            </Button>
          </Hidden>
          <NERPanel />
        </Container>
      </Box>
    </>
  );
};

export default MicroserviceApp;
