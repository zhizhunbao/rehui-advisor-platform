// Admin 数据抓取管理 API
import { http } from "@/common/http";
import type { CrawlSource, CrawlTask } from "@/common/types";

export const crawlerService = {
  getSources() {
    return http.get<CrawlSource[]>("/admin/crawlers/sources");
  },
  createSource(data: Partial<CrawlSource>) {
    return http.post<CrawlSource>("/admin/crawlers/sources", data);
  },
  updateSource(id: string, data: Partial<CrawlSource>) {
    return http.put<CrawlSource>(`/admin/crawlers/sources/${id}`, data);
  },
  deleteSource(id: string) {
    return http.delete<void>(`/admin/crawlers/sources/${id}`);
  },
  getTasks(sourceId?: string) {
    const query = sourceId ? `?sourceId=${sourceId}` : "";
    return http.get<CrawlTask[]>(`/admin/crawlers/tasks${query}`);
  },
  runTask(sourceId: string) {
    return http.post<CrawlTask>(`/admin/crawlers/sources/${sourceId}/run`);
  },
};
