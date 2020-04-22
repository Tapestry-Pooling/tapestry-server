import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';
import './UploadTestLandingPage.scss';

const CTCard = (props) => {
  const {
    label, test_start_time: testStartTime, test_end_time: testEndTime,
    batch, results_available: resultsAvailable,
    test_id: testId,
  } = props;

  const zeroPadding = (number) => {
    const numberString = number.toString();
    if (numberString.length < 2) {
      return `0${numberString}`;
    }
    return numberString;
  };

  const getFormattedDate = (dateString) => {
    console.log('dateString: ', dateString);
    const dateObj = new Date(dateString);
    const hours = dateObj.getHours();
    const minutes = dateObj.getMinutes();
    const seconds = dateObj.getSeconds();
    return `${dateObj.toDateString()}, ${((hours === 0 || hours > 12)
      ? zeroPadding(Math.abs(hours - 12))
      : zeroPadding(hours))}:${zeroPadding(minutes)}:${zeroPadding(seconds)} ${(hours > 12) ? 'PM' : 'AM'}`;
  };

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
          Start Time:
        </div>
        <div className="ct-card-value">
          {getFormattedDate(testStartTime)}
        </div>
      </div>
      <div>
        <div className="ct-card-label">
          End Time:
        </div>
        <div className="ct-card-value">
          {getFormattedDate(testEndTime)}
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
  test_start_time: PropTypes.string,
  test_end_time: PropTypes.string,
  results_available: PropTypes.bool,
  batch: PropTypes.string,
};

CTCard.defaultProps = {
  test_id: 0,
  label: '',
  test_start_time: '',
  test_end_time: '',
  results_available: false,
  batch: '',
};

const UploadTestLandingPage = (props) => {
  console.log('props: ', props);
  const { testsData } = props;
  return (
    <div className="upload-test-landing-page">
      {testsData.map((data) => (<CTCard key={data.test_id} {...data} />))}
      {testsData.length === 0
        ? <div className="upload-test-landing-page-empty">No tests done yet</div>
        : ''}
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
