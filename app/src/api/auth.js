import { request } from 'api';

export const requestOTPAPI = (phone) => {
  const data = {
    phone,
  };
  const options = {
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
  };
  return request.post('/request_otp', data, options)
    .then((response) => {
      if (response.status === 200) {
        console.log('response data: ', response.data);
      }
      return response;
    }, (err) => (err.response))
    .catch((err) => {
      console.log('Caught in api chain: ', err.message);
    });
};

export const verifyOTPAPI = (phone, otp) => {
  const data = {
    phone,
    otp,
  };
  const options = {
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
  };
  return request.post('/validate_otp', data, options)
    .then((response) => {
      if (response.status === 200) {
        console.log('response data: ', response.data);
      }
      return response;
    }, (err) => (err.response))
    .catch((err) => {
      console.log('Caught in api chain: ', err.message);
    });
};

export default {
  requestOTPAPI,
  verifyOTPAPI,
};
