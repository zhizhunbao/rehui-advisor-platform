// Admin 数据源管理 Hook
import { useState, useEffect, useCallback } from "react";
import type {
  DataSource,
  DataSourceStats,
  DataSourceCategory,
  DataSourceDomain,
  DataSourceTypeItem,
  DataSourceStatusItem,
  DataSourceLanguageItem,
  DataSourceListParams,
  DataSourceCreate,
} from "@/common/types";
import { dataSourceService } from "../services/dataSource.service";

interface UseDataSourcesOptions {
  autoFetch?: boolean;
}

export function useDataSources(options: UseDataSourcesOptions = {}) {
  const { autoFetch = true } = options;
  const [sources, setSources] = useState<DataSource[]>([]);
  const [stats, setStats] = useState<DataSourceStats | null>(null);
  const [categories, setCategories] = useState<DataSourceCategory[]>([]);
  const [domains, setDomains] = useState<DataSourceDomain[]>([]);
  const [types, setTypes] = useState<DataSourceTypeItem[]>([]);
  const [statuses, setStatuses] = useState<DataSourceStatusItem[]>([]);
  const [languages, setLanguages] = useState<DataSourceLanguageItem[]>([]);
  const [loading, setLoading] = useState(false);
  const [total, setTotal] = useState(0);

  const fetchSources = useCallback(
    async (params: DataSourceListParams = {}) => {
      setLoading(true);
      try {
        const res = await dataSourceService.getList(params);
        setSources(res.data || []);
        setTotal(res.meta?.total || 0);
        return res;
      } finally {
        setLoading(false);
      }
    },
    []
  );

  const fetchStats = useCallback(async () => {
    const data = await dataSourceService.getStats();
    setStats(data);
    return data;
  }, []);

  const fetchCategories = useCallback(async () => {
    const data = await dataSourceService.getCategories();
    setCategories(data);
    return data;
  }, []);

  const fetchDomains = useCallback(async (categoryId?: string) => {
    const data = await dataSourceService.getDomains(categoryId);
    setDomains(data);
    return data;
  }, []);

  const fetchTypes = useCallback(async () => {
    const data = await dataSourceService.getTypes();
    setTypes(data);
    return data;
  }, []);

  const fetchStatuses = useCallback(async () => {
    const data = await dataSourceService.getStatuses();
    setStatuses(data);
    return data;
  }, []);

  const fetchLanguages = useCallback(async () => {
    const data = await dataSourceService.getLanguages();
    setLanguages(data);
    return data;
  }, []);

  const create = useCallback(async (data: DataSourceCreate) => {
    const source = await dataSourceService.create(data);
    setSources((prev) => [...prev, source]);
    return source;
  }, []);

  const remove = useCallback(async (id: string) => {
    await dataSourceService.delete(id);
    setSources((prev) => prev.filter((s) => s.id !== id));
  }, []);

  const refresh = useCallback(async (id: string) => {
    return dataSourceService.refresh(id);
  }, []);

  const refreshAll = useCallback(async () => {
    return dataSourceService.refreshAll();
  }, []);

  useEffect(() => {
    if (autoFetch) {
      fetchSources();
      fetchStats();
      fetchCategories();
      fetchTypes();
      fetchStatuses();
      fetchLanguages();
    }
  }, [
    autoFetch,
    fetchSources,
    fetchStats,
    fetchCategories,
    fetchTypes,
    fetchStatuses,
    fetchLanguages,
  ]);

  return {
    sources,
    stats,
    categories,
    domains,
    types,
    statuses,
    languages,
    loading,
    total,
    fetchSources,
    fetchStats,
    fetchCategories,
    fetchDomains,
    fetchTypes,
    fetchStatuses,
    fetchLanguages,
    create,
    remove,
    refresh,
    refreshAll,
  };
}
