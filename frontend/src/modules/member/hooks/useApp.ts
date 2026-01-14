// Member App Hook - 管理 session 初始化、主题、导航
import { useState, useEffect, useCallback } from "react";
import {
  useAuthStore,
  useMemberSettingsStore,
  useMemberNavigationStore,
  useMemberConversationStore,
} from "@/common/stores";
import { appService } from "../services/app.service";
import { logger } from "@/common/logger";

export function useApp() {
  const { setUser, setQuotaStatus, logout: storeLogout } = useAuthStore();
  const { theme, setTheme } = useMemberSettingsStore();
  const { view } = useMemberNavigationStore();
  const { setConversations, setActiveConversationId } =
    useMemberConversationStore();

  const [isInitialized, setIsInitialized] = useState(false);

  useEffect(() => {
    const initSession = async () => {
      try {
        const token = localStorage.getItem("token");
        const sessionToken = sessionStorage.getItem("sessionToken");

        if (token) {
          try {
            const [user, quota] = await Promise.all([
              appService.getCurrentUser(),
              appService.getQuotaStatus(),
            ]);
            setUser(user);
            setQuotaStatus(quota);
          } catch {
            localStorage.removeItem("token");
            localStorage.removeItem("refreshToken");
            await createAnonymousSession();
          }
        } else if (sessionToken) {
          try {
            const quota = await appService.getQuotaStatus();
            setQuotaStatus(quota);
            setUser({
              id: "",
              email: null,
              name: null,
              userType: "ANONYMOUS",
              isAnonymous: true,
            });
          } catch {
            sessionStorage.removeItem("sessionToken");
            await createAnonymousSession();
          }
        } else {
          await createAnonymousSession();
        }
      } catch (error) {
        logger.error("Session initialization failed", {
          error: error instanceof Error ? error.message : String(error),
        });
      } finally {
        setIsInitialized(true);
      }
    };

    const createAnonymousSession = async () => {
      try {
        const { sessionToken, user, quota } =
          await appService.createAnonymousSession();
        sessionStorage.setItem("sessionToken", sessionToken);
        setUser(user);
        setQuotaStatus(quota);
      } catch (error) {
        logger.error("Failed to create anonymous session", {
          error: error instanceof Error ? error.message : String(error),
        });
      }
    };

    initSession();
  }, [setUser, setQuotaStatus]);

  useEffect(() => {
    if (theme === "dark") {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
    localStorage.setItem("theme", theme);
  }, [theme]);

  const handleLogout = useCallback(() => {
    localStorage.removeItem("token");
    localStorage.removeItem("refreshToken");
    sessionStorage.removeItem("sessionToken");
    storeLogout();
    setConversations([]);
    setActiveConversationId(null);
  }, [storeLogout, setConversations, setActiveConversationId]);

  useEffect(() => {
    window.addEventListener("auth:logout", handleLogout);
    return () => window.removeEventListener("auth:logout", handleLogout);
  }, [handleLogout]);

  return {
    view,
    isInitialized,
  };
}
