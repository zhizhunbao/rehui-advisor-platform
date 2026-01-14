// Member 对话容器组件
import type { RefObject } from "react";
import type {
  Conversation,
  Language,
  Message,
  QuotaStatus,
} from "@/common/types";
import { advisorLocales } from "@/common/i18n";
import { Search } from "lucide-react";
import MemberMessageBubble from "./MemberMessageBubble";
import MemberChatInput from "./MemberChatInput";

interface MemberConversationContainerProps {
  lang: Language;
  conversation: Conversation | undefined;
  quotaStatus: QuotaStatus | null;
  isLoading: boolean;
  isQuotaExhausted: boolean;
  scrollRef: RefObject<HTMLDivElement | null>;
  handleSend: (content: string) => void;
  handleRegenerate: () => void;
}

export function MemberConversationContainer({
  lang,
  conversation,
  isLoading,
  isQuotaExhausted,
  scrollRef,
  handleSend,
  handleRegenerate,
}: MemberConversationContainerProps) {
  const t = advisorLocales[lang];

  return (
    <div className="flex flex-col h-full bg-white dark:bg-slate-900 transition-colors overflow-hidden">
      <div ref={scrollRef} className="flex-1 overflow-y-auto scrollbar-hide">
        <div className="w-full max-w-3xl mx-auto py-6 px-4">
          {conversation?.messages.map((msg: Message) => (
            <MemberMessageBubble
              key={msg.id}
              message={msg}
              lang={lang}
              onSuggestionClick={handleSend}
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

      <div className="shrink-0 bg-white dark:bg-slate-900 px-4 pb-4 pt-2">
        <div className="w-full max-w-3xl mx-auto">
          <MemberChatInput
            onSend={handleSend}
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
