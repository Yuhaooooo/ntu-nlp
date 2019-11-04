import { Action } from 'redux';
import {
  ActionReceive,
  ActionReceiveFactory,
  ActionRequestFactory,
  State,
} from '../../constant/lib';

export const REVIEW_REQ = 'REVIEW_REQ';
export const REVIEW_REC = 'REVIEW_REC';

type ReviewReqAction = Action<typeof REVIEW_REQ>;
type ReviewRecSuccessAction = ActionReceive<typeof REVIEW_REC, ReviewRecData>;
type ReviewRecFailureAction = ActionReceive<typeof REVIEW_REC>;

/**
 * Review received data type after json decoder
 */
type ReviewRecData = {
  stars: number;
};

/**
 * Review received json type from server api1
 */
type ReviewRecDataRaw = ReviewRecData;

/**
 * Review request action factory
 */
export type ReviewReqActionFactory = ActionRequestFactory<ReviewReqAction>;

/**
 * Review receive success action factory
 */
export type ReviewRecSuccessActionFactory = ActionReceiveFactory<
  ReviewRecSuccessAction,
  ReviewRecDataRaw
>;

/**
 * NER receive failure action factory
 */
export type ReviewRecFailureActionFactory = ActionReceiveFactory<
  ReviewRecFailureAction
>;

/**
 * Review action type for reducer
 */
export type ReviewActionType =
  | ReviewReqAction
  | ReviewRecSuccessAction
  | ReviewRecFailureAction;

export type TextActionType = ReviewActionType;

/**
 * Review request type for frontend
 */
export interface ReviewReqType {
  sentence: string;
}

/**
 * text state for reducer
 */
export interface TextState {
  text: State<{ stars: number }>;
}
