// Admin LLM 模型管理 API
import { http } from "@/common/http";
import type {
  LLMModel,
  LLMSyncSource,
  LLMSyncResult,
  LLMModelCreate,
} from "@/common/types";

export const llmService = {
  async getList(limit = 1000) {
    return http.get<LLMModel[]>(`/llm/models?limit=${limit}`);
  },

  async getById(id: string) {
    return http.get<LLMModel>(`/llm/models/${id}`);
  },

  async create(data: LLMModelCreate) {
    return http.post<LLMModel>("/llm/models", data);
  },

  async update(id: string, data: LLMModelCreate) {
    return http.put<LLMModel>(`/llm/models/${id}`, data);
  },

  async delete(id: string) {
    return http.delete<void>(`/llm/models/${id}`);
  },

  async getSyncSources() {
    return http.get<LLMSyncSource[]>("/llm/sync/sources");
  },

  async sync(sourceId?: string) {
    const url = sourceId ? `/llm/sync?source_id=${sourceId}` : "/llm/sync";
    return http.post<LLMSyncResult>(url);
  },
};
