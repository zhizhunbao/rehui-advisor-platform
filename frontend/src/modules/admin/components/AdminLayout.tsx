import { useState } from "react";
import { Link, useLocation, Outlet } from "react-router-dom";
import { useAdminAuth } from "../context/AdminAuthContext";
import { useAdminSettings } from "../context/AdminSettingsContext";
import { adminLocales } from "../locales";
import ThemeSelector from "./ThemeSelector";

interface MenuItem {
  path: string;
  label: string;
  icon: string;
  superAdminOnly?: boolean;
}

interface MenuGroup {
  key: string;
  label: string;
  icon: string;
  children: MenuItem[];
  superAdminOnly?: boolean;
}

type MenuConfig = (MenuItem | MenuGroup)[];

const menuConfig: MenuConfig = [
  // 独立菜单项
  { path: "/admin", label: "dashboard", icon: "📊" },
  { path: "/admin/analytics", label: "analytics", icon: "📈" },

  // AI 核心
  {
    key: "ai",
    label: "aiCore",
    icon: "🤖",
    children: [
      { path: "/admin/llm", label: "llm", icon: "🧠" },
      { path: "/admin/prompts", label: "prompts", icon: "💬" },
      { path: "/admin/skills", label: "skills", icon: "🧩" },
      { path: "/admin/agent-frameworks", label: "agentFrameworks", icon: "🤝" },
    ],
  },

  // 数据管理
  {
    key: "data",
    label: "dataManagement",
    icon: "📦",
    children: [
      { path: "/admin/domains", label: "domains", icon: "🌐" },
      { path: "/admin/data-sources", label: "dataSources", icon: "🔗" },
      { path: "/admin/crawlers", label: "crawlers", icon: "🕷️" },
      { path: "/admin/retrieval", label: "retrieval", icon: "🔍" },
      { path: "/admin/scheduler", label: "scheduler", icon: "⏰" },
    ],
  },

  // 内容管理
  {
    key: "content",
    label: "contentManagement",
    icon: "📝",
    children: [
      { path: "/admin/questions", label: "questions", icon: "❓" },
      { path: "/admin/recommendations", label: "recommendations", icon: "⭐" },
    ],
  },

  // 用户与订阅
  {
    key: "users",
    label: "userManagement",
    icon: "👥",
    children: [
      { path: "/admin/users", label: "users", icon: "👤" },
      { path: "/admin/conversations", label: "conversations", icon: "💭" },
      { path: "/admin/subscriptions", label: "subscriptions", icon: "💳" },
    ],
  },

  // 系统设置
  {
    path: "/admin/configs",
    label: "configs",
    icon: "⚙️",
    superAdminOnly: true,
  },
];

function isMenuGroup(item: MenuItem | MenuGroup): item is MenuGroup {
  return "children" in item;
}

function getAllMenuItems(config: MenuConfig): MenuItem[] {
  const items: MenuItem[] = [];
  for (const item of config) {
    if (isMenuGroup(item)) {
      items.push(...item.children);
    } else {
      items.push(item);
    }
  }
  return items;
}

export default function AdminLayout() {
  const { lang, setLang } = useAdminSettings();
  const t = adminLocales[lang];
  const location = useLocation();
  const { admin, logout } = useAdminAuth();
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [expandedGroups, setExpandedGroups] = useState<string[]>([
    "ai",
    "data",
  ]);

  const toggleGroup = (key: string) => {
    setExpandedGroups((prev) =>
      prev.includes(key) ? prev.filter((k) => k !== key) : [...prev, key]
    );
  };

  const isGroupActive = (group: MenuGroup) => {
    return group.children.some((child) => location.pathname === child.path);
  };

  const allMenuItems = getAllMenuItems(menuConfig);

  return (
    <div className="min-h-screen flex bg-background">
      {/* Sidebar */}
      <aside
        className={`${
          sidebarOpen ? "w-64" : "w-16"
        } bg-sidebar text-sidebar-foreground transition-all duration-300 flex flex-col sticky top-0 h-screen`}
      >
        {/* Logo */}
        <div className="h-16 flex items-center justify-between px-4 border-b border-sidebar-border">
          {sidebarOpen && <span className="font-bold text-lg">{t.title}</span>}
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="p-2 rounded transition-colors hover:bg-sidebar-accent"
          >
            {sidebarOpen ? "◀" : "▶"}
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 py-4 overflow-y-auto scrollbar-hide">
          {menuConfig.map((item) => {
            // 权限过滤
            if (item.superAdminOnly && admin?.role !== "super_admin") {
              return null;
            }

            // 菜单组
            if (isMenuGroup(item)) {
              const isExpanded = expandedGroups.includes(item.key);
              const isActive = isGroupActive(item);

              return (
                <div key={item.key}>
                  <button
                    onClick={() => sidebarOpen && toggleGroup(item.key)}
                    className={`w-full flex items-center px-4 py-3 transition-colors ${
                      isActive
                        ? "bg-sidebar-accent/50 text-primary"
                        : "hover:bg-sidebar-accent"
                    }`}
                  >
                    <span className="text-xl">{item.icon}</span>
                    {sidebarOpen && (
                      <>
                        <span className="ml-3 flex-1 text-left">
                          {t[item.label as keyof typeof t] || item.label}
                        </span>
                        <span
                          className={`transition-transform duration-200 ${
                            isExpanded ? "rotate-90" : ""
                          }`}
                        >
                          ▶
                        </span>
                      </>
                    )}
                  </button>

                  {/* 子菜单 */}
                  {sidebarOpen && isExpanded && (
                    <div className="bg-sidebar-accent/30">
                      {item.children
                        .filter(
                          (child) =>
                            !child.superAdminOnly ||
                            admin?.role === "super_admin"
                        )
                        .map((child) => {
                          const isChildActive =
                            location.pathname === child.path;
                          return (
                            <Link
                              key={child.path}
                              to={child.path}
                              className={`flex items-center pl-10 pr-4 py-2.5 transition-colors text-sm ${
                                isChildActive
                                  ? "bg-sidebar-accent border-l-4 border-primary text-primary"
                                  : "hover:bg-sidebar-accent"
                              }`}
                            >
                              <span className="text-base">{child.icon}</span>
                              <span className="ml-2">
                                {t[child.label as keyof typeof t] ||
                                  child.label}
                              </span>
                            </Link>
                          );
                        })}
                    </div>
                  )}
                </div>
              );
            }

            // 独立菜单项
            const isActive = location.pathname === item.path;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center px-4 py-3 transition-colors ${
                  isActive
                    ? "bg-sidebar-accent border-l-4 border-primary"
                    : "hover:bg-sidebar-accent"
                }`}
              >
                <span className="text-xl">{item.icon}</span>
                {sidebarOpen && (
                  <span className="ml-3">
                    {t[item.label as keyof typeof t] || item.label}
                  </span>
                )}
              </Link>
            );
          })}
        </nav>

        {/* User Info */}
        <div className="border-t border-sidebar-border p-4">
          {sidebarOpen ? (
            <div className="flex items-center justify-between">
              <div>
                <div className="font-medium">{admin?.name}</div>
                <div className="text-sm text-muted-foreground">
                  {admin?.role}
                </div>
              </div>
              <button
                onClick={logout}
                className="p-2 rounded text-destructive transition-colors hover:bg-sidebar-accent"
                title={t.logout}
              >
                🚪
              </button>
            </div>
          ) : (
            <button
              onClick={logout}
              className="w-full p-2 rounded text-destructive transition-colors hover:bg-sidebar-accent"
              title={t.logout}
            >
              🚪
            </button>
          )}
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-auto">
        {/* Top Bar */}
        <header className="h-16 shadow flex items-center justify-between px-6 bg-card border-b border-border">
          <h1 className="text-xl font-semibold text-card-foreground">
            {t[
              allMenuItems.find((m) => m.path === location.pathname)
                ?.label as keyof typeof t
            ] || t.dashboard}
          </h1>
          <div className="flex items-center space-x-4">
            {/* Theme Selector */}
            <ThemeSelector lang={lang} />

            {/* Language Toggle */}
            <button
              onClick={() => setLang(lang === "zh" ? "en" : "zh")}
              className="px-3 py-2 rounded-lg text-sm font-medium transition-colors bg-secondary hover:bg-secondary/80 text-secondary-foreground"
            >
              {lang === "zh" ? "EN" : "中文"}
            </button>

            <span className="text-sm text-muted-foreground">
              {admin?.email}
            </span>
          </div>
        </header>

        {/* Page Content */}
        <div className="p-6 text-foreground">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
