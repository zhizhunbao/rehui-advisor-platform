// Admin 数据源统计组件
import type { DataSourceStats } from "@/common/types";
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import { AdminStatCard } from "./AdminStatCard";

interface AdminDataSourcesStatsProps {
  stats: DataSourceStats | null;
}

export function AdminDataSourcesStats({ stats }: AdminDataSourcesStatsProps) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  if (!stats) return null;

  return (
    <div className="grid grid-cols-5 gap-4">
      <AdminStatCard value={stats.total} label={t.total} />
      <AdminStatCard
        value={stats.byStatus.active || 0}
        label={t.active}
        color="green"
      />
      <AdminStatCard
        value={stats.byType.github || 0}
        label="GitHub"
        color="violet"
      />
      <AdminStatCard value={stats.byType.api || 0} label="API" color="blue" />
      <AdminStatCard
        value={stats.byType.website || 0}
        label="Website"
        color="amber"
      />
    </div>
  );
}
