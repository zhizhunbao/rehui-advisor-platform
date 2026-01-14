// Admin 技能筛选组件
import type { SkillStats } from "@/common/types";
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import { AdminTagFilter } from "./AdminTagFilter";
import { Button } from "@/libs/shadcn/ui/button";
import { Input } from "@/libs/shadcn/ui/input";

interface AdminSkillsFilterProps {
  stats: SkillStats | null;
  search: string;
  filterCategory: string;
  filterSource: string;
  onSearchChange: (value: string) => void;
  onCategoryChange: (value: string) => void;
  onSourceChange: (value: string) => void;
  onReset: () => void;
  getCategoryLabel: (code: string) => string;
  getSourceLabel: (code: string) => string;
}

export function AdminSkillsFilter({
  stats,
  search,
  filterCategory,
  filterSource,
  onSearchChange,
  onCategoryChange,
  onSourceChange,
  onReset,
  getCategoryLabel,
  getSourceLabel,
}: AdminSkillsFilterProps) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];
  const hasFilters =
    search || filterCategory !== "__all__" || filterSource !== "__all__";

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
          value={filterCategory}
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
          value={filterSource}
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
