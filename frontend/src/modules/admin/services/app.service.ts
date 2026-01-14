// Admin App 服务 - 认证相关 API
import { http } from "@/common/http";
import type { AdminAuthUser } from "@/common/types";

export const adminAppService = {
  async login(
    username: string,
    password: string
  ): Promise<{
    accessToken: string;
    refreshToken: string;
    admin: AdminAuthUser;
  }> {
    return http.post("/admin/auth/login", { username, password });
  },

  async getProfile(): Promise<AdminAuthUser> {
    return http.get("/admin/auth/me");
  },

  async refreshToken(
    refreshToken: string
  ): Promise<{ accessToken: string; refreshToken: string }> {
    return http.post("/admin/auth/refresh", { refreshToken });
  },
};
