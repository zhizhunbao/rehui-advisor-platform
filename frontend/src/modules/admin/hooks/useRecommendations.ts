import { useState, useCallback } from "react";
import type {
  AdminRecommendation,
  UpdateRecommendationDto,
  PaginatedResponse,
  RecommendationListParams,
} from "@/common/types";
import { recommendationService } from "../services/recommendation.service";

export function useRecommendations() {
  const [data, setData] =
    useState<PaginatedResponse<AdminRecommendation> | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const fetchRecommendations = useCallback(
    async (params?: RecommendationListParams) => {
      setIsLoading(true);
      setError(null);
      try {
        const result = await recommendationService.getAll(params);
        setData(result);
        return result;
      } catch (err) {
        setError(
          err instanceof Error
            ? err
            : new Error("Failed to fetch recommendations")
        );
        return null;
      } finally {
        setIsLoading(false);
      }
    },
    []
  );

  const updateRecommendation = useCallback(
    async (id: string, updates: UpdateRecommendationDto) => {
      try {
        const updated = await recommendationService.update(id, updates);
        setData((prev) =>
          prev
            ? {
                ...prev,
                data: prev.data.map((r) => (r.id === id ? updated : r)),
              }
            : null
        );
        return updated;
      } catch (err) {
        setError(
          err instanceof Error
            ? err
            : new Error("Failed to update recommendation")
        );
        return null;
      }
    },
    []
  );

  const deleteRecommendation = useCallback(async (id: string) => {
    try {
      await recommendationService.delete(id);
      setData((prev) =>
        prev
          ? {
              ...prev,
              data: prev.data.filter((r) => r.id !== id),
              total: prev.total - 1,
            }
          : null
      );
      return true;
    } catch (err) {
      setError(
        err instanceof Error
          ? err
          : new Error("Failed to delete recommendation")
      );
      return false;
    }
  }, []);

  return {
    recommendations: data?.data || [],
    total: data?.total || 0,
    page: data?.page || 1,
    limit: data?.limit || 20,
    isLoading,
    error,
    fetchRecommendations,
    updateRecommendation,
    deleteRecommendation,
  };
}
