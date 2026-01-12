import { http } from "@/common/http";
import type {
  AdminUser,
  UpdateUserDto,
  PaginatedResponse,
} from "../types/admin.types";

export interface UserListParams {
  page?: number;
  limit?: number;
  search?: string;
  status?: string;
}

export const userService = {
  getAll(params?: UserListParams) {
    const query = new URLSearchParams();
    if (params?.page) query.set("page", String(params.page));
    if (params?.limit) query.set("limit", String(params.limit));
    if (params?.search) query.set("search", params.search);
    if (params?.status) query.set("status", params.status);
    const queryStr = query.toString();
    return http.get<PaginatedResponse<AdminUser>>(
      `/admin/users${queryStr ? `?${queryStr}` : ""}`
    );
  },

  getById(id: string) {
    return http.get<AdminUser>(`/admin/users/${id}`);
  },

  update(id: string, data: UpdateUserDto) {
    return http.put<AdminUser>(`/admin/users/${id}`, data);
  },

  toggleStatus(id: string) {
    return http.post<AdminUser>(`/admin/users/${id}/toggle-status`);
  },
};
