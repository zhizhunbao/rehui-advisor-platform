// Admin 仪表盘图表区域
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import type { AnalyticsSummary } from "@/common/types";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/libs/shadcn/ui/card";

interface Props {
  summary: AnalyticsSummary | null;
}

export function AdminDashboardCharts({ summary }: Props) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <Card>
        <CardHeader>
          <CardTitle>{t.popularDomains}</CardTitle>
        </CardHeader>
        <CardContent>
          {summary?.popularDomains?.length ? (
            <ul className="space-y-2">
              {summary.popularDomains.map((d, i) => (
                <li key={i} className="flex justify-between">
                  <span className="text-foreground">{d.domainId}</span>
                  <span className="text-muted-foreground">{d.count}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-muted-foreground">{t.noData}</p>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>{t.recentActivity}</CardTitle>
        </CardHeader>
        <CardContent>
          {summary?.recentActivity?.length ? (
            <ul className="space-y-2">
              {summary.recentActivity.map((a, i) => (
                <li key={i} className="flex justify-between text-sm">
                  <span className="text-foreground">{a.date}</span>
                  <span className="text-muted-foreground">
                    {a.sessions} sessions / {a.messages} messages
                  </span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-muted-foreground">{t.noData}</p>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
