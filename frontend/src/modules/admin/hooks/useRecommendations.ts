// Admin 推荐管理 Hook
import { useState, useCallback } from "react";
import type { AdminRecommendation } from "@/common/types";
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import { useInfiniteScroll } from "@/common/hooks";
import { recommendationService } from "../services/recommendation.service";

export function useRecommendations() {
  const { lang } = useAdminSettingsStore();
  const [statusFilter, setStatusFilter] = useState("__all__");

  const fetchRecommendations = useCallback(
    async (page: number) => {
      const res = await recommendationService.getList({
        page,
        limit: 20,
        status: statusFilter !== "__all__" ? statusFilter : undefined,
      });
      return { data: res.data, total: res.meta.total };
    },
    [statusFilter]
  );

  const {
    data: recommendations,
    isLoading,
    hasMore,
    total,
    loadMoreRef,
    refresh,
  } = useInfiniteScroll<AdminRecommendation>({ fetchFn: fetchRecommendations });

  const handleStatusChange = useCallback(
    async (id: string, status: "APPROVED" | "REJECTED") => {
      await recommendationService.updateStatus(id, status);
      refresh();
    },
    [refresh]
  );

  const handleDelete = useCallback(
    async (id: string) => {
      await recommendationService.delete(id);
      refresh();
    },
    [refresh]
  );

  const getStatusLabel = useCallback(
    (status: string) => {
      const t = adminLocales[lang];
      switch (status) {
        case "PENDING":
          return t.pending;
        case "APPROVED":
          return t.approved;
        case "REJECTED":
          return t.rejected;
        default:
          return status;
      }
    },
    [lang]
  );

  const getStatusVariant = useCallback(
    (status: string): "default" | "secondary" | "destructive" | "outline" => {
      switch (status) {
        case "PENDING":
          return "outline";
        case "APPROVED":
          return "default";
        case "REJECTED":
          return "destructive";
        default:
          return "secondary";
      }
    },
    []
  );

  return {
    recommendations,
    isLoading,
    hasMore,
    total,
    loadMoreRef,
    statusFilter,
    setStatusFilter,
    handleStatusChange,
    handleDelete,
    getStatusLabel,
    getStatusVariant,
  };
}
