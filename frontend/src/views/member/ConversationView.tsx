import { useRef, useEffect } from "react";
import type {
  Conversation,
  Language,
  QuotaStatus,
} from "@/modules/member/types";
import { MessageBubble, ChatInput } from "@/modules/member/components";
import { memberLocales } from "@/modules/member/locales";
import { Search } from "lucide-react";

interface ConversationViewProps {
  conversation?: Conversation;
  quotaStatus: QuotaStatus | null;
  lang: Language;
  onSendMessage: (content: string) => void;
  isLoading: boolean;
}

export default function ConversationView({
  conversation,
  quotaStatus,
  lang,
  onSendMessage,
  isLoading,
}: ConversationViewProps) {
  const scrollRef = useRef<HTMLDivElement>(null);
  const t = memberLocales[lang];

  const isQuotaExhausted = quotaStatus ? quotaStatus.remaining <= 0 : false;

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTo({
        top: scrollRef.current.scrollHeight,
        behavior: "smooth",
      });
    }
  }, [conversation?.messages, isLoading]);

  const handleRegenerate = () => {
    if (conversation && conversation.messages.length > 1 && !isLoading) {
      const lastUserMsg = [...conversation.messages]
        .reverse()
        .find((m) => m.role === "user");
      if (lastUserMsg) onSendMessage(lastUserMsg.content);
    }
  };

  return (
    <div className="flex flex-col h-full bg-white dark:bg-[#212121] transition-colors overflow-hidden">
      <div ref={scrollRef} className="flex-1 overflow-y-auto scrollbar-hide">
        <div className="w-full max-w-3xl mx-auto py-6 px-4">
          {conversation?.messages.map((msg) => (
            <MessageBubble
              key={msg.id}
              message={msg}
              lang={lang}
              onSuggestionClick={(q) => !isLoading && onSendMessage(q)}
              onRegenerate={handleRegenerate}
            />
          ))}

          {isLoading && (
            <div className="flex items-center gap-3 py-4 text-slate-500 dark:text-slate-400 text-sm">
              <Search className="w-4 h-4 animate-pulse" />
              <span>{t.executingResearch}</span>
            </div>
          )}
        </div>
      </div>

      <div className="shrink-0 bg-white dark:bg-[#212121] px-4 pb-4 pt-2">
        <div className="w-full max-w-3xl mx-auto">
          <ChatInput
            onSend={onSendMessage}
            isLoading={isLoading}
            placeholder={t.placeholder}
            disabled={isQuotaExhausted}
            disabledPlaceholder={t.quotaDisabledPlaceholder}
          />
          <p className="mt-2 text-xs text-center text-slate-400 dark:text-slate-500">
            {t.aiDisclaimer}
          </p>
        </div>
      </div>
    </div>
  );
}
