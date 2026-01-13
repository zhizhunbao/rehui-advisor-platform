// Admin 设置 Hook 和 Provider
import {
  createContext,
  useContext,
  useState,
  useEffect,
  type ReactNode,
} from "react";
import type { Language, AdminSettingsContextValue } from "@/common/types";
import {
  type ThemeName,
  themes,
  applyTheme,
  getStoredTheme,
} from "@/common/themes";

const AdminSettingsContext = createContext<AdminSettingsContextValue | null>(
  null
);

export function useAdminSettings() {
  const ctx = useContext(AdminSettingsContext);
  if (!ctx)
    throw new Error(
      "useAdminSettings must be used within AdminSettingsProvider"
    );
  return ctx;
}

export function AdminSettingsProvider({ children }: { children: ReactNode }) {
  const [lang, setLang] = useState<Language>(
    () => (localStorage.getItem("adminLang") as Language) || "zh"
  );
  const [themeName, setThemeName] = useState<ThemeName>(getStoredTheme);

  useEffect(() => {
    localStorage.setItem("adminLang", lang);
  }, [lang]);

  useEffect(() => {
    applyTheme(themeName);
  }, [themeName]);

  return (
    <AdminSettingsContext.Provider
      value={{
        lang,
        setLang,
        themeName,
        setThemeName,
      }}
    >
      {children}
    </AdminSettingsContext.Provider>
  );
}

export { themes, type ThemeName };
