import { http } from "@/common/http";
import type {
  AdminRecommendation,
  UpdateRecommendationDto,
  PaginatedResponse,
} from "../types/admin.types";

export interface RecommendationListParams {
  page?: number;
  limit?: number;
  domainId?: string;
  status?: string;
}

export const recommendationService = {
  getAll(params?: RecommendationListParams) {
    const query = new URLSearchParams();
    if (params?.page) query.set("page", String(params.page));
    if (params?.limit) query.set("limit", String(params.limit));
    if (params?.domainId) query.set("domain_id", params.domainId);
    if (params?.status) query.set("status", params.status);
    const queryStr = query.toString();
    return http.get<PaginatedResponse<AdminRecommendation>>(
      `/admin/recommendations${queryStr ? `?${queryStr}` : ""}`
    );
  },

  getById(id: string) {
    return http.get<AdminRecommendation>(`/admin/recommendations/${id}`);
  },

  update(id: string, data: UpdateRecommendationDto) {
    return http.put<AdminRecommendation>(`/admin/recommendations/${id}`, data);
  },

  delete(id: string) {
    return http.delete<void>(`/admin/recommendations/${id}`);
  },
};
