
import axios from "axios";

axios.defaults.timeout = 100000;
axios.defaults.baseURL = "/studios";

axios.interceptors.request.use(
	(config) => {
		config.data = JSON.stringify(config.data);
		config.headers = {
			"Content-Type": "application/json",
		};
		return config;
	},
	(error) => {
		return Promise.reject(error);
	}
);

axios.interceptors.response.use(
	(response) => {
		return response;
	},
	(error) => {
		console.log("Request Error：", error);
	}
);

export function get(url, params={}) {
	return new Promise((resolve, reject) => {
		axios.get(url, {
			params: params,
		}).then((response) => {
			//  landing(url, params, response.data);
			if (response) {
				resolve(response.data)
			}
		})
			.catch((error) => {
				reject(error);
			});
	});
}


export function post(url, data) {
	return new Promise((resolve, reject) => {
		axios.post(url, data).then(
			(response) => {
				resolve(response.data);
			},
			(err) => {
				reject(err);
			}
		);
	});
}


export function patch(url, data = {}) {
	return new Promise((resolve, reject) => {
		axios.patch(url, data).then(
			(response) => {
				resolve(response.data);
			},
			(err) => {
				msag(err);
				reject(err);
			}
		);
	});
}


export function put(url, data = {}) {
	return new Promise((resolve, reject) => {
		axios.put(url, data).then(
			(response) => {
				resolve(response.data);
			},
			(err) => {
				msag(err);
				reject(err);
			}
		);
	});
}


function msag(err) {
	debugger
	if (err && err.response) {
		switch (err.response.status) {
			case 400:
				alert(err.response.data.error.details);
				break;
			case 401:
				alert("Unauthorized, please log in");
				break;

			case 403:
				alert("Access Denied");
				break;

			case 404:
				alert("Request address error");
				break;

			case 408:
				alert("Request timed out");
				break;

			case 500:
				alert("Internal server error");
				break;

			case 501:
				alert("Service not implemented");
				break;

			case 502:
				alert("Gateway error");
				break;

			case 503:
				alert("Service is not available");
				break;

			case 504:
				alert("Gateway timeout");
				break;

			case 505:
				alert("HTTP version not supported");
				break;
			default:
		}
	}
}

export default function (fecth, url, param) {
	return new Promise((resolve, reject) => {
		switch (fecth) {
			case "get":
				console.log("begin a get request,and url:", url);
				get(url, param)
					.then(function (response) {
						resolve(response);
					})
					.catch(function (error) {
						console.log("get request GET failed.", error);
						reject(error);
					});
				break;
			case "post":
				post(url, param)
					.then(function (response) {
						resolve(response);
					})
					.catch(function (error) {
						console.log("get request POST failed.", error);
						reject(error);
					});
				break;
			default:
				break;
		}
	});
}