import request from "@/utils/request";

export function listPdf(param) {
  return request({
    url: "/pdf",
    method: "get",
    params: param,
  });
}

export function getPdf(param) {
  return request({
    url: "/pdf/item",
    method: "get",
    params: param,
  });
}

export function createPdf(data) {
  return request({
    url: "/pdf",
    method: "post",
    data,
  });
}
