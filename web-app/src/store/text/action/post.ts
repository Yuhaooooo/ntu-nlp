import {
  MICROSERVICE_T_NER_REC,
  MICROSERVICE_T_NER_REQ,
  MicroserviceTNERRecFailureActionFactory,
  MicroserviceTNERRecSuccessActionFactory,
  MicroserviceTNERReqActionFactory,
  MicroserviceTNERReqType,
} from '../type';
import { AsyncActionFactory } from '../../../constant/lib';
import { xmlHttpRequest } from '../../../utils/httpRequest';
import { api_host as apiHost, api_port as apiPort } from '../../../config';

const requestPost: MicroserviceTNERReqActionFactory = () => ({
  type: MICROSERVICE_T_NER_REQ,
});

const receivePostSuccess: MicroserviceTNERRecSuccessActionFactory = json => ({
  type: MICROSERVICE_T_NER_REC,
  status: 'SUCCESS',
  data: json.data,
  message: '',
  statusCode: 200,
  timestamp: json.timestamp,
});

const receivePostFailure: MicroserviceTNERRecFailureActionFactory = json => ({
  type: MICROSERVICE_T_NER_REC,
  status: 'FAILURE',
  data: undefined,
  message: json.message,
  statusCode: json.statusCode,
  timestamp: json.timestamp,
});

const microserviceTNERPredict: AsyncActionFactory<
  MicroserviceTNERReqType
> = props => dispatch => {
  const { text } = props as MicroserviceTNERReqType;

  const formData = new FormData();
  formData.append('text', text);
  return xmlHttpRequest(dispatch, 'POST', {
    url: `${apiHost}:${apiPort}/app/text/ner`,
    request: requestPost,
    receiveSuccess: receivePostSuccess,
    receiveFailure: receivePostFailure,
    formData,
  }) as XMLHttpRequest;
};

export default microserviceTNERPredict;
