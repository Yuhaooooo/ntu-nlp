import * as React from 'react';
import { Route, Router, Switch } from 'react-router-dom';
import { createBrowserHistory } from 'history';
import { createStyles, WithStyles, withStyles } from '@material-ui/styles';
import { Theme } from '@material-ui/core';
import Header from './common/Header';
import Swagger from './page/doc/Swagger';
import Home from './page/home';

const history = createBrowserHistory();

const styles = (theme: Theme) =>
  createStyles({
    root: {
      display: 'flex',
      flexDirection: 'column',
      minHeight: '100%',
    },
    content: {
      flexGrow: 1,
      backgroundColor: theme.palette.background.default,
      minWidth: 0,
      minHeight: '100%',
      position: 'relative',
    },
  });

interface Props extends WithStyles<typeof styles> {}

const RootRouter = withStyles(styles)(({ classes }: Props) => (
  <Router history={history}>
    <React.Fragment>
      <Header />
      <main id='app-main' className={classes.content}>
        <Switch>
          <Route path='/' exact component={Home} />
          <Route path='/doc' component={Swagger} />
        </Switch>
      </main>
      <div id='footer-container' />
    </React.Fragment>
  </Router>
));

export default RootRouter;
