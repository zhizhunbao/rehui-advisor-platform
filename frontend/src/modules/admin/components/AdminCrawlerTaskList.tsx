// Admin 爬虫任务历史组件
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import type { CrawlTask } from "@/common/types";
import { Badge } from "@/libs/shadcn/ui/badge";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/libs/shadcn/ui/card";

interface Props {
  tasks: CrawlTask[];
}

export function AdminCrawlerTaskList({ tasks }: Props) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  return (
    <Card>
      <CardHeader>
        <CardTitle>{t.taskHistory}</CardTitle>
      </CardHeader>
      <CardContent className="p-0">
        <div className="divide-y divide-border max-h-96 overflow-y-auto">
          {tasks.map((task) => (
            <div key={task.id} className="p-4">
              <div className="flex justify-between items-center">
                <StatusBadge status={task.status} />
                <span className="text-sm text-muted-foreground">
                  {task.recordsCount} records
                </span>
              </div>
              <p className="text-xs text-muted-foreground mt-1">
                {task.startedAt && new Date(task.startedAt).toLocaleString()}
              </p>
              {task.errorMessage && (
                <p className="text-xs text-destructive mt-1">
                  {task.errorMessage}
                </p>
              )}
            </div>
          ))}
          {!tasks.length && (
            <div className="p-8 text-center text-muted-foreground">
              {t.noData}
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}

function StatusBadge({ status }: { status: string }) {
  const variantMap: Record<
    string,
    "default" | "secondary" | "destructive" | "outline"
  > = {
    success: "default",
    failed: "destructive",
    running: "secondary",
    pending: "outline",
  };

  return <Badge variant={variantMap[status] ?? "outline"}>{status}</Badge>;
}
