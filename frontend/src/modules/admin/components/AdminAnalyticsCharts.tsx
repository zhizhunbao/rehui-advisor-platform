// Admin 数据分析图表区域
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import type { AnalyticsSummary } from "@/common/types";
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

interface Props {
  summary: AnalyticsSummary | null;
}

export function AdminAnalyticsCharts({ summary }: Props) {
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
  );
}
