// Member 主布局组件
import type { ReactNode } from "react";
import {
  useAuthStore,
  useMemberSettingsStore,
  useMemberNavigationStore,
  useMemberConversationStore,
} from "@/common/stores";
import MemberSidebar from "./MemberSidebar";
import MemberHeader from "./MemberHeader";
import MemberFooter from "./MemberFooter";

interface MemberLayoutProps {
  children: ReactNode;
}

export default function MemberLayout({ children }: MemberLayoutProps) {
  const { user, quotaStatus, logout } = useAuthStore();
  const { lang, theme, toggleLang, toggleTheme } = useMemberSettingsStore();
  const { view, setView } = useMemberNavigationStore();
  const {
    conversations,
    activeConversationId,
    setActiveConversationId,
    deleteConversation,
    updateConversations,
  } = useMemberConversationStore();

  const isConversationView = view === "conversation";
  const isAuthView = view === "login" || view === "register";
  const showFooter = !isConversationView && !isAuthView;

  const handleSelectConversation = (id: string | null) => {
    setActiveConversationId(id);
    setView(id ? "conversation" : "home");
  };

  const handleNewChat = () => {
    setActiveConversationId(null);
    setView("home");
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("refreshToken");
    sessionStorage.removeItem("sessionToken");
    logout();
    updateConversations(() => []);
    setActiveConversationId(null);
    setView("home");
  };

  return (
    <div className="flex h-screen bg-white dark:bg-admin-bg-dark transition-colors duration-300 overflow-hidden">
      <MemberSidebar
        user={user}
        quotaStatus={quotaStatus}
        lang={lang}
        conversations={conversations}
        activeConversationId={activeConversationId}
        onSelectConversation={handleSelectConversation}
        onNewChat={handleNewChat}
        onDeleteConversation={deleteConversation}
        onNavigate={setView}
        onLogout={handleLogout}
      />

      <div className="flex-1 flex flex-col min-w-0 overflow-hidden relative">
        <MemberHeader
          lang={lang}
          theme={theme}
          onToggleLang={toggleLang}
          onToggleTheme={toggleTheme}
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
