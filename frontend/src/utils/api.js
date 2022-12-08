
import http from './requests';

export function getArticleList (params) {
  return new Promise((resolve, reject) => {
    http('get', '/distance', params)
        .then(res => {
            resolve (res);
        },
        error => {
            console.log("Internet Error",error);
            reject(error)
        })
  }) 
}

export function getQueryList (params) {
  return new Promise((resolve, reject) => {
    http('get', '/query', params)
        .then(res => {
            resolve (res);
        },
        error => {
            console.log("Internet Error",error);
            reject(error)
        })
  }) 
}

export function getClassDetail (params) {
  return new Promise((resolve, reject) => {
    http('get', '/get_classes', params)
        .then(res => {
            resolve (res);
        },
        error => {
            console.log("Internet Error",error);
            reject(error)
        })
  }) 
}

export function getDistance (params) {
  return new Promise((resolve, reject) => {
    http('get', '/cal_distance', params)
        .then(res => {
            resolve (res);
        },
        error => {
            console.log("Internet Error",error);
            reject(error)
        })
  }) 
}