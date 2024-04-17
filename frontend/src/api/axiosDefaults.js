import axios from "axios";

axios.defaults.headers.post["content-type"] = "multipart/form-data";
axios.defaults.withCredentials = true;

export const axiosRec = axios.create();
export const axiosRes = axios.create();