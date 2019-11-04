import React from 'react';
import { create } from 'jss';
import {
  createGenerateClassName,
  jssPreset,
  StylesProvider,
} from '@material-ui/styles';
import Theme from './Theme';
import GlobalClasses from './GlobalClasses';

const generateClassName = createGenerateClassName({
  productionPrefix: 'reactkit',
});

const jss = create({
  ...jssPreset(),
  insertionPoint: 'jss-insertion-point',
});

export interface Props {
  children: React.ReactElement;
}

const JssRegistry = ({ children }: Props) => {
  return (
    <StylesProvider jss={jss} generateClassName={generateClassName}>
      <Theme>
        <GlobalClasses>{children}</GlobalClasses>
      </Theme>
    </StylesProvider>
  );
};

export default JssRegistry;
