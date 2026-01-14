// Admin 技能统计卡片组件
import type { SkillStats } from "@/common/types";
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import { AdminStatCard } from "./AdminStatCard";

interface AdminSkillsStatsProps {
  stats: SkillStats | null;
}

export function AdminSkillsStats({ stats }: AdminSkillsStatsProps) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  if (!stats) return null;

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      <AdminStatCard value={stats.total} label={t.totalSkills} />
      <AdminStatCard
        value={stats.active}
        label={t.activeSkills}
        color="green"
      />
      <AdminStatCard
        value={stats.inactive}
        label={t.inactiveSkills}
        color="muted"
      />
      <AdminStatCard
        value={stats.categories.length}
        label={t.skillCategory}
        color="violet"
      />
    </div>
  );
}
