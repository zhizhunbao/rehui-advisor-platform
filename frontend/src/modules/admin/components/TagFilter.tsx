import type { Language } from "@/common/i18n";
import { adminLocales } from "@/common/i18n";

export interface TagOption {
  value: string;
  label: string;
  count: number;
}

export type TagColor =
  | "violet"
  | "blue"
  | "emerald"
  | "amber"
  | "rose"
  | "orange";

interface TagFilterProps {
  lang: Language;
  label: string;
  options: TagOption[];
  value: string;
  onChange: (value: string) => void;
  color?: TagColor;
}

const COLOR_CLASSES: Record<TagColor, { active: string; inactive: string }> = {
  violet: {
    active: "bg-violet-600 text-white border-violet-600",
    inactive:
      "bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300 border-slate-200 dark:border-slate-700 hover:border-violet-400 hover:text-violet-600 dark:hover:text-violet-400",
  },
  blue: {
    active: "bg-blue-600 text-white border-blue-600",
    inactive:
      "bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300 border-slate-200 dark:border-slate-700 hover:border-blue-400 hover:text-blue-600 dark:hover:text-blue-400",
  },
  emerald: {
    active: "bg-emerald-600 text-white border-emerald-600",
    inactive:
      "bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300 border-slate-200 dark:border-slate-700 hover:border-emerald-400 hover:text-emerald-600 dark:hover:text-emerald-400",
  },
  amber: {
    active: "bg-amber-600 text-white border-amber-600",
    inactive:
      "bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300 border-slate-200 dark:border-slate-700 hover:border-amber-400 hover:text-amber-600 dark:hover:text-amber-400",
  },
  orange: {
    active: "bg-orange-600 text-white border-orange-600",
    inactive:
      "bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300 border-slate-200 dark:border-slate-700 hover:border-orange-400 hover:text-orange-600 dark:hover:text-orange-400",
  },
  rose: {
    active: "bg-rose-600 text-white border-rose-600",
    inactive:
      "bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300 border-slate-200 dark:border-slate-700 hover:border-rose-400 hover:text-rose-600 dark:hover:text-rose-400",
  },
};

export function TagFilter({
  lang,
  label,
  options,
  value,
  onChange,
  color = "violet",
}: TagFilterProps) {
  const t = adminLocales[lang];
  const colorClass = COLOR_CLASSES[color] || COLOR_CLASSES.violet;
  const isAllSelected = value === "__all__" || value === "";

  return (
    <div className="flex gap-2">
      <span className="text-sm font-medium text-muted-foreground w-24 shrink-0 py-1.5 text-left whitespace-nowrap">
        {label}:
      </span>
      <button
        onClick={() => onChange("__all__")}
        className={`px-3 py-1.5 text-sm rounded-full border transition-all duration-200 shrink-0 self-start ${
          isAllSelected ? colorClass.active : colorClass.inactive
        }`}
      >
        {t.all}
      </button>
      <div className="flex flex-wrap gap-2 items-start">
        {options.map((opt) => (
          <button
            key={opt.value}
            onClick={() => onChange(opt.value)}
            className={`px-3 py-1.5 text-sm rounded-full border transition-all duration-200 ${
              value === opt.value ? colorClass.active : colorClass.inactive
            }`}
          >
            {opt.label}
            <span className="ml-1 opacity-80">({opt.count})</span>
          </button>
        ))}
      </div>
    </div>
  );
}
