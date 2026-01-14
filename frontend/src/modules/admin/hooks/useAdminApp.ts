// Admin App Hook - 管理认证状态和初始化
import { useEffect, useCallback } from "react";
import { useAdminAuthStore } from "@/common/stores";
import { adminAppService } from "../services/app.service";

const ADMIN_TOKEN_KEY = "admin_token";
const ADMIN_REFRESH_TOKEN_KEY = "admin_refresh_token";

export function useAdminApp() {
  const { admin, isAuthenticated, isLoading, login, logout, setLoading } =
    useAdminAuthStore();

  useEffect(() => {
    const initAuth = async () => {
      const token = localStorage.getItem(ADMIN_TOKEN_KEY);
      if (!token) {
        setLoading(false);
        return;
      }

      try {
        const adminData = await adminAppService.getProfile();
        login(adminData);
      } catch {
        localStorage.removeItem(ADMIN_TOKEN_KEY);
        localStorage.removeItem(ADMIN_REFRESH_TOKEN_KEY);
        setLoading(false);
      }
    };

    initAuth();
  }, [login, setLoading]);

  const handleLogin = useCallback(
    async (username: string, password: string) => {
      const response = await adminAppService.login(username, password);
      localStorage.setItem(ADMIN_TOKEN_KEY, response.accessToken);
      localStorage.setItem(ADMIN_REFRESH_TOKEN_KEY, response.refreshToken);
      login(response.admin);
    },
    [login]
  );

  const handleLogout = useCallback(() => {
    localStorage.removeItem(ADMIN_TOKEN_KEY);
    localStorage.removeItem(ADMIN_REFRESH_TOKEN_KEY);
    logout();
  }, [logout]);

  return {
    admin,
    isAuthenticated,
    isLoading,
    login: handleLogin,
    logout: handleLogout,
  };
}
