import axios from "axios";
import { Message, MessageBox } from "element-ui";
import { getToken, setToken } from "@/utils/auth";
import qs from "qs";

// 创建axios实例

const service = axios.create({
  baseURL:
    process.env.NODE_ENV == "development"
      ? "http://127.0.0.1:5000/api/v1"
      : "http://106.15.225.113:9527/api/v1",
  timeout: 60000, // 请求超时时间
  withCredentials: true,
  headers: {
    "Content-Type": "application/json; charse=UTF-8",
  },
});

// request拦截器
service.interceptors.request.use(
  (config) => {
    var token = getToken();
    if (token != undefined) {
      config.headers["Authorization"] = token; // 让每个请求携带自定义token 请根据实际情况自行修改
    }
    if (config.method == "post" && config.url == "/pdf") {
      config.headers["Content-Type"] = "multipart/form-data";
    } else if (config.method == "post" || config.method == "/put") {
      config.data = qs.stringify(config.data);
      config.headers["Content-Type"] = "application/x-www-form-urlencoded";
    }
    return config;
  },
  (error) => {
    // Do something with request error
    // console.log(error) // for debug
    Promise.reject(error);
  }
);

// respone拦截器
service.interceptors.response.use(
  (response) => {
    /**
     * code为非20000是抛错 可结合自己业务进行修改
     */
    const res = response.data;
    if (res.code !== 0) {
      Message({
        message: res.msg,
        type: "error",
        duration: 5 * 1000,
      });
      return Promise.reject("error");
    } else {
      return response.data;
    }
  },
  (err) => {
    switch (err.response.status) {
      case 400:
        msg = err.response.msg;
        Message({
          message: msg,
          type: "error",
          duration: 5 * 1000,
        });
        break;
      case 401:
        MessageBox.confirm(
          "你已被登出，可以取消继续留在该页面，或者重新登录",
          "确定登出",
          {
            confirmButtonText: "重新登录",
            cancelButtonText: "取消",
            type: "warning",
          }
        ).then(() => {
          window.location = "/auth";
        });
        break;
      case 500:
        Message({
          message: "服务器内部错误，请联系管理员",
          type: "error",
          duration: 5 * 1000,
        });
        break;
      default:
        break;
    }
  }
);
export default service;
