// Admin 数据抓取管理 Hook
import { useState, useEffect, useCallback } from "react";
import { crawlerService } from "../services/crawler.service";
import type { CrawlSource, CrawlTask } from "@/common/types";

interface UseCrawlersOptions {
  autoFetch?: boolean;
}

export function useCrawlers(options: UseCrawlersOptions = {}) {
  const { autoFetch = true } = options;
  const [sources, setSources] = useState<CrawlSource[]>([]);
  const [tasks, setTasks] = useState<CrawlTask[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchSources = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await crawlerService.getSources();
      setSources(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch sources");
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchTasks = useCallback(async (sourceId?: string) => {
    setLoading(true);
    setError(null);
    try {
      const data = await crawlerService.getTasks(sourceId);
      setTasks(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch tasks");
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const createSource = useCallback(async (data: Partial<CrawlSource>) => {
    const newSource = await crawlerService.createSource(data);
    setSources((prev) => [...prev, newSource]);
    return newSource;
  }, []);

  const updateSource = useCallback(
    async (id: string, data: Partial<CrawlSource>) => {
      const updated = await crawlerService.updateSource(id, data);
      setSources((prev) => prev.map((s) => (s.id === id ? updated : s)));
      return updated;
    },
    []
  );

  const deleteSource = useCallback(async (id: string) => {
    await crawlerService.deleteSource(id);
    setSources((prev) => prev.filter((s) => s.id !== id));
  }, []);

  const runTask = useCallback(async (sourceId: string) => {
    const task = await crawlerService.runTask(sourceId);
    setTasks((prev) => [task, ...prev]);
    return task;
  }, []);

  useEffect(() => {
    if (autoFetch) {
      fetchSources();
    }
  }, [autoFetch, fetchSources]);

  return {
    sources,
    tasks,
    loading,
    error,
    fetchSources,
    fetchTasks,
    createSource,
    updateSource,
    deleteSource,
    runTask,
  };
}
