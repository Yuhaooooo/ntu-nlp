import { Action } from 'redux';
import {
  ActionReceive,
  ActionReceiveFactory,
  ActionRequestFactory,
  State,
} from '../../constant/lib';

export const MICROSERVICE_T_NER_REQ = 'MICROSERVICE_T_NER_REQ';
export const MICROSERVICE_T_NER_REC = 'MICROSERVICE_T_NER_REC';

type MicroserviceTNERReqAction = Action<typeof MICROSERVICE_T_NER_REQ>;
type MicroserviceTNERRecSuccessAction = ActionReceive<
  typeof MICROSERVICE_T_NER_REC,
  MicroserviceTNERRecData
>;
type MicroserviceTNERRecFailureAction = ActionReceive<
  typeof MICROSERVICE_T_NER_REC
>;

/**
 * NER received data type after json decoder
 */
type MicroserviceTNERRecData = string;

/**
 * NER received json type from server api1
 */
type MicroserviceTNERRecDataRaw = MicroserviceTNERRecData;

/**
 * NER request action factory
 */
export type MicroserviceTNERReqActionFactory = ActionRequestFactory<
  MicroserviceTNERReqAction
>;

/**
 * NER receive success action factory
 */
export type MicroserviceTNERRecSuccessActionFactory = ActionReceiveFactory<
  MicroserviceTNERRecSuccessAction,
  MicroserviceTNERRecDataRaw
>;

/**
 * NER receive failure action factory
 */
export type MicroserviceTNERRecFailureActionFactory = ActionReceiveFactory<
  MicroserviceTNERRecFailureAction
>;

/**
 * NER action type for reducer
 */
export type MicroserviceTNERActionType =
  | MicroserviceTNERReqAction
  | MicroserviceTNERRecSuccessAction
  | MicroserviceTNERRecFailureAction;

export type MicroserviceTActionType = MicroserviceTNERActionType;

/**
 * NER request type for frontend
 */
export interface MicroserviceTNERReqType {
  text: string;
}

/**
 * Microservice text state for reducer
 */
export interface MicroserviceTState {
  ner: State<string>;
}
