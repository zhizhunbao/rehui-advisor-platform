// Member 认证 Hook - AuthView 使用
import { useCallback, useState } from "react";
import {
  useAuthStore,
  useMemberSettingsStore,
  useMemberNavigationStore,
} from "@/common/stores";
import { useErrorHandler } from "@/common/toast";
import type { LoginDto, RegisterDto, User, QuotaStatus } from "@/common/types";
import { authService } from "../services/auth.service";

export function useAuth(type: "login" | "register") {
  const [isLoading, setIsLoading] = useState(false);
  const {
    login: storeLogin,
    logout: storeLogout,
    setQuotaStatus,
    setUser,
  } = useAuthStore();
  const { lang } = useMemberSettingsStore();
  const { setView } = useMemberNavigationStore();
  const { handleError } = useErrorHandler();

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

  const handleSubmit = useCallback(
    async (data: { email: string; password: string; name?: string }) => {
      try {
        if (type === "login") {
          await login({ email: data.email, password: data.password });
        } else {
          await register({
            email: data.email,
            password: data.password,
            name: data.name,
          });
        }
        setView("home");
      } catch (error) {
        handleError(error, type === "login" ? "Login" : "Register");
      }
    },
    [type, login, register, setView, handleError]
  );

  const handleSocialLogin = useCallback((platform: string) => {
    console.info("Social login:", platform);
  }, []);

  const handleSwitchType = useCallback(() => {
    setView(type === "login" ? "register" : "login");
  }, [type, setView]);

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

  const fetchCurrentUser = useCallback(async (): Promise<void> => {
    const userData = await authService.getCurrentUser();
    setUser(userData);
  }, [setUser]);

  return {
    lang,
    type,
    isLoading,
    handleSubmit,
    handleSocialLogin,
    handleSwitchType,
    logout,
    initAnonymousSession,
    refreshQuota,
    fetchCurrentUser,
  };
}
