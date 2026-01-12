import type { Theme, Language } from "../types";
import { Sun, Moon, Languages } from "lucide-react";

interface HeaderProps {
  lang: Language;
  theme: Theme;
  onToggleLang: () => void;
  onToggleTheme: () => void;
}

const Header: React.FC<HeaderProps> = ({
  lang,
  theme,
  onToggleLang,
  onToggleTheme,
}) => {
  return (
    <header className="fixed top-0 right-0 p-6 z-[100] flex items-center gap-2 pointer-events-none">
      <div className="flex items-center gap-1 pointer-events-auto bg-white/40 dark:bg-black/20 backdrop-blur-xl rounded-2xl px-1.5 py-1.5 shadow-sm border border-slate-200/50 dark:border-white/5">
        <button
          onClick={onToggleTheme}
          className="p-2 rounded-xl hover:bg-white/80 dark:hover:bg-white/10 transition-all text-slate-500 dark:text-slate-400 active:scale-90"
          title="Toggle Theme"
        >
          {theme === "light" ? (
            <Moon className="w-4 h-4" />
          ) : (
            <Sun className="w-4 h-4" />
          )}
        </button>
        <div className="w-px h-4 bg-slate-200 dark:bg-white/10 mx-1"></div>
        <button
          onClick={onToggleLang}
          className="flex items-center gap-2 px-3 py-2 rounded-xl hover:bg-white/80 dark:hover:bg-white/10 transition-all text-slate-500 dark:text-slate-400 text-[10px] font-black uppercase tracking-widest"
          title="Toggle Language"
        >
          <Languages className="w-4 h-4" />
          {lang}
        </button>
      </div>
    </header>
  );
};

export default Header;
