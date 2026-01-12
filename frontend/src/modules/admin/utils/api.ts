export const getApiBase = () => import.meta.env.VITE_API_URL || "/api";

export const getAuthHeaders = () => ({
  "Content-Type": "application/json",
  Authorization: `Bearer ${localStorage.getItem("admin_token") || ""}`,
});
