// Admin 布局组件 - Hooks: useAdminSettings, useAdminAuth
import { useState } from "react";
import { Link, useLocation, Outlet } from "react-router-dom";
import { adminLocales } from "@/common/i18n";
import type { Language } from "@/common/types";
import { AdminThemeSelector } from "./AdminThemeSelector";
import type { ThemeName } from "./AdminThemeSelector";

interface Admin {
  name: string;
  email: string;
  role: string;
}

interface AdminLayoutProps {
  admin: Admin | null;
  lang: Language;
  themeName: ThemeName;
  onLogout: () => void;
  onLangChange: (lang: Language) => void;
  onThemeChange: (theme: ThemeName) => void;
}

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

const MENU_CONFIG: MenuConfig = [
  { path: "/admin", label: "dashboard", icon: "📊" },
  { path: "/admin/analytics", label: "analytics", icon: "📈" },
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
  {
    key: "data",
    label: "dataManagement",
    icon: "📦",
    children: [
      { path: "/admin/domains", label: "domains", icon: "🌐" },
      { path: "/admin/data-sources", label: "dataSources", icon: "🔗" },
      { path: "/admin/crawlers", label: "crawlers", icon: "🕷️" },
      { path: "/admin/retrieval", label: "retrieval", icon: "🔍" },
      { path: "/admin/scheduler", label: "scheduler", icon: "📅" },
    ],
  },
  {
    key: "content",
    label: "contentManagement",
    icon: "📝",
    children: [
      { path: "/admin/questions", label: "questions", icon: "❓" },
      { path: "/admin/recommendations", label: "recommendations", icon: "⭐" },
    ],
  },
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

export default function AdminLayout({
  admin,
  lang,
  themeName,
  onLogout,
  onLangChange,
  onThemeChange,
}: AdminLayoutProps) {
  const t = adminLocales[lang];
  const location = useLocation();
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

  const allMenuItems = getAllMenuItems(MENU_CONFIG);
  const isSuperAdmin = admin?.role === "super_admin";

  const getLabel = (key: string): string => {
    const value = t[key as keyof typeof t];
    return typeof value === "string" ? value : key;
  };

  return (
    <div className="min-h-screen flex bg-background">
      <aside
        className={`${
          sidebarOpen ? "w-64" : "w-16"
        } bg-sidebar text-sidebar-foreground transition-all duration-300 flex flex-col sticky top-0 h-screen`}
      >
        <div className="h-16 flex items-center justify-between px-4 border-b border-sidebar-border">
          {sidebarOpen && <span className="font-bold text-lg">{t.title}</span>}
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="p-2 rounded transition-colors hover:bg-sidebar-accent"
          >
            {sidebarOpen ? "◀" : "▶"}
          </button>
        </div>

        <nav className="flex-1 py-4 overflow-y-auto scrollbar-hide">
          {MENU_CONFIG.map((item) => {
            if (item.superAdminOnly && !isSuperAdmin) return null;

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
                          {getLabel(item.label)}
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
                  {sidebarOpen && isExpanded && (
                    <div className="bg-sidebar-accent/30">
                      {item.children
                        .filter(
                          (child) => !child.superAdminOnly || isSuperAdmin
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
                                {getLabel(child.label)}
                              </span>
                            </Link>
                          );
                        })}
                    </div>
                  )}
                </div>
              );
            }

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
                  <span className="ml-3">{getLabel(item.label)}</span>
                )}
              </Link>
            );
          })}
        </nav>

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
                onClick={onLogout}
                className="p-2 rounded text-destructive transition-colors hover:bg-sidebar-accent"
                title={t.logout}
              >
                🚪
              </button>
            </div>
          ) : (
            <button
              onClick={onLogout}
              className="w-full p-2 rounded text-destructive transition-colors hover:bg-sidebar-accent"
              title={t.logout}
            >
              🚪
            </button>
          )}
        </div>
      </aside>

      <main className="flex-1 overflow-auto">
        <header className="h-16 shadow flex items-center justify-between px-6 bg-card border-b border-border">
          <h1 className="text-xl font-semibold text-card-foreground">
            {getLabel(
              allMenuItems.find((m) => m.path === location.pathname)?.label ||
                "dashboard"
            )}
          </h1>
          <div className="flex items-center space-x-4">
            <AdminThemeSelector
              lang={lang}
              themeName={themeName}
              onThemeChange={onThemeChange}
            />
            <button
              onClick={() => onLangChange(lang === "zh" ? "en" : "zh")}
              className="px-3 py-2 rounded-lg text-sm font-medium transition-colors bg-secondary hover:bg-secondary/80 text-secondary-foreground"
            >
              {lang === "zh" ? "EN" : "中文"}
            </button>
            <span className="text-sm text-muted-foreground">
              {admin?.email}
            </span>
          </div>
        </header>
        <div className="p-6 text-foreground">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
