// 全局状态管理
import { create } from "zustand";
import { persist } from "zustand/middleware";
import type {
  User,
  QuotaStatus,
  Language,
  Theme,
  Conversation,
  AppView,
  AdminAuthUser,
} from "./types";
import { type ThemeName, applyTheme, getStoredTheme } from "./themes";

// ==================== Admin Auth Store ====================

interface AdminAuthState {
  admin: AdminAuthUser | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  setAdmin: (admin: AdminAuthUser) => void;
  setLoading: (loading: boolean) => void;
  login: (admin: AdminAuthUser) => void;
  logout: () => void;
}

export const useAdminAuthStore = create<AdminAuthState>()((set) => ({
  admin: null,
  isAuthenticated: false,
  isLoading: true,
  setAdmin: (admin) => set({ admin, isAuthenticated: true }),
  setLoading: (isLoading) => set({ isLoading }),
  login: (admin) => set({ admin, isAuthenticated: true, isLoading: false }),
  logout: () => set({ admin: null, isAuthenticated: false, isLoading: false }),
}));

// ==================== Admin Settings Store ====================

interface AdminSettingsState {
  lang: Language;
  themeName: ThemeName;
  setLang: (lang: Language) => void;
  setThemeName: (themeName: ThemeName) => void;
}

export const useAdminSettingsStore = create<AdminSettingsState>()(
  persist(
    (set) => ({
      lang: "zh",
      themeName: getStoredTheme(),
      setLang: (lang) => set({ lang }),
      setThemeName: (themeName) => {
        applyTheme(themeName);
        set({ themeName });
      },
    }),
    {
      name: "admin-settings",
      partialize: (state) => ({
        lang: state.lang,
        themeName: state.themeName,
      }),
    }
  )
);

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

// ==================== Member Settings Store ====================

interface MemberSettingsState {
  lang: Language;
  theme: Theme;
  setLang: (lang: Language) => void;
  setTheme: (theme: Theme) => void;
  toggleLang: () => void;
  toggleTheme: () => void;
}

export const useMemberSettingsStore = create<MemberSettingsState>()(
  persist(
    (set) => ({
      lang: "zh",
      theme: "dark",
      setLang: (lang) => set({ lang }),
      setTheme: (theme) => set({ theme }),
      toggleLang: () =>
        set((state) => ({ lang: state.lang === "zh" ? "en" : "zh" })),
      toggleTheme: () =>
        set((state) => ({ theme: state.theme === "dark" ? "light" : "dark" })),
    }),
    {
      name: "member-settings",
      partialize: (state) => ({
        lang: state.lang,
        theme: state.theme,
      }),
    }
  )
);

// ==================== Member Navigation Store ====================

interface MemberNavigationState {
  view: AppView;
  setView: (view: AppView) => void;
}

export const useMemberNavigationStore = create<MemberNavigationState>()(
  (set) => ({
    view: "home",
    setView: (view) => set({ view }),
  })
);

// ==================== Member Conversation Store ====================

interface MemberConversationState {
  conversations: Conversation[];
  activeConversationId: string | null;
  isAiLoading: boolean;
  showQuotaModal: boolean;
  setConversations: (conversations: Conversation[]) => void;
  updateConversations: (
    updater: (prev: Conversation[]) => Conversation[]
  ) => void;
  setActiveConversationId: (id: string | null) => void;
  setIsAiLoading: (loading: boolean) => void;
  setShowQuotaModal: (show: boolean) => void;
  deleteConversation: (id: string) => void;
  getActiveConversation: () => Conversation | undefined;
}

export const useMemberConversationStore = create<MemberConversationState>()(
  persist(
    (set, get) => ({
      conversations: [],
      activeConversationId: null,
      isAiLoading: false,
      showQuotaModal: false,
      setConversations: (conversations) => set({ conversations }),
      updateConversations: (updater) =>
        set((state) => ({ conversations: updater(state.conversations) })),
      setActiveConversationId: (id) => set({ activeConversationId: id }),
      setIsAiLoading: (loading) => set({ isAiLoading: loading }),
      setShowQuotaModal: (show) => set({ showQuotaModal: show }),
      deleteConversation: (id) =>
        set((state) => ({
          conversations: state.conversations.filter((c) => c.id !== id),
          activeConversationId:
            state.activeConversationId === id
              ? null
              : state.activeConversationId,
        })),
      getActiveConversation: () => {
        const state = get();
        return state.conversations.find(
          (c) => c.id === state.activeConversationId
        );
      },
    }),
    {
      name: "member-conversations",
      partialize: (state) => ({
        conversations: state.conversations,
      }),
    }
  )
);
