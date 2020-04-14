import React from 'react';
import PropTypes from 'prop-types';
import './UploadTestResult.scss';

const UploadTestResult = (props) => {
  console.log('props: ', props);
  const { result } = props;
  return (
    <div className="upload-test-result">
      {result}
    </div>
  );
};

UploadTestResult.propTypes = {
  result: PropTypes.string,
};

UploadTestResult.defaultProps = {
  result: '',
};

export default UploadTestResult;
