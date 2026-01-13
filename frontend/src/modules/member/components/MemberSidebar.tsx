// Member 侧边栏组件 - Props: user, quotaStatus, lang, conversations, onSelectConversation, onNewChat
import { useState, useMemo } from "react";
import type {
  Conversation,
  User,
  Language,
  AppView,
  QuotaStatus,
} from "@/common/types";
import {
  Trash2,
  PanelLeftClose,
  PanelLeftOpen,
  User as UserIcon,
  LogOut,
  SquarePen,
  MessageSquare,
  Compass,
} from "lucide-react";
import { advisorLocales } from "@/common/i18n";

interface MemberSidebarProps {
  user: User | null;
  quotaStatus: QuotaStatus | null;
  lang: Language;
  conversations: Conversation[];
  activeConversationId: string | null;
  onSelectConversation: (id: string | null) => void;
  onNewChat: () => void;
  onDeleteConversation: (id: string) => void;
  onNavigate: (view: AppView) => void;
  onLogout: () => void;
}

const MemberSidebar: React.FC<MemberSidebarProps> = ({
  user,
  quotaStatus,
  lang,
  conversations,
  activeConversationId,
  onSelectConversation,
  onNewChat,
  onDeleteConversation,
  onNavigate,
  onLogout,
}) => {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const t = advisorLocales[lang];

  const displayName = user?.name || user?.email?.split("@")[0] || "User";
  const displayInitial = displayName.charAt(0).toUpperCase();

  const groupedConversations = useMemo(() => {
    const groups: Record<string, Conversation[]> = {
      [t.today]: [],
      [t.yesterday]: [],
      [t.earlier]: [],
    };
    const now = new Date();
    const todayStart = new Date(
      now.getFullYear(),
      now.getMonth(),
      now.getDate()
    ).getTime();
    const yesterdayStart = todayStart - 86400000;

    conversations.forEach((conv) => {
      if (conv.updatedAt >= todayStart) groups[t.today].push(conv);
      else if (conv.updatedAt >= yesterdayStart) groups[t.yesterday].push(conv);
      else groups[t.earlier].push(conv);
    });
    return groups;
  }, [conversations, t.today, t.yesterday, t.earlier]);

  const handleGoHome = () => {
    onNavigate("home");
    onSelectConversation(null);
  };

  return (
    <aside
      className={`relative h-full bg-[#f9f9f9] dark:bg-[#171717] flex flex-col shrink-0 z-70 transition-all duration-300 ease-in-out ${
        isCollapsed ? "w-[68px]" : "w-[260px]"
      }`}
    >
      <div className="h-[52px] flex items-center px-3 shrink-0">
        {isCollapsed ? (
          <div className="flex flex-col items-center w-full">
            <button
              onClick={() => setIsCollapsed(false)}
              className="w-10 h-10 flex items-center justify-center text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white hover:bg-slate-200/70 dark:hover:bg-white/10 rounded-lg transition-colors"
            >
              <PanelLeftOpen className="w-5 h-5" />
            </button>
          </div>
        ) : (
          <div className="flex items-center justify-between w-full">
            <button
              onClick={() => setIsCollapsed(true)}
              className="w-10 h-10 flex items-center justify-center text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white hover:bg-slate-200/70 dark:hover:bg-white/10 rounded-lg transition-colors"
            >
              <PanelLeftClose className="w-5 h-5" />
            </button>
            <button
              onClick={onNewChat}
              className="w-10 h-10 flex items-center justify-center text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white hover:bg-slate-200/70 dark:hover:bg-white/10 rounded-lg transition-colors"
            >
              <SquarePen className="w-5 h-5" />
            </button>
          </div>
        )}
      </div>

      <div className={`px-3 mb-3 ${isCollapsed ? "flex justify-center" : ""}`}>
        {isCollapsed ? (
          <button
            onClick={handleGoHome}
            className="w-10 h-10 flex items-center justify-center bg-slate-900 dark:bg-white rounded-full hover:scale-105 transition-transform"
          >
            <Compass className="w-5 h-5 text-white dark:text-black" />
          </button>
        ) : (
          <button
            onClick={handleGoHome}
            className="w-full flex items-center gap-3 px-3 py-2.5 hover:bg-slate-200/70 dark:hover:bg-white/10 rounded-lg transition-colors group"
          >
            <div className="w-8 h-8 bg-slate-900 dark:bg-white rounded-full flex items-center justify-center shrink-0 group-hover:scale-105 transition-transform">
              <Compass className="w-4 h-4 text-white dark:text-black" />
            </div>
            <span className="text-sm font-semibold text-slate-900 dark:text-white">
              {t.brandName}
            </span>
          </button>
        )}
      </div>

      <div className="flex-1 overflow-y-auto px-2 space-y-1 scrollbar-hide">
        {isCollapsed ? (
          <div className="flex flex-col items-center gap-1">
            {conversations.slice(0, 8).map((conv) => (
              <button
                key={conv.id}
                onClick={() => onSelectConversation(conv.id)}
                className={`w-10 h-10 flex items-center justify-center rounded-lg transition-colors ${
                  activeConversationId === conv.id
                    ? "bg-slate-200 dark:bg-white/15 text-slate-900 dark:text-white"
                    : "text-slate-500 dark:text-slate-400 hover:bg-slate-200/70 dark:hover:bg-white/10"
                }`}
              >
                <MessageSquare className="w-4 h-4" />
              </button>
            ))}
          </div>
        ) : (
          Object.entries(groupedConversations).map(
            ([label, list]) =>
              (list as Conversation[]).length > 0 && (
                <div key={label} className="mb-4">
                  <div className="px-3 py-2 text-xs font-medium text-slate-400 dark:text-slate-500">
                    {label}
                  </div>
                  {(list as Conversation[]).map((conv) => (
                    <div
                      key={conv.id}
                      onClick={() => onSelectConversation(conv.id)}
                      className={`group relative flex items-center rounded-lg px-3 py-2.5 cursor-pointer transition-colors text-sm ${
                        activeConversationId === conv.id
                          ? "bg-slate-200/80 dark:bg-white/15 text-slate-900 dark:text-white"
                          : "hover:bg-slate-200/50 dark:hover:bg-white/10 text-slate-700 dark:text-slate-300"
                      }`}
                    >
                      <span className="flex-1 truncate pr-6">{conv.title}</span>
                      <button
                        className="absolute right-2 opacity-0 group-hover:opacity-100 p-1 text-slate-400 hover:text-rose-500 transition-all"
                        onClick={(e) => {
                          e.stopPropagation();
                          onDeleteConversation(conv.id);
                        }}
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  ))}
                </div>
              )
          )
        )}
      </div>

      <div className="p-3 border-t border-slate-200/80 dark:border-white/10 shrink-0">
        {user ? (
          isCollapsed ? (
            <div className="flex flex-col items-center gap-2">
              <div className="w-9 h-9 rounded-full bg-linear-to-br from-violet-500 to-purple-600 flex items-center justify-center text-white text-sm font-medium">
                {displayInitial}
              </div>
              <button
                onClick={onLogout}
                className="p-2 text-slate-400 hover:text-rose-500 transition-colors"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          ) : (
            <div className="flex items-center gap-3 p-2 rounded-xl hover:bg-slate-200/70 dark:hover:bg-white/10 transition-colors cursor-pointer">
              <div className="w-9 h-9 rounded-full bg-linear-to-br from-violet-500 to-purple-600 flex items-center justify-center text-white text-sm font-medium shrink-0">
                {displayInitial}
              </div>
              <div className="flex-1 min-w-0">
                <div className="text-sm font-medium text-slate-900 dark:text-white truncate">
                  {displayName}
                </div>
                <div
                  className={`text-xs ${
                    (quotaStatus?.remaining ?? 0) <= 3
                      ? "text-amber-500 dark:text-amber-400 font-medium"
                      : "text-slate-500 dark:text-slate-400"
                  }`}
                >
                  {t.quotaLeft}: {quotaStatus?.remaining ?? 0}/
                  {quotaStatus?.searchLimit ?? 20}
                </div>
              </div>
              <button
                onClick={onLogout}
                className="p-1.5 text-slate-400 hover:text-rose-500 transition-colors"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          )
        ) : isCollapsed ? (
          <button
            onClick={() => onNavigate("login")}
            className="w-10 h-10 mx-auto flex items-center justify-center rounded-full bg-slate-200 dark:bg-white/10 text-slate-500 dark:text-slate-400 hover:bg-slate-300 dark:hover:bg-white/20 transition-colors"
          >
            <UserIcon className="w-4 h-4" />
          </button>
        ) : (
          <button
            onClick={() => onNavigate("login")}
            className="flex items-center gap-3 w-full p-2 rounded-xl hover:bg-slate-200/70 dark:hover:bg-white/10 transition-colors"
          >
            <div className="w-9 h-9 rounded-full bg-slate-200 dark:bg-white/10 flex items-center justify-center shrink-0">
              <UserIcon className="w-4 h-4 text-slate-500 dark:text-slate-400" />
            </div>
            <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
              {t.login}
            </span>
          </button>
        )}
      </div>
    </aside>
  );
};

export default MemberSidebar;
