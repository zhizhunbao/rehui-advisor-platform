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
} from "@/common/types";
import { useInfiniteScroll } from "@/common/hooks";
import { dataSourceService } from "../services/dataSource.service";

export function useDataSources() {
  const [stats, setStats] = useState<DataSourceStats | null>(null);
  const [categories, setCategories] = useState<DataSourceCategory[]>([]);
  const [domains, setDomains] = useState<DataSourceDomain[]>([]);
  const [types, setTypes] = useState<DataSourceTypeItem[]>([]);
  const [statuses, setStatuses] = useState<DataSourceStatusItem[]>([]);
  const [languages, setLanguages] = useState<DataSourceLanguageItem[]>([]);

  const [search, setSearch] = useState("");
  const [categoryId, setCategoryId] = useState("__all__");
  const [domainId, setDomainId] = useState("__all__");
  const [status, setStatus] = useState("__all__");
  const [type, setType] = useState("__all__");
  const [language, setLanguage] = useState("__all__");

  const [selectedSource, setSelectedSource] = useState<DataSource | null>(null);
  const [showAddModal, setShowAddModal] = useState(false);

  const fetchSources = useCallback(
    async (page: number) => {
      const params: Record<string, string> = {
        page: String(page),
        limit: "20",
      };
      if (search) params.search = search;
      if (categoryId !== "__all__") params.categoryId = categoryId;
      if (domainId !== "__all__") params.domainId = domainId;
      if (status !== "__all__") params.status = status;
      if (type !== "__all__") params.type = type;
      if (language !== "__all__") params.language = language;

      const res = await dataSourceService.getList(params);
      return { data: res.data || [], total: res.meta?.total || 0 };
    },
    [search, categoryId, domainId, status, type, language]
  );

  const {
    data: sources,
    isLoading,
    hasMore,
    total,
    loadMoreRef,
    refresh,
  } = useInfiniteScroll<DataSource>({ fetchFn: fetchSources });

  const fetchStats = useCallback(async () => {
    const data = await dataSourceService.getStats();
    setStats(data);
  }, []);

  const fetchCategories = useCallback(async () => {
    const data = await dataSourceService.getCategories();
    setCategories(data);
  }, []);

  const fetchDomainsByCategory = useCallback(async (catId: string) => {
    setDomainId("__all__");
    if (catId === "__all__") {
      setDomains([]);
      return;
    }
    const data = await dataSourceService.getDomains(catId);
    setDomains(data);
  }, []);

  const fetchTypes = useCallback(async () => {
    const data = await dataSourceService.getTypes();
    setTypes(data);
  }, []);

  const fetchStatuses = useCallback(async () => {
    const data = await dataSourceService.getStatuses();
    setStatuses(data);
  }, []);

  const fetchLanguages = useCallback(async () => {
    const data = await dataSourceService.getLanguages();
    setLanguages(data);
  }, []);

  const handleRefresh = useCallback(
    async (id: string) => {
      await dataSourceService.refresh(id);
      refresh();
      fetchStats();
    },
    [refresh, fetchStats]
  );

  const handleDelete = useCallback(
    async (id: string) => {
      await dataSourceService.delete(id);
      refresh();
      fetchStats();
    },
    [refresh, fetchStats]
  );

  const handleRefreshAll = useCallback(async () => {
    const result = await dataSourceService.refreshAll();
    refresh();
    fetchStats();
    fetchCategories();
    return result;
  }, [refresh, fetchStats, fetchCategories]);

  const handleReset = useCallback(() => {
    setSearch("");
    setCategoryId("__all__");
    setDomainId("__all__");
    setStatus("__all__");
    setType("__all__");
    setLanguage("__all__");
  }, []);

  useEffect(() => {
    fetchStats();
    fetchCategories();
    fetchTypes();
    fetchStatuses();
    fetchLanguages();
  }, [fetchStats, fetchCategories, fetchTypes, fetchStatuses, fetchLanguages]);

  return {
    sources,
    stats,
    categories,
    domains,
    types,
    statuses,
    languages,
    isLoading,
    hasMore,
    total,
    loadMoreRef,
    search,
    setSearch,
    categoryId,
    setCategoryId,
    domainId,
    setDomainId,
    status,
    setStatus,
    type,
    setType,
    language,
    setLanguage,
    refresh,
    handleRefresh,
    handleDelete,
    handleRefreshAll,
    handleReset,
    fetchDomainsByCategory,
    selectedSource,
    setSelectedSource,
    showAddModal,
    setShowAddModal,
  };
}
