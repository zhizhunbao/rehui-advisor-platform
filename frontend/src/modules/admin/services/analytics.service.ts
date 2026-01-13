// Admin 分析统计 API
import { http } from "@/common/http";
import type { AnalyticsSummary } from "@/common/types";

export const analyticsService = {
  getSummary() {
    return http.get<AnalyticsSummary>("/admin/analytics/summary");
  },
};
