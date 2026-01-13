import { useState, useEffect } from "react";
import { adminLocales, type Language } from "@/common/i18n";
import { crawlerService } from "@/modules/admin/services/crawler.service";
import type { CrawlSource, CrawlTask } from "@/common/types";
import { Button } from "@/libs/shadcn/ui/button";
import { Badge } from "@/libs/shadcn/ui/badge";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/libs/shadcn/ui/card";

interface CrawlersViewProps {
  lang: Language;
}

export default function CrawlersView({ lang }: CrawlersViewProps) {
  const t = adminLocales[lang];
  const [sources, setSources] = useState<CrawlSource[]>([]);
  const [tasks, setTasks] = useState<CrawlTask[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedSourceId, setSelectedSourceId] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [sourcesData, tasksData] = await Promise.all([
          crawlerService.getSources(),
          crawlerService.getTasks(),
        ]);
        setSources(sourcesData);
        setTasks(tasksData);
      } catch {
        // Handle error
      } finally {
        setIsLoading(false);
      }
    };
    fetchData();
  }, []);

  const handleRunTask = async (sourceId: string) => {
    try {
      const task = await crawlerService.runTask(sourceId);
      setTasks((prev) => [task, ...prev]);
    } catch {
      // Handle error
    }
  };

  const handleDeleteSource = async (id: string) => {
    if (!confirm(t.confirmDelete)) return;
    try {
      await crawlerService.deleteSource(id);
      setSources((prev) => prev.filter((s) => s.id !== id));
    } catch {
      // Handle error
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-full text-muted-foreground">
        {t.loading}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-foreground">{t.crawlers}</h1>
        <Button>{t.addSource}</Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
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
                  onClick={() => setSelectedSourceId(source.id)}
                >
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="font-medium text-foreground">
                        {source.name}
                      </h3>
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
                          handleRunTask(source.id);
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
                          handleDeleteSource(source.id);
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

        <Card>
          <CardHeader>
            <CardTitle>{t.taskHistory}</CardTitle>
          </CardHeader>
          <CardContent className="p-0">
            <div className="divide-y divide-border max-h-96 overflow-y-auto">
              {tasks
                .filter(
                  (t) => !selectedSourceId || t.sourceId === selectedSourceId
                )
                .map((task) => (
                  <div key={task.id} className="p-4">
                    <div className="flex justify-between items-center">
                      <StatusBadge status={task.status} />
                      <span className="text-sm text-muted-foreground">
                        {task.recordsCount} records
                      </span>
                    </div>
                    <p className="text-xs text-muted-foreground mt-1">
                      {task.startedAt &&
                        new Date(task.startedAt).toLocaleString()}
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
      </div>
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  const variant: Record<
    string,
    "default" | "secondary" | "destructive" | "outline"
  > = {
    success: "default",
    failed: "destructive",
    running: "secondary",
    pending: "outline",
  };

  return <Badge variant={variant[status] ?? "outline"}>{status}</Badge>;
}
