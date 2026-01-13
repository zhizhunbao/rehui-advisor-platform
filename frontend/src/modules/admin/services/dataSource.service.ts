// Admin 数据源管理 API
import { http } from "@/common/http";
import type {
  DataSource,
  DataSourceStats,
  DataSourceCategory,
  DataSourceDomain,
  DataSourceTypeItem,
  DataSourceStatusItem,
  DataSourceLanguageItem,
  DataSourceListParams,
  DataSourceCreate,
} from "@/common/types";

export const dataSourceService = {
  async getList(params: DataSourceListParams = {}) {
    const query = new URLSearchParams();
    if (params.page) query.set("page", params.page.toString());
    if (params.limit) query.set("limit", params.limit.toString());
    if (params.search) query.set("search", params.search);
    if (params.categoryId) query.set("category_id", params.categoryId);
    if (params.domainId) query.set("domain_id", params.domainId);
    if (params.status) query.set("status", params.status);
    if (params.type) query.set("type", params.type);
    if (params.language) query.set("language", params.language);
    return http.get<{ data: DataSource[]; meta: { total: number } }>(
      `/data-sources?${query}`
    );
  },

  async getStats() {
    return http.get<DataSourceStats>("/data-sources/stats");
  },

  async getCategories() {
    return http.get<DataSourceCategory[]>("/data-sources/categories");
  },

  async getDomains(categoryId?: string) {
    const url = categoryId
      ? `/data-sources/categories/${categoryId}/domains`
      : "/data-sources/domains";
    return http.get<DataSourceDomain[]>(url);
  },

  async getTypes() {
    return http.get<DataSourceTypeItem[]>("/data-sources/types");
  },

  async getStatuses() {
    return http.get<DataSourceStatusItem[]>("/data-sources/statuses");
  },

  async getLanguages() {
    return http.get<DataSourceLanguageItem[]>("/data-sources/languages");
  },

  async create(data: DataSourceCreate) {
    return http.post<DataSource>("/data-sources", data);
  },

  async delete(id: string) {
    return http.delete<void>(`/data-sources/${id}`);
  },

  async refresh(id: string) {
    return http.post<DataSource>(`/data-sources/${id}/refresh`);
  },

  async refreshAll() {
    return http.post<{ refreshed: number }>("/data-sources/refresh-all");
  },
};
