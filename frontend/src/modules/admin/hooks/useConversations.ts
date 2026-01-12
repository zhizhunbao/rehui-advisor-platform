import { useState, useCallback } from "react";
import {
  conversationService,
  type ConversationListParams,
} from "../services/conversation.service";
import type {
  AdminConversation,
  PaginatedResponse,
} from "../types/admin.types";

export function useConversations() {
  const [data, setData] = useState<PaginatedResponse<AdminConversation> | null>(
    null
  );
  const [selectedConversation, setSelectedConversation] =
    useState<AdminConversation | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const fetchConversations = useCallback(
    async (params?: ConversationListParams) => {
      setIsLoading(true);
      setError(null);
      try {
        const result = await conversationService.getAll(params);
        setData(result);
        return result;
      } catch (err) {
        setError(
          err instanceof Error
            ? err
            : new Error("Failed to fetch conversations")
        );
        return null;
      } finally {
        setIsLoading(false);
      }
    },
    []
  );

  const fetchConversationById = useCallback(async (id: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await conversationService.getById(id);
      setSelectedConversation(result);
      return result;
    } catch (err) {
      setError(
        err instanceof Error ? err : new Error("Failed to fetch conversation")
      );
      return null;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const deleteConversation = useCallback(async (id: string) => {
    try {
      await conversationService.delete(id);
      setData((prev) =>
        prev
          ? {
              ...prev,
              data: prev.data.filter((c) => c.id !== id),
              total: prev.total - 1,
            }
          : null
      );
      return true;
    } catch (err) {
      setError(
        err instanceof Error ? err : new Error("Failed to delete conversation")
      );
      return false;
    }
  }, []);

  return {
    conversations: data?.data || [],
    total: data?.total || 0,
    page: data?.page || 1,
    limit: data?.limit || 20,
    selectedConversation,
    isLoading,
    error,
    fetchConversations,
    fetchConversationById,
    deleteConversation,
    setSelectedConversation,
  };
}
