// Admin 检索引擎管理 API
import { http } from "@/common/http";
import type {
  RetrievalEngine,
  RetrievalEngineType,
  RetrievalEngineCreate,
  RetrievalTestResult,
} from "@/common/types";

export const retrievalService = {
  async getList(limit = 100) {
    return http.get<RetrievalEngine[]>(`/retrieval/engines?limit=${limit}`);
  },

  async getTypes() {
    return http.get<RetrievalEngineType[]>("/retrieval/types");
  },

  async create(data: RetrievalEngineCreate) {
    return http.post<RetrievalEngine>("/retrieval/engines", data);
  },

  async update(id: string, data: RetrievalEngineCreate) {
    return http.put<RetrievalEngine>(`/retrieval/engines/${id}`, data);
  },

  async delete(id: string) {
    return http.delete<void>(`/retrieval/engines/${id}`);
  },

  async setDefault(engineId: string) {
    return http.post<void>("/retrieval/engines/default", {
      engineId,
    });
  },

  async test(
    engineId: string,
    query: string,
    context: Record<string, unknown> = {}
  ) {
    return http.post<RetrievalTestResult>("/retrieval/test", {
      engineId,
      query,
      context,
    });
  },
};
