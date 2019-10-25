import { connect } from 'react-redux';
import { AppState } from '../../../store';
import HighlightText from '../component/HighlightText';

const mapStateToProps = (state: AppState) => ({
  text: state.text.ner.data,
});

export default connect(mapStateToProps)(HighlightText);
