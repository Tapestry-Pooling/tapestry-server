import { request } from 'api';

export const getDashboardDataAPI = (authToken, phone) => {
  const options = {
    headers: {
      'X-Auth': authToken,
      'X-Mob': phone,
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
  };
  return request.get('/dashboard', options)
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

export const getCellDataAPI = (authToken, batchSize) => {
  const options = {
    headers: {
      'X-Auth': authToken,
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
  };
  return request.get(`/cell_data/${batchSize}`, options)
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

export const uploadTestDataAPI = (authToken, phone, testId, batch, testData) => {
  const data = {
    test_id: testId,
    batch,
    test_data: testData,
  };
  const options = {
    headers: {
      'X-Auth': authToken,
      'X-Mob': phone,
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
  };
  return request.post('/test_data', data, options)
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

export const getResultAPI = (authToken, phone, testId) => {
  const options = {
    headers: {
      'X-Auth': authToken,
      'X-Mob': phone,
      Accept: 'application/json',
      'Content-Type': 'application/json',
    },
  };
  return request.get(`/results/${testId}`, options)
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
  getDashboardDataAPI,
  getCellDataAPI,
  uploadTestDataAPI,
};
