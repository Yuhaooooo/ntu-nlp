import { Action } from 'redux';
import { ActionReceive, State } from '../constant/lib';

function asyncReducer<T, D, Q, R>(
  state: State<D>,
  action: Action<Q> | ActionReceive<R, T>,
  {
    request,
    receive,
  }: {
    request: Q;
    receive: R;
  },
  mapping?: (actionData: T) => D,
): State<D> {
  switch (action.type) {
    case request:
      return {
        ...state,
        state: 'REQUEST',
      };
    case receive:
      if ((action as ActionReceive).status === 'SUCCESS')
        return {
          ...state,
          state: 'SUCCESS',
          data: mapping
            ? mapping((action as ActionReceive).data)
            : (action as ActionReceive).data,
        };
      return {
        ...state,
        state: 'FAILURE',
        message: (action as ActionReceive).message,
        statusCode: (action as ActionReceive).statusCode,
      };
    default:
      return { ...state };
  }
}

export default asyncReducer;
