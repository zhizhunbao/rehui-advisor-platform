// Admin 提示词管理 Hook
import { useState, useEffect, useCallback } from "react";
import type {
  AdminPrompt,
  AdminPromptStats,
  SkillLabel,
  Language,
} from "@/common/types";
import { useInfiniteScroll } from "@/common/hooks";
import { promptService } from "../services/prompt.service";

export function usePrompts(lang: Language, autoFetch = true) {
  const [stats, setStats] = useState<AdminPromptStats | null>(null);
  const [categoryLabels, setCategoryLabels] = useState<SkillLabel[]>([]);
  const [sourceLabels, setSourceLabels] = useState<SkillLabel[]>([]);
  const [isSyncing, setIsSyncing] = useState(false);
  const [selectedPrompt, setSelectedPrompt] = useState<AdminPrompt | null>(
    null
  );
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("__all__");
  const [source, setSource] = useState("__all__");

  const fetchStats = useCallback(async () => {
    const data = await promptService.getStats();
    setStats(data);
    return data;
  }, []);

  const fetchLabels = useCallback(async () => {
    const data = await promptService.getLabels();
    setCategoryLabels(data.categories || []);
    setSourceLabels(data.sources || []);
    return data;
  }, []);

  const getCategoryLabel = useCallback(
    (code: string) => {
      if (!code) return "";
      const label = categoryLabels.find((l) => l.code === code);
      return label ? (lang === "zh" ? label.labelZh : label.labelEn) : code;
    },
    [categoryLabels, lang]
  );

  const getSourceLabel = useCallback(
    (code: string) => {
      if (!code) return "";
      const label = sourceLabels.find((l) => l.code === code);
      return label ? (lang === "zh" ? label.labelZh : label.labelEn) : code;
    },
    [sourceLabels, lang]
  );

  const fetchPrompts = useCallback(
    async (page: number) => {
      const params = {
        page,
        limit: 20,
        search: search || undefined,
        category: category !== "__all__" ? category : undefined,
        source: source !== "__all__" ? source : undefined,
      };
      const res = await promptService.getList(params);
      return { data: res.data || [], total: res.meta?.total || 0 };
    },
    [search, category, source]
  );

  const {
    data: prompts,
    isLoading,
    hasMore,
    total,
    loadMoreRef,
    refresh,
  } = useInfiniteScroll<AdminPrompt>({ fetchFn: fetchPrompts });

  const handleToggle = useCallback(
    async (id: string) => {
      await promptService.toggle(id);
      fetchStats();
      refresh();
    },
    [fetchStats, refresh]
  );

  const handleSync = useCallback(async () => {
    setIsSyncing(true);
    try {
      const result = await promptService.sync();
      fetchStats();
      refresh();
      return result;
    } finally {
      setIsSyncing(false);
    }
  }, [fetchStats, refresh]);

  const handleReset = useCallback(() => {
    setSearch("");
    setCategory("__all__");
    setSource("__all__");
  }, []);

  useEffect(() => {
    if (autoFetch) {
      fetchStats();
      fetchLabels();
    }
  }, [autoFetch, fetchStats, fetchLabels]);

  return {
    prompts,
    stats,
    categoryLabels,
    sourceLabels,
    isLoading,
    hasMore,
    total,
    loadMoreRef,
    isSyncing,
    selectedPrompt,
    setSelectedPrompt,
    search,
    setSearch,
    category,
    setCategory,
    source,
    setSource,
    fetchStats,
    fetchLabels,
    getCategoryLabel,
    getSourceLabel,
    handleToggle,
    handleSync,
    handleReset,
    refresh,
  };
}
