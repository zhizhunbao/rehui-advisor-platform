// Admin 仪表盘 Hook
import { useState, useEffect, useCallback } from "react";
import type { AnalyticsSummary } from "@/common/types";
import { analyticsService } from "../services/analytics.service";

export function useDashboard(autoFetch = true) {
  const [summary, setSummary] = useState<AnalyticsSummary | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const fetchData = useCallback(async () => {
    setIsLoading(true);
    try {
      const data = await analyticsService.getSummary();
      setSummary(data);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    if (autoFetch) {
      fetchData();
    }
  }, [autoFetch, fetchData]);

  return {
    summary,
    isLoading,
    refresh: fetchData,
  };
}
