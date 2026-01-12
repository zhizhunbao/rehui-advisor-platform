import { useState, useEffect } from "react";
import { adminLocales, type Language } from "@/common/i18n";
import { analyticsService } from "@/modules/admin/services/admin.service";
import type { AnalyticsSummary } from "@/modules/admin/types/admin.types";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/libs/shadcn/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/libs/shadcn/ui/table";

interface AnalyticsViewProps {
  lang: Language;
}

export default function AnalyticsView({ lang }: AnalyticsViewProps) {
  const t = adminLocales[lang];
  const [summary, setSummary] = useState<AnalyticsSummary | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await analyticsService.getSummary();
        setSummary(data);
      } catch {
        // Handle error
      } finally {
        setIsLoading(false);
      }
    };
    fetchData();
  }, []);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-full text-muted-foreground">
        {t.loading}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-foreground">{t.analytics}</h1>

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

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>{t.popularDomains}</CardTitle>
          </CardHeader>
          <CardContent>
            {summary?.popularDomains?.length ? (
              <div className="space-y-3">
                {summary.popularDomains.map((d, i) => (
                  <div key={i} className="flex items-center">
                    <div className="flex-1">
                      <div className="flex justify-between mb-1">
                        <span className="text-sm text-foreground">
                          {d.domainId}
                        </span>
                        <span className="text-sm text-muted-foreground">
                          {d.count}
                        </span>
                      </div>
                      <div className="w-full bg-muted rounded-full h-2">
                        <div
                          className="bg-primary h-2 rounded-full"
                          style={{
                            width: `${
                              (d.count /
                                Math.max(
                                  ...summary.popularDomains.map((x) => x.count)
                                )) *
                              100
                            }%`,
                          }}
                        />
                      </div>
                    </div>
                  </div>
                ))}
              </div>
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
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>{t.date}</TableHead>
                    <TableHead>{t.sessions}</TableHead>
                    <TableHead>{t.messages}</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {summary.recentActivity.map((a, i) => (
                    <TableRow key={i}>
                      <TableCell>{a.date}</TableCell>
                      <TableCell>{a.sessions}</TableCell>
                      <TableCell>{a.messages}</TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            ) : (
              <p className="text-muted-foreground">{t.noData}</p>
            )}
          </CardContent>
        </Card>
      </div>
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
      className={`bg-gradient-to-br ${colors[color]} rounded-lg p-4 text-white shadow`}
    >
      <p className="text-sm opacity-90">{title}</p>
      <p className="text-3xl font-bold mt-1">{value.toLocaleString()}</p>
    </div>
  );
}
