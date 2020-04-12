import React from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom';
import './VerifyOTP.scss';

const VerifyOTP = (props) => {
  console.log('props: ', props);
  const { phoneNumber, otp, handleVerifyOTPInput } = props;
  return (
    <div className="verify-otp">
      <div className="verify-otp__title">
        Please Enter OTP
      </div>
      <div className="verify-otp__input-group">
        <div className="verify-otp__input-group-label">
          SMS sent to +91
          {' '}
          {phoneNumber}
          {' '}
          <Link to="/login">Edit</Link>
        </div>
        <span className="verify-otp__input-group-otp-hide" />
        <input type="text" value={otp} onChange={handleVerifyOTPInput} />
        <div className="verify-otp__input-group-description">
          You will receive OTP in
          {' '}
          <b>20</b>
          {' '}
          seconds
        </div>
      </div>
    </div>
  );
};

VerifyOTP.propTypes = {
  phoneNumber: PropTypes.string,
  otp: PropTypes.string,
  handleVerifyOTPInput: PropTypes.func.isRequired,
};

VerifyOTP.defaultProps = {
  phoneNumber: '',
  otp: '',
};

export default VerifyOTP;
