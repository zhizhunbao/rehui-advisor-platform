// Admin 数据分析统计卡片
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import type { AnalyticsSummary } from "@/common/types";

interface Props {
  summary: AnalyticsSummary | null;
}

export function AdminAnalyticsStats({ summary }: Props) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <StatCard
        title={t.totalUsers}
        value={summary?.totalUsers ?? 0}
        color="blue"
      />
      <StatCard
        title={t.totalSessions}
        value={summary?.totalSessions ?? 0}
        color="green"
      />
      <StatCard
        title={t.totalMessages}
        value={summary?.totalMessages ?? 0}
        color="purple"
      />
      <StatCard
        title={t.activeToday}
        value={summary?.activeUsersToday ?? 0}
        color="orange"
      />
    </div>
  );
}

function StatCard({
  title,
  value,
  color,
}: {
  title: string;
  value: number;
  color: "blue" | "green" | "purple" | "orange";
}) {
  const colors = {
    blue: "from-blue-500 to-blue-600",
    green: "from-green-500 to-green-600",
    purple: "from-purple-500 to-purple-600",
    orange: "from-orange-500 to-orange-600",
  };

  return (
    <div
      className={`bg-linear-to-br ${colors[color]} rounded-lg p-4 text-white shadow`}
    >
      <p className="text-sm opacity-90">{title}</p>
      <p className="text-3xl font-bold mt-1">{value.toLocaleString()}</p>
    </div>
  );
}
