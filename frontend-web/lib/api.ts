import axios from "axios";

export const api = axios.create({
  baseURL: "http://localhost:8000", // لاحقًا Cloud Run URL
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("demo_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
