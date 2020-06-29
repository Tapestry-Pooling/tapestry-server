import React from 'react';
// import PropTypes from 'prop-types';
import './RequestOTP.scss';

const RequestOTP = (props) => {
  console.log('props: ', props);
  // const { phoneNumber, email, handleRequestOTPInput } = props;
  return (
    <div className="request-otp">
      <div className="request-otp__title">
        Welcome to COVID-19 Testing Kit
      </div>
      {/* <div className="request-otp__input-group">
        <div className="request-otp__input-group-label">
          Phone number for verification
        </div>
        <span className="request-otp__input-group-phone-prepend">+91</span>
        <input type="tel" value={phoneNumber} name="phoneNumber" onChange={handleRequestOTPInput} />
      </div> */}
      <div className="request-otp__input-group">
        {/* <div className="request-otp__input-group-label">
          Email Id to receive results
        </div>
        <input type="text" value={email} name="email" onChange={handleRequestOTPInput} /> */}
        <div id="my-signIn" />
      </div>
    </div>
  );
};

RequestOTP.propTypes = {
  // phoneNumber: PropTypes.string,
  // email: PropTypes.string,
  // handleRequestOTPInput: PropTypes.func.isRequired,
};

RequestOTP.defaultProps = {
  phoneNumber: '',
  email: '',
};

export default RequestOTP;
