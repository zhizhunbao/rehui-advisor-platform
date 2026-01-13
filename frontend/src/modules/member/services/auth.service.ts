// Member 认证服务 API
import { http } from "@/common/http";
import type {
  LoginDto,
  RegisterDto,
  QuotaStatus,
  User,
  AuthApiResponse,
  AnonymousSessionApiResponse,
  QuotaStatusApiResponse,
  UserApiResponse,
} from "@/common/types";

export const authService = {
  async login(data: LoginDto): Promise<AuthApiResponse> {
    return http.post<AuthApiResponse>("/auth/login", data);
  },

  async register(data: RegisterDto): Promise<AuthApiResponse> {
    return http.post<AuthApiResponse>("/auth/register", data);
  },

  async refreshToken(refreshToken: string): Promise<AuthApiResponse> {
    return http.post<AuthApiResponse>("/auth/refresh", {
      refresh_token: refreshToken,
    });
  },

  async getCurrentUser(): Promise<User> {
    const res = await http.get<UserApiResponse>("/auth/me");
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
    const res = await http.get<QuotaStatusApiResponse>("/auth/quota/status");
    return {
      userType: res.user_type as QuotaStatus["userType"],
      searchCount: res.search_count,
      searchLimit: res.search_limit,
      remaining: res.remaining,
      resetAt: null,
      canSearch: res.remaining > 0,
    };
  },

  async createAnonymousSession(): Promise<AnonymousSessionApiResponse> {
    return http.post<AnonymousSessionApiResponse>("/auth/session/anonymous");
  },
};
