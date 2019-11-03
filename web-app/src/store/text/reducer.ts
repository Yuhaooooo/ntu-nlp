import { REVIEW_REC, REVIEW_REQ, TextActionType, TextState } from './type';
import asyncReducer from '../../utils/reducer';

export const initState: TextState = {
  text: {
    state: 'INIT',
    timestamp: Date.now(),
    message: '',
    statusCode: 0,
    data: { stars: -1 },
  },
};

export default function reducer(
  state = initState,
  action: TextActionType,
): TextState {
  switch (action.type) {
    case 'REVIEW_REC':
    case 'REVIEW_REQ':
      return {
        ...state,
        text: asyncReducer(
          state.text,
          action,
          {
            request: REVIEW_REQ,
            receive: REVIEW_REC,
          },
          x => x,
        ),
      };
    default:
      return { ...state };
  }
}
