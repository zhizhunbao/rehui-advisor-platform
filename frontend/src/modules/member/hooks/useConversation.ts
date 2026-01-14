// Member 对话 Hook - 管理对话滚动、配额检查、消息发送
import { useRef, useEffect, useCallback } from "react";
import type { Message, GroundingSource } from "@/common/types";
import {
  useAuthStore,
  useMemberSettingsStore,
  useMemberConversationStore,
  useMemberNavigationStore,
} from "@/common/stores";
import { streamChat } from "../services/conversation.service";
import { logger } from "@/common/logger";

export function useConversation() {
  const { quotaStatus, updateQuota } = useAuthStore();
  const { lang } = useMemberSettingsStore();
  const {
    conversations,
    activeConversationId,
    isAiLoading,
    updateConversations,
    setActiveConversationId,
    setIsAiLoading,
    setShowQuotaModal,
  } = useMemberConversationStore();
  const { setView } = useMemberNavigationStore();

  const scrollRef = useRef<HTMLDivElement | null>(null);
  const conversation = conversations.find((c) => c.id === activeConversationId);
  const isQuotaExhausted = quotaStatus ? quotaStatus.remaining <= 0 : false;

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTo({
        top: scrollRef.current.scrollHeight,
        behavior: "smooth",
      });
    }
  }, [conversation?.messages, isAiLoading]);

  const processAiReplyStream = useCallback(
    async (convId: string, history: Message[]) => {
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
          c.id === convId
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
              c.id === convId
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
            c.id === convId
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
      } catch (error) {
        logger.error("Streaming Error", {
          error: error instanceof Error ? error.message : String(error),
        });
        updateConversations((prev) =>
          prev.map((c) =>
            c.id === convId
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

  const handleSendMessage = useCallback(
    async (content: string) => {
      if (quotaStatus && quotaStatus.remaining <= 0) {
        setShowQuotaModal(true);
        return;
      }

      if (!activeConversationId) {
        const newId = Date.now().toString();
        const userMsg: Message = {
          id: Date.now().toString() + "-user",
          role: "user",
          content,
          timestamp: Date.now(),
        };
        const newConv = {
          id: newId,
          title: content.slice(0, 20),
          messages: [userMsg],
          updatedAt: Date.now(),
        };
        updateConversations((prev) => [newConv, ...prev]);
        setActiveConversationId(newId);
        setView("conversation");
        await processAiReplyStream(newId, [userMsg]);
        return;
      }

      const userMsg: Message = {
        id: Date.now().toString() + "-user",
        role: "user",
        content,
        timestamp: Date.now(),
      };
      let updatedHistory: Message[] = [];

      updateConversations((prev) =>
        prev.map((c) => {
          if (c.id === activeConversationId) {
            updatedHistory = [...c.messages, userMsg];
            return {
              ...c,
              messages: updatedHistory,
              updatedAt: Date.now(),
              title: c.messages.length <= 1 ? content.slice(0, 20) : c.title,
            };
          }
          return c;
        })
      );

      await processAiReplyStream(activeConversationId, updatedHistory);
    },
    [
      activeConversationId,
      quotaStatus,
      processAiReplyStream,
      updateConversations,
      setActiveConversationId,
      setView,
      setShowQuotaModal,
    ]
  );

  const handleRegenerate = useCallback(() => {
    if (conversation && conversation.messages.length > 1 && !isAiLoading) {
      const lastUserMsg = [...conversation.messages]
        .reverse()
        .find((m) => m.role === "user");
      if (lastUserMsg) handleSendMessage(lastUserMsg.content);
    }
  }, [conversation, isAiLoading, handleSendMessage]);

  const handleSend = useCallback(
    (content: string) => {
      if (!isAiLoading) handleSendMessage(content);
    },
    [isAiLoading, handleSendMessage]
  );

  return {
    lang,
    conversation,
    quotaStatus,
    isLoading: isAiLoading,
    isQuotaExhausted,
    scrollRef,
    handleSend,
    handleRegenerate,
  };
}
