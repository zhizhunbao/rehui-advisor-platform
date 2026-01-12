import { http } from "@/common/http";
import type {
  SystemConfig,
  CreateConfigDto,
  UpdateConfigDto,
} from "../types/admin.types";

export const configService = {
  getAll(category?: string) {
    const query = category ? `?category=${category}` : "";
    return http.get<SystemConfig[]>(`/admin/configs${query}`);
  },

  getByKey(key: string) {
    return http.get<SystemConfig>(`/admin/configs/${key}`);
  },

  create(data: CreateConfigDto) {
    return http.post<SystemConfig>("/admin/configs", data);
  },

  update(key: string, data: UpdateConfigDto) {
    return http.put<SystemConfig>(`/admin/configs/${key}`, data);
  },

  delete(key: string) {
    return http.delete<void>(`/admin/configs/${key}`);
  },
};
