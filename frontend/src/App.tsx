import { useState, useEffect, useCallback } from "react";
import type {
  Conversation,
  Message,
  Topic,
  Language,
  Theme,
  GroundingSource,
  AppView,
} from "./modules/member/types";
import MemberLayout from "./modules/member/components/MemberLayout";
import MemberQuotaExhaustedModal from "./modules/member/components/MemberQuotaExhaustedModal";
import { streamChat } from "./modules/member/services/advisor.service";
import { authService } from "./modules/member/services/auth.service";
import { useAuthStore } from "./common/stores";
import HomeView from "./modules/member/views/HomeView";
import ConversationView from "./modules/member/views/ConversationView";
import AuthView from "./modules/member/views/AuthView";
import { ErrorBoundary } from "./common/ErrorBoundary";
import { ToastProvider } from "./common/toast";
import { logger } from "./common/logger";

function App() {
  const [view, setView] = useState<AppView>("home");
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [activeConversationId, setActiveConversationId] = useState<
    string | null
  >(null);
  const [isAiLoading, setIsAiLoading] = useState(false);
  const [showQuotaModal, setShowQuotaModal] = useState(false);

  const {
    user,
    quotaStatus,
    logout: storeLogout,
    updateQuota,
    setUser,
    setQuotaStatus,
  } = useAuthStore();

  const [lang, setLang] = useState<Language>(
    () => (localStorage.getItem("lang") as Language) || "zh"
  );
  const [theme, setTheme] = useState<Theme>(
    () => (localStorage.getItem("theme") as Theme) || "dark"
  );

  // 初始化会话
  useEffect(() => {
    const initSession = async () => {
      try {
        const token = localStorage.getItem("token");
        const sessionToken = sessionStorage.getItem("sessionToken");

        if (token) {
          // 已有 JWT token，获取用户信息和配额
          try {
            const [currentUser, quota] = await Promise.all([
              authService.getCurrentUser(),
              authService.getQuotaStatus(),
            ]);
            setUser(currentUser);
            setQuotaStatus(quota);
          } catch {
            // Token 无效，清除并创建匿名会话
            localStorage.removeItem("token");
            localStorage.removeItem("refreshToken");
            await createAnonymousSession();
          }
        } else if (sessionToken) {
          // 已有 session token，获取配额状态
          try {
            const quota = await authService.getQuotaStatus();
            setQuotaStatus(quota);
            setUser({
              id: "",
              email: null,
              name: null,
              userType: "ANONYMOUS",
              isAnonymous: true,
            });
          } catch {
            // Session 无效，创建新的匿名会话
            sessionStorage.removeItem("sessionToken");
            await createAnonymousSession();
          }
        } else {
          // 没有任何会话，创建匿名会话
          await createAnonymousSession();
        }
      } catch (error) {
        logger.error("Session initialization failed", {
          error: error instanceof Error ? error.message : String(error),
        });
      }
    };

    const createAnonymousSession = async () => {
      try {
        const session = await authService.createAnonymousSession();
        sessionStorage.setItem("sessionToken", session.session_token);
        setUser({
          id: session.user_id,
          email: null,
          name: null,
          userType: "ANONYMOUS",
          isAnonymous: true,
        });
        setQuotaStatus({
          userType: "ANONYMOUS",
          searchCount: session.search_count,
          searchLimit: session.search_limit,
          remaining: session.search_limit - session.search_count,
          resetAt: null,
          canSearch: session.search_count < session.search_limit,
        });
      } catch (error) {
        logger.error("Failed to create anonymous session", {
          error: error instanceof Error ? error.message : String(error),
        });
      }
    };

    initSession();
  }, [setUser, setQuotaStatus]);

  useEffect(() => {
    const savedConvs = localStorage.getItem("conversations");
    if (savedConvs) setConversations(JSON.parse(savedConvs));
  }, []);

  useEffect(() => {
    if (theme === "dark") {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
    localStorage.setItem("theme", theme);
  }, [theme]);

  useEffect(() => {
    localStorage.setItem("lang", lang);
  }, [lang]);

  useEffect(() => {
    localStorage.setItem("conversations", JSON.stringify(conversations));
  }, [conversations]);

  const handleNavigate = (newView: AppView) => setView(newView);

  const handleAuthSuccess = () => {
    setView("home");
  };

  const handleLogout = useCallback(() => {
    localStorage.removeItem("token");
    localStorage.removeItem("refreshToken");
    sessionStorage.removeItem("sessionToken");
    storeLogout();
    setConversations([]);
    setActiveConversationId(null);
    setView("home");
  }, [storeLogout]);

  // 监听登出事件（从 http client 触发）
  useEffect(() => {
    const handleAuthLogout = () => {
      handleLogout();
    };

    window.addEventListener("auth:logout", handleAuthLogout);
    return () => {
      window.removeEventListener("auth:logout", handleAuthLogout);
    };
  }, [handleLogout]);

  const toggleLang = () => setLang((prev) => (prev === "zh" ? "en" : "zh"));
  const toggleTheme = () =>
    setTheme((prev) => (prev === "dark" ? "light" : "dark"));

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

      setConversations((prev) =>
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
                (ns) => !sources.some((s) => s.uri === ns.uri)
              ),
            ];
          }
          setConversations((prev) =>
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

        setConversations((prev) =>
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

        // 更新配额
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
        setConversations((prev) =>
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
    [lang, quotaStatus, updateQuota]
  );

  const createNewConversation = useCallback(
    (initialMessage?: string, topic?: Topic, hidden: boolean = false) => {
      // 检查配额
      if (initialMessage && quotaStatus && quotaStatus.remaining <= 0) {
        setShowQuotaModal(true);
        return;
      }

      const newId = Date.now().toString();
      const initialMsgs: Message[] = [];

      if (initialMessage) {
        initialMsgs.push({
          id: Date.now().toString() + "-user",
          role: "user",
          content: initialMessage,
          timestamp: Date.now(),
          metadata: { hidden },
        });
      }

      const newConv: Conversation = {
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

      setConversations((prev) => [newConv, ...prev]);
      setActiveConversationId(newId);
      setView("conversation");

      if (initialMessage) processAiReplyStream(newId, initialMsgs);
    },
    [lang, processAiReplyStream, quotaStatus]
  );

  const handleTopicClick = (topic: Topic) =>
    createNewConversation(topic.prompt, topic, true);
  const handleQuickSearch = (query: string) => createNewConversation(query);

  const handleDeleteConversation = (id: string) => {
    setConversations((prev) => prev.filter((c) => c.id !== id));
    if (activeConversationId === id) {
      setActiveConversationId(null);
      setView("home");
    }
  };

  const handleSendMessage = async (content: string) => {
    // 检查配额
    if (quotaStatus && quotaStatus.remaining <= 0) {
      setShowQuotaModal(true);
      return;
    }

    if (!activeConversationId) {
      createNewConversation(content);
      return;
    }
    const userMsg: Message = {
      id: Date.now().toString() + "-user",
      role: "user",
      content,
      timestamp: Date.now(),
    };
    let updatedHistory: Message[] = [];
    setConversations((prev) =>
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
  };

  const activeConv = conversations.find((c) => c.id === activeConversationId);

  const renderContent = () => {
    switch (view) {
      case "home":
        return (
          <HomeView
            lang={lang}
            onTopicClick={handleTopicClick}
            onQuickSearch={handleQuickSearch}
          />
        );
      case "conversation":
        return (
          <ConversationView
            conversation={activeConv}
            quotaStatus={quotaStatus}
            lang={lang}
            onSendMessage={handleSendMessage}
            isLoading={isAiLoading}
          />
        );
      case "login":
        return (
          <AuthView
            type="login"
            lang={lang}
            onNavigate={handleNavigate}
            onAuthSuccess={handleAuthSuccess}
          />
        );
      case "register":
        return (
          <AuthView
            type="register"
            lang={lang}
            onNavigate={handleNavigate}
            onAuthSuccess={handleAuthSuccess}
          />
        );
      default:
        return (
          <HomeView
            lang={lang}
            onTopicClick={handleTopicClick}
            onQuickSearch={handleQuickSearch}
          />
        );
    }
  };

  return (
    <ErrorBoundary>
      <ToastProvider>
        <MemberLayout
          view={view}
          user={user}
          quotaStatus={quotaStatus}
          lang={lang}
          theme={theme}
          onNavigate={handleNavigate}
          onLogout={handleLogout}
          onToggleLang={toggleLang}
          onToggleTheme={toggleTheme}
          conversations={conversations}
          activeConversationId={activeConversationId}
          onSelectConversation={(id) => {
            setActiveConversationId(id);
            setView(id ? "conversation" : "home");
          }}
          onNewChat={() => {
            setActiveConversationId(null);
            setView("home");
          }}
          onDeleteConversation={handleDeleteConversation}
        >
          {renderContent()}
        </MemberLayout>
        <MemberQuotaExhaustedModal
          lang={lang}
          quotaStatus={quotaStatus}
          isOpen={showQuotaModal}
          onClose={() => setShowQuotaModal(false)}
          onNavigate={(newView) => {
            setShowQuotaModal(false);
            handleNavigate(newView);
          }}
        />
      </ToastProvider>
    </ErrorBoundary>
  );
}

export default App;
