import React, { useCallback, useState } from 'react';
import {
  AppBar,
  Container,
  Hidden,
  IconButton,
  makeStyles,
  Theme,
  Toolbar,
  Typography,
} from '@material-ui/core';
import { RouteComponentProps, withRouter } from 'react-router-dom';
import classNames from 'classnames';
import Box from '@material-ui/core/Box';
import MenuIcon from '@material-ui/icons/Menu';
import _ from 'lodash';
import Link from './Link';
import Sidebar from './Sidebar';

const useStyles = makeStyles((theme: Theme) => ({
  root: {
    zIndex: theme.zIndex.drawer + 1,
    width: '100%',
    backgroundColor: theme.palette.background.paper,
    color: theme.palette.text.secondary,
  },
  logo: {
    margin: theme.spacing(0, 1.5),
  },
  img: {
    height: 36,
    '@media (max-width: 840px)': {
      height: 0,
    },
  },
  headerItemContainer: {
    marginLeft: 36,
    '&:first-child': {
      marginLeft: 'unset',
    },
  },
  headerItem: {
    display: 'block',
    lineHeight: '56px',
    position: 'relative',
  },
}));

interface HeaderItem {
  [text: string]: string;
}

const headerItem: HeaderItem = {
  'API test': '/doc',
};

const Header = ({ location }: RouteComponentProps) => {
  const [mobileOpen, setMobileOpen] = useState(false);
  const handleDrawerToggle = useCallback(() => setMobileOpen(!mobileOpen), [
    mobileOpen,
  ]);
  const path = `/${location.pathname.split('/')[1]}`;
  const classes = useStyles();

  const content = _.keys(headerItem).map(text => (
    <Typography
      key={text}
      className={classes.headerItemContainer}
      variant='body2'
      color='textPrimary'
    >
      <Link
        aira-label={text}
        className={classNames(classes.headerItem, 'navItem', {
          'navItem-highlight': headerItem[text] === path,
        })}
        to={headerItem[text]}
        animation={headerItem[text] !== path}
      >
        {text}
      </Link>
    </Typography>
  ));

  return (
    <AppBar className={classes.root} position='fixed'>
      <Toolbar component={Container}>
        <Hidden smUp>
          <IconButton
            edge='start'
            color='inherit'
            aria-label='menu'
            onClick={handleDrawerToggle}
          >
            <MenuIcon />
          </IconButton>
        </Hidden>
        <Hidden xsDown>
          <Link
            className={classes.logo}
            aira-label='Home'
            to='/'
            animation={false}
          >
            <Typography color='primary' variant='h6' noWrap>
              Home
            </Typography>
          </Link>
          {content}
        </Hidden>
        <Hidden smUp>
          <Sidebar
            itemDict={headerItem}
            mobileOpen={mobileOpen}
            handleDrawerToggle={handleDrawerToggle}
          />
        </Hidden>
        <Box flexGrow={1} />
      </Toolbar>
    </AppBar>
  );
};

export default withRouter(Header);
