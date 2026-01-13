import { useState, useEffect, useCallback } from "react";
import { adminLocales, type Language } from "@/common/i18n";
import { analyticsService } from "@/modules/admin/services/analytics.service";
import type { AnalyticsSummary } from "@/common/types";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/libs/shadcn/ui/card";

interface DashboardViewProps {
  lang: Language;
}

export default function DashboardView({ lang }: DashboardViewProps) {
  const t = adminLocales[lang];
  const [summary, setSummary] = useState<AnalyticsSummary | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const fetchData = useCallback(async () => {
    try {
      const data = await analyticsService.getSummary();
      setSummary(data);
    } catch {
      // 由中间件统一处理
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-full text-muted-foreground">
        {t.loading}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-foreground">{t.dashboard}</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard title={t.totalUsers} value={summary?.totalUsers ?? 0} />
        <StatCard title={t.totalSessions} value={summary?.totalSessions ?? 0} />
        <StatCard title={t.totalMessages} value={summary?.totalMessages ?? 0} />
        <StatCard
          title={t.activeToday}
          value={summary?.activeUsersToday ?? 0}
        />
      </div>

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
