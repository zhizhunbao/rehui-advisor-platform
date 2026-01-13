// Admin LLM 统计组件
import type { Language } from "@/common/types";
import { adminLocales } from "@/common/i18n";
import { AdminStatCard } from "./AdminStatCard";

interface AdminLLMStatsProps {
  lang: Language;
  stats: {
    total: number;
    active: number;
    api: number;
    local: number;
    free: number;
  };
}

export function AdminLLMStats({ lang, stats }: AdminLLMStatsProps) {
  const t = adminLocales[lang];

  return (
    <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
      <AdminStatCard label={t.total} value={stats.total} />
      <AdminStatCard label={t.active} value={stats.active} color="green" />
      <AdminStatCard label={t.apiCall} value={stats.api} color="violet" />
      <AdminStatCard label={t.localDeploy} value={stats.local} color="amber" />
      <AdminStatCard label={t.free} value={stats.free} color="rose" />
    </div>
  );
}
