// Admin 推荐管理 Service
import type {
  AdminRecommendation,
  RecommendationListParams,
} from "@/common/types";
import { getApiBase, getAuthHeaders, keysToCamel } from "@/common/helper";

const API_BASE = getApiBase();

export const recommendationService = {
  async getList(params: RecommendationListParams) {
    const searchParams = new URLSearchParams();
    if (params.page) searchParams.set("page", String(params.page));
    if (params.limit) searchParams.set("limit", String(params.limit));
    if (params.status) searchParams.set("status", params.status);
    if (params.domainId) searchParams.set("domain_id", params.domainId);

    const res = await fetch(
      `${API_BASE}/admin/recommendations?${searchParams}`,
      {
        headers: getAuthHeaders(),
      }
    );
    const json = await res.json();
    return {
      data: (json.data || []).map(keysToCamel) as AdminRecommendation[],
      meta: { total: json.meta?.total || 0 },
    };
  },

  async updateStatus(
    id: string,
    status: "APPROVED" | "REJECTED"
  ): Promise<void> {
    await fetch(`${API_BASE}/admin/recommendations/${id}`, {
      method: "PUT",
      headers: { ...getAuthHeaders(), "Content-Type": "application/json" },
      body: JSON.stringify({ status }),
    });
  },

  async delete(id: string): Promise<void> {
    await fetch(`${API_BASE}/admin/recommendations/${id}`, {
      method: "DELETE",
      headers: getAuthHeaders(),
    });
  },
};
