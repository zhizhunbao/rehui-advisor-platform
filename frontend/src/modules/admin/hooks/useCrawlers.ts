// Admin 爬虫管理 Hook
import { useState, useEffect, useCallback } from "react";
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import type { CrawlSource, CrawlTask } from "@/common/types";
import { crawlerService } from "../services/crawler.service";

export function useCrawlers(autoFetch = true) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  const [sources, setSources] = useState<CrawlSource[]>([]);
  const [tasks, setTasks] = useState<CrawlTask[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedSourceId, setSelectedSourceId] = useState<string | null>(null);

  const fetchData = useCallback(async () => {
    setIsLoading(true);
    try {
      const [sourcesData, tasksData] = await Promise.all([
        crawlerService.getSources(),
        crawlerService.getTasks(),
      ]);
      setSources(sourcesData);
      setTasks(tasksData);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const handleRunTask = useCallback(async (sourceId: string) => {
    const task = await crawlerService.runTask(sourceId);
    setTasks((prev) => [task, ...prev]);
  }, []);

  const handleDeleteSource = useCallback(
    async (id: string) => {
      if (!confirm(t.confirmDelete)) return;
      await crawlerService.deleteSource(id);
      setSources((prev) => prev.filter((s) => s.id !== id));
    },
    [t.confirmDelete]
  );

  const filteredTasks = selectedSourceId
    ? tasks.filter((t) => t.sourceId === selectedSourceId)
    : tasks;

  useEffect(() => {
    if (autoFetch) {
      fetchData();
    }
  }, [autoFetch, fetchData]);

  return {
    sources,
    tasks,
    filteredTasks,
    isLoading,
    selectedSourceId,
    setSelectedSourceId,
    handleRunTask,
    handleDeleteSource,
    refresh: fetchData,
  };
}
