import React from 'react';
import { Provider } from 'react-redux';
import store from './store';
import JssRegistry from './style/JssRegistry';
import RootRouter from './RootRouter';

const App: React.FC = () => {
  return (
    <JssRegistry>
      <Provider store={store}>
        <RootRouter />
      </Provider>
    </JssRegistry>
  );
};

export default App;
