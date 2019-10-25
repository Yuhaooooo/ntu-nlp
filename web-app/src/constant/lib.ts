import { Action } from 'redux';
import { ThunkAction } from 'redux-thunk';
import { JsonResponse } from '../utils/type';

/* Standard returned state from redux */
export interface State<D = any> {
  state: 'INIT' | 'REQUEST' | 'SUCCESS' | 'FAILURE';
  timestamp: number;
  message: string;
  statusCode: number;
  data: D;
}

export interface ActionReceive<T = any, D = any> extends Action<T> {
  status: StatusType;
  data: D;
  message: string;
  statusCode: number;
  timestamp: number;
}

export type ActionRequestFactory<A extends Action, P = any> = (props: P) => A;

export type ActionReceiveFactory<A extends ActionReceive<any, any>, J = any> = (
  json: JsonResponse<J>,
) => A;

export type AsyncActionFactory<
  P extends {} = {},
  S extends {} = {},
  A extends Action<any> = Action<any>
> = (props: P, callback?: () => void) => ThunkAction<any, S, null, A>;

export const SUCCESS = 'SUCCESS';
export const FAILURE = 'FAILURE';

export type StatusType = typeof SUCCESS | typeof FAILURE;
