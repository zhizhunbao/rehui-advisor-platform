import { http } from "@/common/http";
import type { LoginDto, RegisterDto, QuotaStatus, User } from "../types";

// 后端返回的原始格式
interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user_id: string;
  user_type: string;
}

interface AnonymousSessionResponse {
  session_token: string;
  user_id: string;
  user_type: string;
  search_limit: number;
  search_count: number;
}

interface QuotaStatusResponse {
  user_type: string;
  search_count: number;
  search_limit: number;
  remaining: number;
}

interface UserResponse {
  id: string;
  email: string | null;
  name: string | null;
  user_type: string;
  is_anonymous: boolean;
  search_limit: number;
  search_count: number;
}

export const authService = {
  async login(data: LoginDto): Promise<AuthResponse> {
    return http.post<AuthResponse>("/auth/login", data);
  },

  async register(data: RegisterDto): Promise<AuthResponse> {
    return http.post<AuthResponse>("/auth/register", data);
  },

  async refreshToken(refreshToken: string): Promise<AuthResponse> {
    return http.post<AuthResponse>("/auth/refresh", {
      refresh_token: refreshToken,
    });
  },

  async getCurrentUser(): Promise<User> {
    const res = await http.get<UserResponse>("/auth/me");
    return {
      id: res.id,
      email: res.email,
      name: res.name,
      userType: res.user_type as User["userType"],
      isAnonymous: res.is_anonymous,
    };
  },

  async updatePassword(
    oldPassword: string,
    newPassword: string
  ): Promise<void> {
    await http.put("/auth/password", {
      old_password: oldPassword,
      new_password: newPassword,
    });
  },

  async getQuotaStatus(): Promise<QuotaStatus> {
    const res = await http.get<QuotaStatusResponse>("/auth/quota/status");
    return {
      userType: res.user_type as QuotaStatus["userType"],
      searchCount: res.search_count,
      searchLimit: res.search_limit,
      remaining: res.remaining,
      resetAt: null,
      canSearch: res.remaining > 0,
    };
  },

  async createAnonymousSession(): Promise<AnonymousSessionResponse> {
    return http.post<AnonymousSessionResponse>("/auth/session/anonymous");
  },
};
