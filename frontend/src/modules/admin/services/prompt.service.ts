// Admin Prompt 管理 API
import { http } from "@/common/http";
import type {
  AdminPrompt,
  AdminPromptStats,
  SkillLabels,
  PromptTemplate,
  CreatePromptDto,
  UpdatePromptDto,
} from "@/common/types";

export const promptService = {
  getList(
    params: {
      page?: number;
      limit?: number;
      search?: string;
      category?: string;
      source?: string;
    } = {}
  ) {
    const query = new URLSearchParams();
    if (params.page) query.set("page", params.page.toString());
    if (params.limit) query.set("limit", params.limit.toString());
    if (params.search) query.set("search", params.search);
    if (params.category) query.set("category", params.category);
    if (params.source) query.set("source", params.source);
    return http.get<{ data: AdminPrompt[]; meta: { total: number } }>(
      `/prompts?${query}`
    );
  },

  getStats() {
    return http.get<AdminPromptStats>("/prompts/stats");
  },

  getLabels() {
    return http.get<SkillLabels>("/prompts/labels");
  },

  toggle(id: string) {
    return http.post<AdminPrompt>(`/prompts/${id}/toggle`);
  },

  sync() {
    return http.post<{ synced: number }>("/prompts/sync");
  },

  getAll() {
    return http.get<PromptTemplate[]>("/admin/prompts");
  },

  getById(id: string) {
    return http.get<PromptTemplate>(`/admin/prompts/${id}`);
  },

  create(data: CreatePromptDto) {
    return http.post<PromptTemplate>("/admin/prompts", data);
  },

  update(id: string, data: UpdatePromptDto) {
    return http.put<PromptTemplate>(`/admin/prompts/${id}`, data);
  },

  delete(id: string) {
    return http.delete<void>(`/admin/prompts/${id}`);
  },
};
