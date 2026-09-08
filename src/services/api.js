import axios from "axios";

const API_URL = (import.meta.env.VITE_API_URL || "").replace(/\/$/, "");
if (!API_URL) console.warn("VITE_API_URL is not set. Configure it in Vercel Project Settings.");

const api = axios.create({ baseURL: API_URL || "/api", timeout: 60000 });
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("learnify_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});
api.interceptors.response.use((response) => response, (error) => {
  error.friendlyMessage = !error.response
    ? "Can't reach the Learnify AI server. Check VITE_API_URL and that the backend is online."
    : error.response.data?.message || "Something went wrong. Please try again.";
  return Promise.reject(error);
});
export default api;
