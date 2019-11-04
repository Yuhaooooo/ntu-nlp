import React from 'react';
import {
  Drawer,
  Hidden,
  List,
  ListItem,
  ListItemText,
  Theme,
} from '@material-ui/core';
import { makeStyles, useTheme } from '@material-ui/styles';
import _ from 'lodash';
import { Link } from 'react-router-dom';
import HeaderPlaceHolder from './HeaderPlaceHolader';

const useStyles = makeStyles((theme: Theme) => ({
  drawer: {
    [theme.breakpoints.up('sm')]: {
      width: 240,
      flexShrink: 0,
    },
  },
  drawerPaper: {
    width: 240,
  },
  listItemTextPrimary: {
    fontWeight: 500,
    lineHeight: 1.75,
  },
}));

interface SidebarProps {
  itemDict: { [text: string]: string };
  mobileOpen?: boolean;
  handleDrawerToggle?: (e: React.MouseEvent<HTMLElement>) => void;
}

const Sidebar = ({
  itemDict,
  mobileOpen = false,
  handleDrawerToggle = undefined,
}: SidebarProps) => {
  const classes = useStyles();
  const theme = useTheme<Theme>();
  const currentPath = window.location.pathname;

  const handleCloseDrawerTrigger = (e: React.MouseEvent<HTMLElement>) => {
    if (mobileOpen && handleDrawerToggle) handleDrawerToggle(e);
  };
  const drawer = (
    <div>
      <HeaderPlaceHolder />
      <List onClick={handleCloseDrawerTrigger}>
        {_.keys(itemDict).map(text => (
          <ListItem
            button
            component={Link}
            to={itemDict[text]}
            selected={itemDict[text] === currentPath}
            key={text}
          >
            <ListItemText
              classes={{ primary: classes.listItemTextPrimary }}
              primary={text}
              primaryTypographyProps={{ variant: 'body2' }}
            />
          </ListItem>
        ))}
      </List>
    </div>
  );

  return (
    <nav className={classes.drawer}>
      <Hidden xsDown>
        <Drawer
          variant='permanent'
          classes={{
            paper: classes.drawerPaper,
          }}
          open
        >
          {drawer}
        </Drawer>
      </Hidden>
      <Hidden smUp>
        <Drawer
          variant='temporary'
          anchor={theme.direction === 'rtl' ? 'right' : 'left'}
          open={mobileOpen}
          onClose={handleDrawerToggle}
          classes={{
            paper: classes.drawerPaper,
          }}
          ModalProps={{
            keepMounted: true, // Better open performance on mobile.
          }}
        >
          {drawer}
        </Drawer>
      </Hidden>
    </nav>
  );
};

export default Sidebar;
