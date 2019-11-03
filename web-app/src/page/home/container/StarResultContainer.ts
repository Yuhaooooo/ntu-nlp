import { connect } from 'react-redux';
import { AppState } from '../../../store';
import StarResult from '../component/StarResult';

const mapStateToProps = (state: AppState) => ({
  stars: state.text.text.data.stars,
});

export default connect(mapStateToProps)(StarResult);
