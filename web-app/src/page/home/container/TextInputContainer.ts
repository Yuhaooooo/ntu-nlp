import { connect } from 'react-redux';
import _ from 'lodash';
import { ThunkDispatch } from 'redux-thunk';
import { AppState } from '../../../store';
import TextInput from '../component/TextInput';
import { MicroserviceTActionType } from '../../../store/text/type';
import microserviceTNERPredict from '../../../store/text/action/post';

const mapDispatchToProps = (
  dispatch: ThunkDispatch<AppState, {}, MicroserviceTActionType>,
) => ({
  analyze: _.flow([microserviceTNERPredict, dispatch]),
});

export default connect(
  null,
  mapDispatchToProps,
)(TextInput);
