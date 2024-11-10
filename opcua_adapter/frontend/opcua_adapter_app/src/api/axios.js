// src/api/axios.js
import axios from 'axios';

const service = axios.create({
  baseURL: 'http://127.0.0.1:5003/opcua', // 基础 URL
  timeout: 50000, // 请求超时时间
});

// 请求拦截器
service.interceptors.request.use(
  (config) => {
    // 可以在这里添加 token
    config.headers['Content-Type'] = 'application/json'; // 设置内容类型
    config.headers['Accept'] = 'application/json'; // 设置接受类型

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
service.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default service;
