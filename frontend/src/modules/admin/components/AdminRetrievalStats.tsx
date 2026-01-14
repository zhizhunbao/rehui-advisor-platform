// Admin 检索引擎统计组件
import type { RetrievalEngine } from "@/common/types";
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import { AdminStatCard } from "./AdminStatCard";

interface AdminRetrievalStatsProps {
  engines: RetrievalEngine[];
  activeCount: number;
  defaultEngine: RetrievalEngine | undefined;
}

export function AdminRetrievalStats({
  engines,
  activeCount,
  defaultEngine,
}: AdminRetrievalStatsProps) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
      <AdminStatCard label={t.total} value={engines.length} />
      <AdminStatCard label={t.active} value={activeCount} color="green" />
      <AdminStatCard
        label={t.defaultEngine}
        value={defaultEngine?.displayName || "-"}
        color="violet"
      />
    </div>
  );
}
