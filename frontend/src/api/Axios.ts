import axios, { AxiosInstance } from 'axios';

// Should be used everywhere in the app to make API calls
export const axiosInstance: AxiosInstance = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
});

