// Admin 布局组件
import { useState } from "react";
import { Link, useLocation, Outlet } from "react-router-dom";
import { useAdminSettingsStore, useAdminAuthStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import { ADMIN_MENU_CONFIG } from "@/common/enum";
import { isAdminMenuGroup, getAllAdminMenuItems } from "@/common/helper";
import type { AdminAuthUser, AdminMenuGroup } from "@/common/types";
import { AdminThemeSelector } from "./AdminThemeSelector";

export default function AdminLayout() {
  const { admin, logout } = useAdminAuthStore();
  const { lang, themeName, setLang, setThemeName } = useAdminSettingsStore();
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

  const isGroupActive = (group: AdminMenuGroup) => {
    return group.children.some((child) => location.pathname === child.path);
  };

  const allMenuItems = getAllAdminMenuItems(ADMIN_MENU_CONFIG);
  const isSuperAdmin = admin?.role === "super_admin";

  const getLabel = (key: string): string => {
    const value = t[key as keyof typeof t];
    return typeof value === "string" ? value : key;
  };

  return (
    <div className="min-h-screen flex bg-background">
      <AdminSidebar
        sidebarOpen={sidebarOpen}
        expandedGroups={expandedGroups}
        isSuperAdmin={isSuperAdmin}
        admin={admin}
        currentPath={location.pathname}
        t={t}
        onToggleSidebar={() => setSidebarOpen(!sidebarOpen)}
        onToggleGroup={toggleGroup}
        onLogout={logout}
        isGroupActive={isGroupActive}
        getLabel={getLabel}
      />

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
              themeName={themeName}
              onThemeChange={setThemeName}
            />
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
        <div className="p-6 text-foreground">
          <Outlet />
        </div>
      </main>
    </div>
  );
}

interface AdminSidebarProps {
  sidebarOpen: boolean;
  expandedGroups: string[];
  isSuperAdmin: boolean;
  admin: AdminAuthUser | null;
  currentPath: string;
  t: typeof adminLocales.zh | typeof adminLocales.en;
  onToggleSidebar: () => void;
  onToggleGroup: (key: string) => void;
  onLogout: () => void;
  isGroupActive: (group: AdminMenuGroup) => boolean;
  getLabel: (key: string) => string;
}

function AdminSidebar({
  sidebarOpen,
  expandedGroups,
  isSuperAdmin,
  admin,
  currentPath,
  t,
  onToggleSidebar,
  onToggleGroup,
  onLogout,
  isGroupActive,
  getLabel,
}: AdminSidebarProps) {
  return (
    <aside
      className={`${
        sidebarOpen ? "w-64" : "w-16"
      } bg-sidebar text-sidebar-foreground transition-all duration-300 flex flex-col sticky top-0 h-screen`}
    >
      <div className="h-16 flex items-center justify-between px-4 border-b border-sidebar-border">
        {sidebarOpen && <span className="font-bold text-lg">{t.title}</span>}
        <button
          onClick={onToggleSidebar}
          className="p-2 rounded transition-colors hover:bg-sidebar-accent"
        >
          {sidebarOpen ? "◀" : "▶"}
        </button>
      </div>

      <nav className="flex-1 py-4 overflow-y-auto scrollbar-hide">
        {ADMIN_MENU_CONFIG.map((item) => {
          if (item.superAdminOnly && !isSuperAdmin) return null;

          if (isAdminMenuGroup(item)) {
            const isExpanded = expandedGroups.includes(item.key);
            const isActive = isGroupActive(item);

            return (
              <div key={item.key}>
                <button
                  onClick={() => sidebarOpen && onToggleGroup(item.key)}
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
                      .filter((child) => !child.superAdminOnly || isSuperAdmin)
                      .map((child) => {
                        const isChildActive = currentPath === child.path;
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

          const isActive = currentPath === item.path;
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
              <div className="text-sm text-muted-foreground">{admin?.role}</div>
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
  );
}
