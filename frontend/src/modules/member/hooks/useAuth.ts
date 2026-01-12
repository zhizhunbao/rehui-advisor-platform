import { useCallback, useState } from "react";
import { useAuthStore } from "../store/useAuthStore";
import { authService } from "../services/auth.service";
import type { LoginDto, RegisterDto, User, QuotaStatus } from "../types";

interface UseAuthReturn {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  quotaStatus: QuotaStatus | null;
  login: (data: LoginDto) => Promise<void>;
  register: (data: RegisterDto) => Promise<void>;
  logout: () => void;
  initAnonymousSession: () => Promise<void>;
  refreshQuota: () => Promise<void>;
  refreshToken: () => Promise<boolean>;
  updatePassword: (oldPassword: string, newPassword: string) => Promise<void>;
  fetchCurrentUser: () => Promise<void>;
}

export function useAuth(): UseAuthReturn {
  const [isLoading, setIsLoading] = useState(false);
  const {
    user,
    isAuthenticated,
    quotaStatus,
    login: storeLogin,
    logout: storeLogout,
    setQuotaStatus,
    setUser,
  } = useAuthStore();

  const login = useCallback(
    async (data: LoginDto): Promise<void> => {
      setIsLoading(true);
      try {
        const res = await authService.login(data);
        localStorage.setItem("token", res.access_token);
        localStorage.setItem("refreshToken", res.refresh_token);

        const quota = await authService.getQuotaStatus();
        const userData: User = {
          id: res.user_id,
          email: data.email,
          name: null,
          userType: res.user_type as User["userType"],
        };

        storeLogin(userData, res.access_token, quota);
      } finally {
        setIsLoading(false);
      }
    },
    [storeLogin]
  );

  const register = useCallback(
    async (data: RegisterDto): Promise<void> => {
      setIsLoading(true);
      try {
        const res = await authService.register(data);
        localStorage.setItem("token", res.access_token);
        localStorage.setItem("refreshToken", res.refresh_token);

        const quota = await authService.getQuotaStatus();
        const userData: User = {
          id: res.user_id,
          email: data.email,
          name: data.name || null,
          userType: res.user_type as User["userType"],
        };

        storeLogin(userData, res.access_token, quota);
      } finally {
        setIsLoading(false);
      }
    },
    [storeLogin]
  );

  const logout = useCallback(() => {
    localStorage.removeItem("token");
    localStorage.removeItem("refreshToken");
    sessionStorage.removeItem("sessionToken");
    storeLogout();
  }, [storeLogout]);

  const initAnonymousSession = useCallback(async () => {
    const res = await authService.createAnonymousSession();
    sessionStorage.setItem("sessionToken", res.session_token);

    const userData: User = {
      id: res.user_id,
      email: null,
      name: null,
      userType: res.user_type as User["userType"],
      isAnonymous: true,
    };
    const quota: QuotaStatus = {
      userType: res.user_type as QuotaStatus["userType"],
      searchCount: res.search_count,
      searchLimit: res.search_limit,
      remaining: res.search_limit - res.search_count,
      resetAt: null,
      canSearch: res.search_count < res.search_limit,
    };

    storeLogin(userData, res.session_token, quota);
  }, [storeLogin]);

  const refreshQuota = useCallback(async () => {
    const quota = await authService.getQuotaStatus();
    setQuotaStatus(quota);
  }, [setQuotaStatus]);

  const refreshToken = useCallback(async (): Promise<boolean> => {
    const storedRefreshToken = localStorage.getItem("refreshToken");
    if (!storedRefreshToken) return false;

    try {
      const res = await authService.refreshToken(storedRefreshToken);
      localStorage.setItem("token", res.access_token);
      localStorage.setItem("refreshToken", res.refresh_token);
      return true;
    } catch {
      logout();
      return false;
    }
  }, [logout]);

  const updatePassword = useCallback(
    async (oldPassword: string, newPassword: string): Promise<void> => {
      await authService.updatePassword(oldPassword, newPassword);
    },
    []
  );

  const fetchCurrentUser = useCallback(async (): Promise<void> => {
    const userData = await authService.getCurrentUser();
    setUser(userData);
  }, [setUser]);

  return {
    user,
    isAuthenticated,
    isLoading,
    quotaStatus,
    login,
    register,
    logout,
    initAnonymousSession,
    refreshQuota,
    refreshToken,
    updatePassword,
    fetchCurrentUser,
  };
}
