import {
  MICROSERVICE_T_NER_REC,
  MICROSERVICE_T_NER_REQ,
  MicroserviceTActionType,
  MicroserviceTState,
} from './type';
import asyncReducer from '../../utils/reducer';

export const initState: MicroserviceTState = {
  ner: {
    state: 'INIT',
    timestamp: Date.now(),
    message: '',
    statusCode: 0,
    data: '',
  },
};

export default function reducer(
  state = initState,
  action: MicroserviceTActionType,
): MicroserviceTState {
  switch (action.type) {
    case 'MICROSERVICE_T_NER_REQ':
    case 'MICROSERVICE_T_NER_REC':
      return {
        ...state,
        ner: asyncReducer(
          state.ner,
          action,
          {
            request: MICROSERVICE_T_NER_REQ,
            receive: MICROSERVICE_T_NER_REC,
          },
          x => x,
        ),
      };
    default:
      return { ...state };
  }
}
