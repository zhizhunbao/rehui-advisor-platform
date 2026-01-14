// Admin 检索引擎筛选组件
import type { RetrievalEngine } from "@/common/types";
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import { RetrievalEngineTypeConfig } from "@/common/enum";
import { AdminTagFilter } from "./AdminTagFilter";
import { Button } from "@/libs/shadcn/ui/button";

interface AdminRetrievalFilterProps {
  engines: RetrievalEngine[];
  filterType: string;
  onFilterTypeChange: (type: string) => void;
  filterStatus: string;
  onFilterStatusChange: (status: string) => void;
  onReset: () => void;
}

export function AdminRetrievalFilter({
  engines,
  filterType,
  onFilterTypeChange,
  filterStatus,
  onFilterStatusChange,
  onReset,
}: AdminRetrievalFilterProps) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  const typeCounts = Object.keys(RetrievalEngineTypeConfig)
    .map((type) => ({
      value: type,
      label: `${RetrievalEngineTypeConfig[type].icon} ${type}`,
      count: engines.filter((e) => e.type === type).length,
    }))
    .filter((item) => item.count > 0);

  const statusCounts = [
    {
      value: "active",
      label: t.active,
      count: engines.filter((e) => e.isActive).length,
    },
    {
      value: "inactive",
      label: t.inactive,
      count: engines.filter((e) => !e.isActive).length,
    },
  ].filter((s) => s.count > 0);

  const hasFilters = filterType || filterStatus;

  return (
    <div className="space-y-2">
      {typeCounts.length > 0 && (
        <AdminTagFilter
          label={t.type}
          options={typeCounts}
          value={filterType || "__all__"}
          onChange={(v) => onFilterTypeChange(v === "__all__" ? "" : v)}
          color="violet"
        />
      )}
      {statusCounts.length > 1 && (
        <AdminTagFilter
          label={t.status}
          options={statusCounts}
          value={filterStatus || "__all__"}
          onChange={(v) => onFilterStatusChange(v === "__all__" ? "" : v)}
          color="emerald"
        />
      )}
      {hasFilters && (
        <Button variant="outline" size="sm" onClick={onReset}>
          {t.reset}
        </Button>
      )}
    </div>
  );
}
