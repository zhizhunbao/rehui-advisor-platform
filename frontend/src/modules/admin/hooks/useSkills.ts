// Admin 技能管理 Hook
import { useState, useEffect, useCallback } from "react";
import type {
  Skill,
  SkillStats,
  SkillLabel,
  SkillListParams,
  Language,
} from "@/common/types";
import { useInfiniteScroll } from "@/common/hooks";
import { skillService } from "../services/skill.service";

export function useSkills(lang: Language, autoFetch = true) {
  const [stats, setStats] = useState<SkillStats | null>(null);
  const [categoryLabels, setCategoryLabels] = useState<SkillLabel[]>([]);
  const [sourceLabels, setSourceLabels] = useState<SkillLabel[]>([]);
  const [isSyncing, setIsSyncing] = useState(false);
  const [selectedSkill, setSelectedSkill] = useState<Skill | null>(null);
  const [search, setSearch] = useState("");
  const [filterCategory, setFilterCategory] = useState("__all__");
  const [filterSource, setFilterSource] = useState("__all__");

  const fetchStats = useCallback(async () => {
    const data = await skillService.getStats();
    setStats(data);
    return data;
  }, []);

  const fetchLabels = useCallback(async () => {
    const data = await skillService.getLabels();
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

  const fetchSkills = useCallback(
    async (page: number) => {
      const params: SkillListParams = {
        page,
        limit: 20,
        search: search || undefined,
        category: filterCategory !== "__all__" ? filterCategory : undefined,
        source: filterSource !== "__all__" ? filterSource : undefined,
      };
      const res = await skillService.getList(params);
      return { data: res.data || [], total: res.meta?.total || 0 };
    },
    [search, filterCategory, filterSource]
  );

  const {
    data: skills,
    isLoading,
    hasMore,
    total,
    loadMoreRef,
    refresh,
  } = useInfiniteScroll<Skill>({ fetchFn: fetchSkills });

  const handleToggle = useCallback(
    async (id: string) => {
      await skillService.toggle(id);
      fetchStats();
      refresh();
    },
    [fetchStats, refresh]
  );

  const sync = useCallback(async () => {
    return skillService.sync();
  }, []);

  const handleSync = useCallback(async () => {
    setIsSyncing(true);
    try {
      const result = await sync();
      fetchStats();
      refresh();
      return result;
    } finally {
      setIsSyncing(false);
    }
  }, [sync, fetchStats, refresh]);

  const handleReset = useCallback(() => {
    setSearch("");
    setFilterCategory("__all__");
    setFilterSource("__all__");
  }, []);

  useEffect(() => {
    if (autoFetch) {
      fetchStats();
      fetchLabels();
    }
  }, [autoFetch, fetchStats, fetchLabels]);

  return {
    skills,
    stats,
    categoryLabels,
    sourceLabels,
    isLoading,
    hasMore,
    total,
    loadMoreRef,
    isSyncing,
    selectedSkill,
    setSelectedSkill,
    search,
    setSearch,
    filterCategory,
    setFilterCategory,
    filterSource,
    setFilterSource,
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
