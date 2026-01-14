// Admin 主题选择器组件
import { useAdminSettingsStore } from "@/common/stores";
import { themes, type ThemeName } from "@/common/themes";

export type { ThemeName };

interface AdminThemeSelectorProps {
  themeName: ThemeName;
  onThemeChange: (theme: ThemeName) => void;
}

export function AdminThemeSelector({
  themeName,
  onThemeChange,
}: AdminThemeSelectorProps) {
  const { lang } = useAdminSettingsStore();
  const shadcnThemes = themes.filter((t) => t.group === "shadcn");
  const editorThemes = themes.filter((t) => t.group === "editor");

  return (
    <div className="relative">
      <select
        value={themeName}
        onChange={(e) => onThemeChange(e.target.value as ThemeName)}
        className="px-3 py-2 rounded-lg text-sm font-medium transition-colors appearance-none cursor-pointer pr-8 bg-secondary hover:bg-secondary/80 text-secondary-foreground border-transparent"
      >
        <optgroup label={lang === "zh" ? "shadcn 主题" : "shadcn Themes"}>
          {shadcnThemes.map((t) => (
            <option
              key={t.name}
              value={t.name}
              className="bg-popover text-popover-foreground"
            >
              {lang === "zh" ? t.label : t.labelEn}
            </option>
          ))}
        </optgroup>
        <optgroup label={lang === "zh" ? "编辑器主题" : "Editor Themes"}>
          {editorThemes.map((t) => (
            <option
              key={t.name}
              value={t.name}
              className="bg-popover text-popover-foreground"
            >
              {lang === "zh" ? t.label : t.labelEn}
            </option>
          ))}
        </optgroup>
      </select>
      <span className="absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none">
        🎨
      </span>
    </div>
  );
}
