// Admin 技能管理 API
import { http } from "@/common/http";
import type {
  Skill,
  SkillStats,
  SkillLabels,
  SkillListParams,
} from "@/common/types";

export const skillService = {
  async getList(params: SkillListParams = {}) {
    const query = new URLSearchParams();
    if (params.page) query.set("page", params.page.toString());
    if (params.limit) query.set("limit", params.limit.toString());
    if (params.search) query.set("search", params.search);
    if (params.category) query.set("category", params.category);
    if (params.source) query.set("source", params.source);
    return http.get<{ data: Skill[]; meta: { total: number } }>(
      `/skills?${query}`
    );
  },

  async getStats() {
    return http.get<SkillStats>("/skills/stats");
  },

  async getLabels() {
    return http.get<SkillLabels>("/skills/labels");
  },

  async toggle(id: string) {
    return http.post<Skill>(`/skills/${id}/toggle`);
  },

  async sync() {
    return http.post<{ synced: number }>("/skills/sync");
  },
};
