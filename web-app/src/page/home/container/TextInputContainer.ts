import { connect } from 'react-redux';
import _ from 'lodash';
import { ThunkDispatch } from 'redux-thunk';
import { AppState } from '../../../store';
import TextInput from '../component/TextInput';
import { TextActionType } from '../../../store/text/type';
import ReviewPredict from '../../../store/text/action/post';

const mapDispatchToProps = (
  dispatch: ThunkDispatch<AppState, {}, TextActionType>,
) => ({
  analyze: _.flow([ReviewPredict, dispatch]),
});

export default connect(
  null,
  mapDispatchToProps,
)(TextInput);
