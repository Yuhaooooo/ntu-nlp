import {
  REVIEW_REC,
  REVIEW_REQ,
  ReviewRecFailureActionFactory,
  ReviewRecSuccessActionFactory,
  ReviewReqActionFactory,
  ReviewReqType,
} from '../type';
import { AsyncActionFactory } from '../../../constant/lib';
import { xmlHttpRequest } from '../../../utils/httpRequest';
import { api_host as apiHost, api_port as apiPort } from '../../../config';

const requestPost: ReviewReqActionFactory = () => ({
  type: REVIEW_REQ,
});

const receivePostSuccess: ReviewRecSuccessActionFactory = json => ({
  type: REVIEW_REC,
  status: 'SUCCESS',
  data: json.data,
  message: '',
  statusCode: 200,
  timestamp: json.timestamp,
});

const receivePostFailure: ReviewRecFailureActionFactory = json => ({
  type: REVIEW_REC,
  status: 'FAILURE',
  data: undefined,
  message: json.message,
  statusCode: json.statusCode,
  timestamp: json.timestamp,
});

const ReviewPredict: AsyncActionFactory<ReviewReqType> = props => dispatch => {
  const { sentence } = props as ReviewReqType;

  const formData = new FormData();
  formData.append('sentence', sentence);
  return xmlHttpRequest(dispatch, 'POST', {
    url: `${apiHost}:${apiPort}/review/predict`,
    request: requestPost,
    receiveSuccess: receivePostSuccess,
    receiveFailure: receivePostFailure,
    formData,
  }) as XMLHttpRequest;
};

export default ReviewPredict;
