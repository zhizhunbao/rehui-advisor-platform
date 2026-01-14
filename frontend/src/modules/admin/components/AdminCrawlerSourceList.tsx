// Admin 爬虫源列表组件
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import type { CrawlSource } from "@/common/types";
import { Button } from "@/libs/shadcn/ui/button";
import { Badge } from "@/libs/shadcn/ui/badge";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/libs/shadcn/ui/card";

interface Props {
  sources: CrawlSource[];
  selectedSourceId: string | null;
  onSelect: (id: string) => void;
  onRun: (id: string) => void;
  onDelete: (id: string) => void;
}

export function AdminCrawlerSourceList({
  sources,
  selectedSourceId,
  onSelect,
  onRun,
  onDelete,
}: Props) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  return (
    <Card>
      <CardHeader>
        <CardTitle>{t.crawlSource}</CardTitle>
      </CardHeader>
      <CardContent className="p-0">
        <div className="divide-y divide-border">
          {sources.map((source) => (
            <div
              key={source.id}
              className={`p-4 cursor-pointer hover:bg-muted/50 transition-colors ${
                selectedSourceId === source.id ? "bg-muted" : ""
              }`}
              onClick={() => onSelect(source.id)}
            >
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-medium text-foreground">{source.name}</h3>
                  <p className="text-sm text-muted-foreground truncate max-w-xs">
                    {source.url}
                  </p>
                </div>
                <div className="flex items-center space-x-2">
                  <StatusBadge status={source.lastStatus} />
                  <Button
                    variant="link"
                    size="sm"
                    onClick={(e) => {
                      e.stopPropagation();
                      onRun(source.id);
                    }}
                  >
                    {t.runNow}
                  </Button>
                  <Button
                    variant="link"
                    size="sm"
                    className="text-destructive"
                    onClick={(e) => {
                      e.stopPropagation();
                      onDelete(source.id);
                    }}
                  >
                    {t.delete}
                  </Button>
                </div>
              </div>
              {source.lastRunAt && (
                <p className="text-xs text-muted-foreground mt-1">
                  {t.crawlLastRun}:{" "}
                  {new Date(source.lastRunAt).toLocaleString()}
                </p>
              )}
            </div>
          ))}
          {!sources.length && (
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
