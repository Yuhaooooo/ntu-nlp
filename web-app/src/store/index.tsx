import { applyMiddleware, combineReducers, createStore } from 'redux';
import thunk from 'redux-thunk';
import text from './text/reducer';

const rootReducer = combineReducers({ text });

export type AppState = ReturnType<typeof rootReducer>;

const store = createStore(rootReducer, applyMiddleware(thunk));

export default store;
