// Admin 提示词统计卡片组件
import type { Language, AdminPromptStats } from "@/common/types";
import { adminLocales } from "@/common/i18n";
import { AdminStatCard } from "./AdminStatCard";

interface AdminPromptsStatsProps {
  lang: Language;
  stats: AdminPromptStats | null;
}

export function AdminPromptsStats({ lang, stats }: AdminPromptsStatsProps) {
  const t = adminLocales[lang];

  if (!stats) return null;

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      <AdminStatCard value={stats.total} label={t.total} />
      <AdminStatCard value={stats.active} label={t.active} color="green" />
      <AdminStatCard value={stats.inactive} label={t.inactive} color="muted" />
      <AdminStatCard
        value={stats.categories.length}
        label={t.promptCategory}
        color="violet"
      />
    </div>
  );
}
