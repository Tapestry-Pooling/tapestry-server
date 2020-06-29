import React from 'react';
import PropTypes from 'prop-types';
import './UploadTestResult.scss';

const UploadTestResult = (props) => {
  console.log('props: ', props);
  const { result } = props;
  return (
    <div className="upload-test-result">
      <div dangerouslySetInnerHTML={{ __html: result.replace(/[\n\r]/g, '<div class="upload-test-result-break"></div>') }} />
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
