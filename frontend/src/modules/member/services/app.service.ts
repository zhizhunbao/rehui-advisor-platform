// Member App 服务 - session 初始化相关 API
import { http } from "@/common/http";
import type { User, QuotaStatus } from "@/common/types";

export const appService = {
  async createAnonymousSession(): Promise<{
    sessionToken: string;
    user: User;
    quota: QuotaStatus;
  }> {
    const res = await http.post<{
      session_token: string;
      user_id: string;
      user_type: string;
      search_count: number;
      search_limit: number;
    }>("/auth/anonymous");

    return {
      sessionToken: res.session_token,
      user: {
        id: res.user_id,
        email: null,
        name: null,
        userType: "ANONYMOUS",
        isAnonymous: true,
      },
      quota: {
        userType: "ANONYMOUS",
        searchCount: res.search_count,
        searchLimit: res.search_limit,
        remaining: res.search_limit - res.search_count,
        resetAt: null,
        canSearch: res.search_count < res.search_limit,
      },
    };
  },

  async getCurrentUser(): Promise<User> {
    return http.get<User>("/auth/me");
  },

  async getQuotaStatus(): Promise<QuotaStatus> {
    return http.get<QuotaStatus>("/auth/quota");
  },
};
