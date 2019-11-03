import { Action } from 'redux';
import { ActionReceive, ActionReceiveFactory } from '../constant/lib';

export interface XMLParameter<D = any, J = any> {
  url: string;
  jsonDecoder?: JsonDecoder<J, D>;
  request: (...args: any[]) => Action;
  receiveSuccess: ActionReceiveFactory<ActionReceive<D>, J>;
  receiveFailure: ActionReceiveFactory<any, never>;
  formData?: FormData;
  headers?: { [propName: string]: string };
}

export type HttpMethod = 'GET' | 'POST' | 'PATCH' | 'DELETE';

export interface JsonResponse<D = never> {
  data: D;
  timestamp: number;
  message: string;
  statusCode: number;
}

export type JsonDecoder<T extends Object, D extends Object> = (jsonIn: T) => D;
