// 全局状态管理
import { create } from "zustand";
import { persist } from "zustand/middleware";
import type { User, QuotaStatus } from "./types";

// ==================== Member Auth Store ====================

interface AuthState {
  user: User | null;
  token: string | null;
  quotaStatus: QuotaStatus | null;
  isAuthenticated: boolean;
  isLoading: boolean;

  setUser: (user: User) => void;
  setToken: (token: string) => void;
  setQuotaStatus: (status: QuotaStatus) => void;
  login: (user: User, token: string, quotaStatus: QuotaStatus) => void;
  logout: () => void;
  updateQuota: (quotaStatus: QuotaStatus) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      quotaStatus: null,
      isAuthenticated: false,
      isLoading: false,

      setUser: (user) => set({ user, isAuthenticated: true }),
      setToken: (token) => set({ token }),
      setQuotaStatus: (quotaStatus) => set({ quotaStatus }),

      login: (user, token, quotaStatus) =>
        set({ user, token, quotaStatus, isAuthenticated: true }),

      logout: () =>
        set({
          user: null,
          token: null,
          quotaStatus: null,
          isAuthenticated: false,
        }),

      updateQuota: (quotaStatus) => set({ quotaStatus }),
    }),
    {
      name: "auth-storage",
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        quotaStatus: state.quotaStatus,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);
