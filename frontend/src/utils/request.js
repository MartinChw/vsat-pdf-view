import axios from "axios";
import { Message, MessageBox } from "element-ui";
import { getToken, setToken } from "@/utils/auth";
import qs from "qs";

// 创建axios实例

const service = axios.create({
  baseURL:
    process.env.NODE_ENV == "development"
      ? "http://106.15.225.113:9527/api/v1"
      : "http://106.15.225.113:9527/api/v1",
  timeout: 15000, // 请求超时时间
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

      // 10005:Token 过期了;
      if (res.code === 10005) {
        MessageBox.confirm(
          "你已被登出，可以取消继续留在该页面，或者重新登录",
          "确定登出",
          {
            confirmButtonText: "重新登录",
            cancelButtonText: "取消",
            type: "warning",
          }
        ).then(() => {
          location.reload(); // 为了重新实例化vue-router对象 避免bug
          this.$router.push({ path: "/login" });
        });
      }
      // if (res.code === 10004 ) {
      //   location.href = "/login"
      // }
      return Promise.reject("error");
    } else {
      // if (response.headers["token-refresh"]) {
      //   setToken(response.headers["token-refresh"]);
      // }

      return response.data;
    }
  },
  (error) => {
    console.log("err" + error); // for debug
    Message({
      message: error.message,
      type: "error",
      duration: 5 * 1000,
    });
    return Promise.reject(error);
  }
);
export default service;
