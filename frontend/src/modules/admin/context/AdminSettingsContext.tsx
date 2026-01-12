import {
  createContext,
  useContext,
  useState,
  useEffect,
  ReactNode,
} from "react";
import type { Language } from "@/modules/member/types";
import {
  type ThemeName,
  themes,
  applyTheme,
  getStoredTheme,
} from "@/common/themes";

interface AdminSettingsContextValue {
  lang: Language;
  setLang: (lang: Language) => void;
  themeName: ThemeName;
  setThemeName: (name: ThemeName) => void;
}

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

interface AdminSettingsProviderProps {
  children: ReactNode;
}

export function AdminSettingsProvider({
  children,
}: AdminSettingsProviderProps) {
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
