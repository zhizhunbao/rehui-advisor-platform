// Member 首页 hook - 管理话题分类
import { useState, useEffect, useCallback } from "react";
import type {
  Topic,
  TopicCategory,
  Message,
  GroundingSource,
} from "@/common/types";
import {
  useMemberSettingsStore,
  useMemberConversationStore,
  useMemberNavigationStore,
  useAuthStore,
} from "@/common/stores";
import { homeService } from "../services/home.service";
import { streamChat } from "../services/conversation.service";
import { logger } from "@/common/logger";

export function useHome() {
  const { lang } = useMemberSettingsStore();
  const { quotaStatus, updateQuota } = useAuthStore();
  const {
    updateConversations,
    setActiveConversationId,
    setShowQuotaModal,
    setIsAiLoading,
  } = useMemberConversationStore();
  const { setView } = useMemberNavigationStore();

  const [categories, setCategories] = useState<TopicCategory[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        setIsLoading(true);
        setError(null);
        const data = await homeService.getGroupedTopics(lang);
        setCategories(data);
      } catch {
        setError(lang === "zh" ? "加载失败" : "Failed to load");
      } finally {
        setIsLoading(false);
      }
    };
    fetchCategories();
  }, [lang]);

  const processAiReplyStream = useCallback(
    async (conversationId: string, history: Message[]) => {
      setIsAiLoading(true);
      const aiMsgId = Date.now().toString() + "-ai";
      const initialAiMsg: Message = {
        id: aiMsgId,
        role: "assistant",
        content: "",
        timestamp: Date.now(),
        isStreaming: true,
      };

      updateConversations((prev) =>
        prev.map((c) =>
          c.id === conversationId
            ? { ...c, messages: [...c.messages, initialAiMsg] }
            : c
        )
      );

      try {
        let fullText = "";
        let sources: GroundingSource[] = [];

        for await (const chunk of streamChat(history, lang)) {
          fullText += chunk.text || "";
          if (chunk.sources?.length) {
            sources = [
              ...sources,
              ...chunk.sources.filter(
                (ns: GroundingSource) => !sources.some((s) => s.uri === ns.uri)
              ),
            ];
          }
          updateConversations((prev) =>
            prev.map((c) =>
              c.id === conversationId
                ? {
                    ...c,
                    messages: c.messages.map((m) =>
                      m.id === aiMsgId
                        ? { ...m, content: fullText, sources }
                        : m
                    ),
                  }
                : c
            )
          );
        }

        updateConversations((prev) =>
          prev.map((c) =>
            c.id === conversationId
              ? {
                  ...c,
                  messages: c.messages.map((m) =>
                    m.id === aiMsgId ? { ...m, isStreaming: false } : m
                  ),
                  updatedAt: Date.now(),
                }
              : c
          )
        );

        if (quotaStatus) {
          updateQuota({
            ...quotaStatus,
            searchCount: quotaStatus.searchCount + 1,
            remaining: Math.max(0, quotaStatus.remaining - 1),
            canSearch: quotaStatus.remaining > 1,
          });
        }
      } catch (err) {
        logger.error("Streaming Error", {
          error: err instanceof Error ? err.message : String(err),
        });
        updateConversations((prev) =>
          prev.map((c) =>
            c.id === conversationId
              ? {
                  ...c,
                  messages: c.messages.map((m) =>
                    m.id === aiMsgId
                      ? {
                          ...m,
                          content:
                            lang === "zh"
                              ? "抱歉，检索实时信息时出现错误。"
                              : "Sorry, an error occurred.",
                          isStreaming: false,
                        }
                      : m
                  ),
                }
              : c
          )
        );
      } finally {
        setIsAiLoading(false);
      }
    },
    [lang, quotaStatus, updateQuota, updateConversations, setIsAiLoading]
  );

  const createConversation = useCallback(
    (initialMessage: string, topic?: Topic, hidden = false) => {
      if (quotaStatus && quotaStatus.remaining <= 0) {
        setShowQuotaModal(true);
        return;
      }

      const newId = Date.now().toString();
      const initialMsgs: Message[] = initialMessage
        ? [
            {
              id: Date.now().toString() + "-user",
              role: "user" as const,
              content: initialMessage,
              timestamp: Date.now(),
              metadata: { hidden },
            },
          ]
        : [];

      const newConversation = {
        id: newId,
        title: topic
          ? topic.title
          : initialMessage
          ? initialMessage.slice(0, 20)
          : lang === "zh"
          ? "新咨询"
          : "New Consulting",
        messages: initialMsgs,
        topicId: topic?.id,
        updatedAt: Date.now(),
      };

      updateConversations((prev) => [newConversation, ...prev]);
      setActiveConversationId(newId);
      setView("conversation");

      if (initialMessage) processAiReplyStream(newId, initialMsgs);
    },
    [
      lang,
      quotaStatus,
      processAiReplyStream,
      updateConversations,
      setActiveConversationId,
      setView,
      setShowQuotaModal,
    ]
  );

  const handleTopicClick = (topic: Topic) =>
    createConversation(topic.prompt, topic, true);
  const handleQuickSearch = (query: string) => createConversation(query);

  return {
    lang,
    categories,
    isLoading,
    error,
    handleTopicClick,
    handleQuickSearch,
  };
}
