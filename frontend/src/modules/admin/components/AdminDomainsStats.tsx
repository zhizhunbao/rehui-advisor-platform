// Admin 领域统计卡片
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import { AdminStatCard } from "./AdminStatCard";

interface Props {
  stats: {
    total: number;
    active: number;
    inactive: number;
    categories: number;
  };
}

export function AdminDomainsStats({ stats }: Props) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  return (
    <div className="grid grid-cols-4 gap-4">
      <AdminStatCard value={stats.total} label={t.total} />
      <AdminStatCard value={stats.active} label={t.active} color="green" />
      <AdminStatCard value={stats.inactive} label={t.inactive} color="muted" />
      <AdminStatCard
        value={stats.categories}
        label={t.domainCategories}
        color="violet"
      />
    </div>
  );
}
