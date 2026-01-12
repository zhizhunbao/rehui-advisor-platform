import Header from "./Header";
import Footer from "./Footer";
import Sidebar from "./Sidebar";
import type {
  AppView,
  User,
  Conversation,
  Language,
  Theme,
  QuotaStatus,
} from "../types";

interface LayoutProps {
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
  children: React.ReactNode;
}

export default function Layout({
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
}: LayoutProps) {
  const isConversationView = view === "conversation";
  const isAuthView = view === "login" || view === "register";
  const showFooter = !isConversationView && !isAuthView;

  return (
    <div className="flex h-screen bg-white dark:bg-[#212121] transition-colors duration-300 overflow-hidden">
      <Sidebar
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
        <Header
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
                <Footer lang={lang} />
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}
