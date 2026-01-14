// Admin 提示词筛选组件
import type { AdminPromptStats } from "@/common/types";
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import { AdminTagFilter } from "./AdminTagFilter";
import { Button } from "@/libs/shadcn/ui/button";
import { Input } from "@/libs/shadcn/ui/input";

interface AdminPromptsFilterProps {
  stats: AdminPromptStats | null;
  search: string;
  category: string;
  source: string;
  onSearchChange: (value: string) => void;
  onCategoryChange: (value: string) => void;
  onSourceChange: (value: string) => void;
  onReset: () => void;
  getCategoryLabel: (code: string) => string;
  getSourceLabel: (code: string) => string;
}

export function AdminPromptsFilter({
  stats,
  search,
  category,
  source,
  onSearchChange,
  onCategoryChange,
  onSourceChange,
  onReset,
  getCategoryLabel,
  getSourceLabel,
}: AdminPromptsFilterProps) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];
  const hasFilters = search || category !== "__all__" || source !== "__all__";

  return (
    <div className="space-y-4 mb-6">
      {stats && stats.categories.length > 0 && (
        <AdminTagFilter
          label={t.category}
          options={stats.categories
            .filter((c) => c.category)
            .map((c) => ({
              value: c.category,
              label: getCategoryLabel(c.category),
              count: c.count,
            }))}
          value={category}
          onChange={onCategoryChange}
          color="violet"
        />
      )}

      {stats && stats.sources.length > 0 && (
        <AdminTagFilter
          label={t.source}
          options={stats.sources
            .filter((s) => s.source)
            .map((s) => ({
              value: s.source,
              label: getSourceLabel(s.source),
              count: s.count,
            }))}
          value={source}
          onChange={onSourceChange}
          color="blue"
        />
      )}

      <div className="flex items-center gap-2">
        <Input
          type="text"
          placeholder={t.search}
          value={search}
          onChange={(e) => onSearchChange(e.target.value)}
          className="max-w-xs"
        />
        {hasFilters && (
          <Button variant="outline" size="sm" onClick={onReset}>
            {t.reset}
          </Button>
        )}
      </div>
    </div>
  );
}
