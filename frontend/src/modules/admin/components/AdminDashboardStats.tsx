// Admin 仪表盘统计卡片
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import type { AnalyticsSummary } from "@/common/types";
import { Card, CardContent } from "@/libs/shadcn/ui/card";

interface Props {
  summary: AnalyticsSummary | null;
}

export function AdminDashboardStats({ summary }: Props) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <StatCard title={t.totalUsers} value={summary?.totalUsers ?? 0} />
      <StatCard title={t.totalSessions} value={summary?.totalSessions ?? 0} />
      <StatCard title={t.totalMessages} value={summary?.totalMessages ?? 0} />
      <StatCard title={t.activeToday} value={summary?.activeUsersToday ?? 0} />
    </div>
  );
}

function StatCard({ title, value }: { title: string; value: number }) {
  return (
    <Card>
      <CardContent className="p-4">
        <p className="text-sm text-muted-foreground">{title}</p>
        <p className="text-2xl font-bold text-foreground mt-1">
          {value.toLocaleString()}
        </p>
      </CardContent>
    </Card>
  );
}
