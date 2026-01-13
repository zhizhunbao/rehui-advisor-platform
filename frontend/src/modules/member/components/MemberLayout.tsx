// Member 主布局组件 - Props: view, user, quotaStatus, lang, theme, conversations, children
import type { ReactNode } from "react";
import type {
  AppView,
  User,
  Conversation,
  Language,
  Theme,
  QuotaStatus,
} from "@/common/types";
import MemberSidebar from "./MemberSidebar";
import MemberHeader from "./MemberHeader";
import MemberFooter from "./MemberFooter";

interface MemberLayoutProps {
  view: AppView;
  user: User | null;
  quotaStatus: QuotaStatus | null;
  lang: Language;
  theme: Theme;
  onNavigate: (view: AppView) => void;
  onLogout: () => void;
  onToggleLang: () => void;
  onToggleTheme: () => void;
  conversations: Conversation[];
  activeConversationId: string | null;
  onSelectConversation: (id: string | null) => void;
  onNewChat: () => void;
  onDeleteConversation: (id: string) => void;
  children: ReactNode;
}

export default function MemberLayout({
  view,
  user,
  quotaStatus,
  lang,
  theme,
  onNavigate,
  onLogout,
  onToggleLang,
  onToggleTheme,
  conversations,
  activeConversationId,
  onSelectConversation,
  onNewChat,
  onDeleteConversation,
  children,
}: MemberLayoutProps) {
  const isConversationView = view === "conversation";
  const isAuthView = view === "login" || view === "register";
  const showFooter = !isConversationView && !isAuthView;

  return (
    <div className="flex h-screen bg-white dark:bg-admin-bg-dark transition-colors duration-300 overflow-hidden">
      <MemberSidebar
        user={user}
        quotaStatus={quotaStatus}
        lang={lang}
        conversations={conversations}
        activeConversationId={activeConversationId}
        onSelectConversation={onSelectConversation}
        onNewChat={onNewChat}
        onDeleteConversation={onDeleteConversation}
        onNavigate={onNavigate}
        onLogout={onLogout}
      />

      <div className="flex-1 flex flex-col min-w-0 overflow-hidden relative">
        <MemberHeader
          lang={lang}
          theme={theme}
          onToggleLang={onToggleLang}
          onToggleTheme={onToggleTheme}
        />

        <main className="flex-1 overflow-y-auto flex flex-col items-center">
          <div className="w-full flex-1 flex flex-col min-h-0">
            <div className="flex-1 w-full flex flex-col">{children}</div>
            {showFooter && (
              <div className="w-full max-w-5xl mx-auto">
                <MemberFooter lang={lang} />
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}
