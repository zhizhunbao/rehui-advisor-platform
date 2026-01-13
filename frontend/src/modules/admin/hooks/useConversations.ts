// Admin 会话管理 Hook - 封装 API 调用和筛选状态
import { useState, useCallback } from "react";
import type { AdminConversation } from "@/common/types";
import { useInfiniteScroll } from "@/common/hooks";
import { conversationService } from "../services/conversation.service";

export function useConversations() {
  const [userId, setUserId] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [showDetail, setShowDetail] = useState(false);
  const [selectedConversation, setSelectedConversation] =
    useState<AdminConversation | null>(null);

  const fetchConversations = useCallback(
    async (page: number) => {
      const result = await conversationService.getAll({
        page,
        limit: 20,
        userId: userId || undefined,
        startDate: startDate || undefined,
        endDate: endDate || undefined,
      });
      return { data: result.data, total: result.total };
    },
    [userId, startDate, endDate]
  );

  const {
    data: conversations,
    isLoading,
    hasMore,
    total,
    loadMoreRef,
    refresh,
  } = useInfiniteScroll<AdminConversation>({ fetchFn: fetchConversations });

  const fetchConversationDetail = useCallback(async (id: string) => {
    const result = await conversationService.getById(id);
    setSelectedConversation(result);
    setShowDetail(true);
  }, []);

  const deleteConversation = useCallback(
    async (id: string) => {
      await conversationService.delete(id);
      refresh();
    },
    [refresh]
  );

  const resetFilters = useCallback(() => {
    setUserId("");
    setStartDate("");
    setEndDate("");
  }, []);

  return {
    conversations,
    selectedConversation,
    isLoading,
    hasMore,
    total,
    loadMoreRef,
    showDetail,
    setShowDetail,
    userId,
    setUserId,
    startDate,
    setStartDate,
    endDate,
    setEndDate,
    refresh,
    fetchConversationDetail,
    deleteConversation,
    resetFilters,
  };
}
