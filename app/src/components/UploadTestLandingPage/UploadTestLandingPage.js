import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';
import './UploadTestLandingPage.scss';

const CTCard = (props) => {
  const {
    label, duration_minutes: durationMinutes, batch, results_available: resultsAvailable,
    test_id: testId,
  } = props;
  return (
    <div className="ct-card">
      <div>
        <div className="ct-card-label">
          Test Name:
        </div>
        <div className="ct-card-value">
          {label}
        </div>
      </div>
      <div>
        <div className="ct-card-label">
          Duration:
        </div>
        <div className="ct-card-value">
          {durationMinutes}
          {' minutes'}
        </div>
      </div>
      <div>
        <div className="ct-card-label">
          Size:
        </div>
        <div className="ct-card-value">
          {batch}
        </div>
      </div>
      {resultsAvailable
        ? (
          <div className="ct-card-update-ct-values-buttons">
            <Link to={`/app/upload-test/form?testId=${testId}`}><button type="button">Update Ct Values</button></Link>
            <Link to={`/app/upload-test/result?testId=${testId}`}><button type="button">View Last Result</button></Link>
          </div>
        )
        : (
          <div className="ct-card-input-ct-values-button">
            <Link to={`/app/upload-test/form?testId=${testId}`}><button type="button">Input Ct Values</button></Link>
          </div>
        )}
    </div>
  );
};

CTCard.propTypes = {
  test_id: PropTypes.number,
  label: PropTypes.string,
  duration_minutes: PropTypes.number,
  results_available: PropTypes.bool,
  batch: PropTypes.string,
};

CTCard.defaultProps = {
  test_id: 0,
  label: '',
  duration_minutes: '',
  results_available: false,
  batch: '',
};

const UploadTestLandingPage = (props) => {
  console.log('props: ', props);
  const { testsData } = props;
  return (
    <div className="upload-test-landing-page">
      {testsData.map((data) => (<CTCard key={data.test_id} {...data} />))}
    </div>
  );
};

UploadTestLandingPage.propTypes = {
  testsData: PropTypes.arrayOf(PropTypes.shape({})),
};

UploadTestLandingPage.defaultProps = {
  testsData: [],
};

export default UploadTestLandingPage;
