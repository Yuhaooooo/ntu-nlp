import React, { ReactNode } from 'react';
import { Theme } from '@material-ui/core/styles';
import classNames from 'classnames';
import { Link as RRLink } from 'react-router-dom';
import { createStyles, WithStyles, withStyles } from '@material-ui/styles';

const styles = ({ transitions }: Theme) =>
  createStyles({
    root: {
      cursor: 'pointer',
    },
    aUnderline: {
      '&:hover': {
        textDecoration: 'underline',
      },
    },
    aResponsive: {
      opacity: 0.7,
      transition: transitions.create('opacity', {
        duration: transitions.duration.complex,
        delay: 0.05,
        easing: transitions.easing.sharp,
      }),
      '&:hover': {
        opacity: 1,
      },
    },
  });

export interface Props extends WithStyles<typeof styles> {
  className?: string;
  children: ReactNode;
  to: string;
  paragraph?: boolean;
  animation?: boolean;
}

const Link = withStyles(styles)(
  ({
    classes,
    className,
    children,
    to,
    paragraph = false,
    animation = true,
  }: Props) => {
    const Link2 = ({
      children: children2,
      className: className2,
    }: {
      children: ReactNode;
      className?: string;
    }) =>
      to.startsWith('http://') || to.startsWith('https://') ? (
        <a className={className2} href={to}>
          {children2}
        </a>
      ) : (
        <RRLink className={className2} to={to}>
          {children2}
        </RRLink>
      );

    return (
      <Link2
        className={classNames(className, classes.root, {
          [classes.aUnderline]: paragraph,
          [classes.aResponsive]: !paragraph && animation,
        })}
      >
        {children}
      </Link2>
    );
  },
);

export default Link;
