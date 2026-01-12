import {
  createContext,
  useContext,
  useState,
  useCallback,
  useEffect,
  ReactNode,
} from "react";
import { http } from "@/common/http";

interface AdminUser {
  id: string;
  username: string;
  email: string;
  name: string;
  role: "super_admin" | "admin";
  isActive: boolean;
}

interface AdminAuthState {
  admin: AdminUser | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

interface AdminAuthContextValue extends AdminAuthState {
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<void>;
}

const ADMIN_TOKEN_KEY = "admin_token";
const ADMIN_REFRESH_TOKEN_KEY = "admin_refresh_token";

const AdminAuthContext = createContext<AdminAuthContextValue | null>(null);

export function AdminAuthProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<AdminAuthState>({
    admin: null,
    isAuthenticated: false,
    isLoading: true,
  });

  // 初始化时检查 token
  useEffect(() => {
    const token = localStorage.getItem(ADMIN_TOKEN_KEY);
    if (token) {
      fetchAdminProfile();
    } else {
      setState((prev) => ({ ...prev, isLoading: false }));
    }
  }, []);

  const fetchAdminProfile = useCallback(async () => {
    try {
      const admin = await http.get<AdminUser>("/admin/auth/me");
      setState({
        admin,
        isAuthenticated: true,
        isLoading: false,
      });
    } catch {
      localStorage.removeItem(ADMIN_TOKEN_KEY);
      localStorage.removeItem(ADMIN_REFRESH_TOKEN_KEY);
      setState({
        admin: null,
        isAuthenticated: false,
        isLoading: false,
      });
    }
  }, []);

  const login = useCallback(async (username: string, password: string) => {
    const response = await http.post<{
      accessToken: string;
      refreshToken: string;
      admin: AdminUser;
    }>("/admin/auth/login", { username, password });

    localStorage.setItem(ADMIN_TOKEN_KEY, response.accessToken);
    localStorage.setItem(ADMIN_REFRESH_TOKEN_KEY, response.refreshToken);

    setState({
      admin: response.admin,
      isAuthenticated: true,
      isLoading: false,
    });
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem(ADMIN_TOKEN_KEY);
    localStorage.removeItem(ADMIN_REFRESH_TOKEN_KEY);
    setState({
      admin: null,
      isAuthenticated: false,
      isLoading: false,
    });
  }, []);

  const refreshToken = useCallback(async () => {
    const refresh = localStorage.getItem(ADMIN_REFRESH_TOKEN_KEY);
    if (!refresh) {
      logout();
      return;
    }

    try {
      const response = await http.post<{
        accessToken: string;
        refreshToken: string;
      }>("/admin/auth/refresh", { refreshToken: refresh });

      localStorage.setItem(ADMIN_TOKEN_KEY, response.accessToken);
      localStorage.setItem(ADMIN_REFRESH_TOKEN_KEY, response.refreshToken);
    } catch {
      logout();
    }
  }, [logout]);

  return (
    <AdminAuthContext.Provider
      value={{ ...state, login, logout, refreshToken }}
    >
      {children}
    </AdminAuthContext.Provider>
  );
}

export function useAdminAuth() {
  const context = useContext(AdminAuthContext);
  if (!context) {
    throw new Error("useAdminAuth must be used within AdminAuthProvider");
  }
  return context;
}
