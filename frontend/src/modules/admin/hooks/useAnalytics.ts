// Admin 分析统计 Hook
import { useState, useEffect, useCallback } from "react";
import { analyticsService } from "../services/analytics.service";
import type { AnalyticsSummary } from "@/common/types";

interface UseAnalyticsOptions {
  autoFetch?: boolean;
}

export function useAnalytics(options: UseAnalyticsOptions = {}) {
  const { autoFetch = true } = options;
  const [summary, setSummary] = useState<AnalyticsSummary | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchSummary = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await analyticsService.getSummary();
      setSummary(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch summary");
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (autoFetch) {
      fetchSummary();
    }
  }, [autoFetch, fetchSummary]);

  return {
    summary,
    loading,
    error,
    fetchSummary,
  };
}
