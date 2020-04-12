import axios from 'axios';

let url = '/api';

if (process.env.APP_ENV !== 'production') {
  url = 'https://c19.zyxw365.in/api';
}

export const BASE_URL = url;

export const request = axios.create({
  baseURL: url,
});

export default {
  BASE_URL,
  request,
};
