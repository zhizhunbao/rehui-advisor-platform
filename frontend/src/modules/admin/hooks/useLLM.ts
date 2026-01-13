// Admin LLM 模型管理 Hook
import { useState, useEffect, useCallback, useMemo } from "react";
import type {
  LLMModel,
  LLMSyncSource,
  LLMSyncResult,
  LLMModelCreate,
  LLMModelForm,
  Language,
} from "@/common/types";
import {
  LLMProviderLabel,
  LLMProviderPriority,
  LLMCategoryLabel,
  LLMDeploymentTypeLabel,
} from "@/common/enum";
import { llmService } from "../services/llm.service";

export function useLLM(lang: Language, autoFetch = true) {
  const [models, setModels] = useState<LLMModel[]>([]);
  const [syncSources, setSyncSources] = useState<LLMSyncSource[]>([]);
  const [loading, setLoading] = useState(false);
  const [syncing, setSyncing] = useState(false);
  const [syncResult, setSyncResult] = useState<LLMSyncResult | null>(null);

  const [searchQuery, setSearchQuery] = useState("");
  const [filterProvider, setFilterProvider] = useState("");
  const [filterCategory, setFilterCategory] = useState("");
  const [filterDeployment, setFilterDeployment] = useState("");
  const [filterInputPrice, setFilterInputPrice] = useState("");
  const [filterOutputPrice, setFilterOutputPrice] = useState("");
  const [filterContext, setFilterContext] = useState("");
  const [collapsedGroups, setCollapsedGroups] = useState<Set<string>>(
    new Set()
  );

  const fetchModels = useCallback(async () => {
    setLoading(true);
    try {
      const data = await llmService.getList();
      setModels(data);
      return data;
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchSyncSources = useCallback(async () => {
    const data = await llmService.getSyncSources();
    setSyncSources(data);
    return data;
  }, []);

  const create = useCallback(async (data: LLMModelCreate) => {
    const model = await llmService.create(data);
    setModels((prev) => [...prev, model]);
    return model;
  }, []);

  const update = useCallback(async (id: string, data: LLMModelCreate) => {
    const model = await llmService.update(id, data);
    setModels((prev) => prev.map((m) => (m.id === id ? model : m)));
    return model;
  }, []);

  const remove = useCallback(async (id: string) => {
    await llmService.delete(id);
    setModels((prev) => prev.filter((m) => m.id !== id));
  }, []);

  const sync = useCallback(
    async (sourceId?: string) => {
      setSyncing(true);
      setSyncResult(null);
      try {
        const result = await llmService.sync(sourceId);
        setSyncResult(result);
        await fetchModels();
        return result;
      } finally {
        setSyncing(false);
      }
    },
    [fetchModels]
  );

  const normalizeProvider = useCallback((provider: string): string => {
    let p = provider || "unknown";
    if (p.includes("/")) {
      const parts = p.split("/");
      p = parts[0] === "openrouter" && parts.length > 1 ? parts[1] : parts[0];
    }
    p = p.toLowerCase();
    if (p === "meta" || p === "llama") p = "meta-llama";
    if (p === "mistral") p = "mistralai";
    if (p === "alibaba" || p === "aliyun") p = "qwen";
    return p;
  }, []);

  const getProviderLabel = useCallback((key: string): string => {
    return LLMProviderLabel[key] || key;
  }, []);

  const getCategoryLabel = useCallback(
    (key: string): string => {
      return LLMCategoryLabel[key]?.[lang] || key;
    },
    [lang]
  );

  const getDeploymentLabel = useCallback(
    (key: string): string => {
      return LLMDeploymentTypeLabel[key]?.[lang] || key;
    },
    [lang]
  );

  const filteredModels = useMemo(() => {
    return models
      .filter((m) => {
        if (searchQuery) {
          const query = searchQuery.toLowerCase();
          const matchesSearch =
            m.name.toLowerCase().includes(query) ||
            m.displayName.toLowerCase().includes(query) ||
            m.provider.toLowerCase().includes(query);
          if (!matchesSearch) return false;
        }
        if (filterProvider && normalizeProvider(m.provider) !== filterProvider)
          return false;
        if (filterCategory && m.category !== filterCategory) return false;
        if (filterDeployment && m.deploymentType !== filterDeployment)
          return false;

        if (filterInputPrice) {
          const isFree = m.isFree || m.inputPrice === 0;
          if (filterInputPrice === "free" && !isFree) return false;
          if (filterInputPrice === "low" && (isFree || m.inputPrice >= 1))
            return false;
          if (
            filterInputPrice === "medium" &&
            (m.inputPrice < 1 || m.inputPrice >= 10)
          )
            return false;
          if (filterInputPrice === "high" && m.inputPrice < 10) return false;
        }

        if (filterOutputPrice) {
          const isFree = m.isFree || m.outputPrice === 0;
          if (filterOutputPrice === "free" && !isFree) return false;
          if (filterOutputPrice === "low" && (isFree || m.outputPrice >= 1))
            return false;
          if (
            filterOutputPrice === "medium" &&
            (m.outputPrice < 1 || m.outputPrice >= 10)
          )
            return false;
          if (filterOutputPrice === "high" && m.outputPrice < 10) return false;
        }

        if (filterContext) {
          const ctx = m.contextWindow || 0;
          if (filterContext === "small" && ctx > 8192) return false;
          if (filterContext === "medium" && (ctx <= 8192 || ctx > 32768))
            return false;
          if (filterContext === "large" && (ctx <= 32768 || ctx > 131072))
            return false;
          if (filterContext === "xlarge" && ctx <= 131072) return false;
        }
        return true;
      })
      .sort((a, b) => {
        const hasDateA = !!a.releaseDate;
        const hasDateB = !!b.releaseDate;
        if (hasDateA && !hasDateB) return -1;
        if (!hasDateA && hasDateB) return 1;
        if (hasDateA && hasDateB) {
          return (
            new Date(b.releaseDate).getTime() -
            new Date(a.releaseDate).getTime()
          );
        }
        return (
          new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
        );
      });
  }, [
    models,
    searchQuery,
    filterProvider,
    filterCategory,
    filterDeployment,
    filterInputPrice,
    filterOutputPrice,
    filterContext,
    normalizeProvider,
  ]);

  const groupedModels = useMemo(() => {
    return filteredModels.reduce((acc, model) => {
      const key = normalizeProvider(model.provider);
      if (!acc[key]) acc[key] = [];
      acc[key].push(model);
      return acc;
    }, {} as Record<string, LLMModel[]>);
  }, [filteredModels, normalizeProvider]);

  const sortedGroups = useMemo(() => {
    return Object.keys(groupedModels).sort((a, b) => {
      const priorityA = LLMProviderPriority[a] ?? 100;
      const priorityB = LLMProviderPriority[b] ?? 100;
      if (priorityA !== priorityB) return priorityA - priorityB;
      return groupedModels[b].length - groupedModels[a].length;
    });
  }, [groupedModels]);

  const toggleGroup = useCallback((group: string) => {
    setCollapsedGroups((prev) => {
      const next = new Set(prev);
      if (next.has(group)) {
        next.delete(group);
      } else {
        next.add(group);
      }
      return next;
    });
  }, []);

  const stats = useMemo(
    () => ({
      total: models.length,
      active: models.filter((m) => m.isActive).length,
      api: models.filter((m) => m.deploymentType === "api").length,
      local: models.filter((m) => m.deploymentType === "local").length,
      free: models.filter((m) => m.isFree).length,
    }),
    [models]
  );

  const filterCounts = useMemo(() => {
    const providerCounts = Object.entries(LLMProviderLabel)
      .map(([value, label]) => ({
        value,
        label,
        count: models.filter((m) => normalizeProvider(m.provider) === value)
          .length,
      }))
      .filter((p) => p.count > 0)
      .sort(
        (a, b) =>
          (LLMProviderPriority[a.value] ?? 100) -
          (LLMProviderPriority[b.value] ?? 100)
      );

    const categoryCounts = Object.entries(LLMCategoryLabel)
      .map(([value, labels]) => ({
        value,
        label: labels[lang],
        count: models.filter((m) => m.category === value).length,
      }))
      .filter((c) => c.count > 0);

    const deploymentCounts = Object.entries(LLMDeploymentTypeLabel)
      .map(([value, labels]) => ({
        value,
        label: labels[lang],
        count: models.filter((m) => m.deploymentType === value).length,
      }))
      .filter((d) => d.count > 0);

    const inputPriceCounts = (() => {
      const ranges = { free: 0, low: 0, medium: 0, high: 0 };
      models.forEach((m) => {
        if (m.isFree || m.inputPrice === 0) ranges.free++;
        else if (m.inputPrice < 1) ranges.low++;
        else if (m.inputPrice < 10) ranges.medium++;
        else ranges.high++;
      });
      return [
        { value: "free", label: "Free", count: ranges.free },
        { value: "low", label: "<$1", count: ranges.low },
        { value: "medium", label: "$1-10", count: ranges.medium },
        { value: "high", label: ">$10", count: ranges.high },
      ].filter((r) => r.count > 0);
    })();

    const outputPriceCounts = (() => {
      const ranges = { free: 0, low: 0, medium: 0, high: 0 };
      models.forEach((m) => {
        if (m.isFree || m.outputPrice === 0) ranges.free++;
        else if (m.outputPrice < 1) ranges.low++;
        else if (m.outputPrice < 10) ranges.medium++;
        else ranges.high++;
      });
      return [
        { value: "free", label: "Free", count: ranges.free },
        { value: "low", label: "<$1", count: ranges.low },
        { value: "medium", label: "$1-10", count: ranges.medium },
        { value: "high", label: ">$10", count: ranges.high },
      ].filter((r) => r.count > 0);
    })();

    const contextCounts = (() => {
      const ranges = { small: 0, medium: 0, large: 0, xlarge: 0 };
      models.forEach((m) => {
        const ctx = m.contextWindow || 0;
        if (ctx <= 8192) ranges.small++;
        else if (ctx <= 32768) ranges.medium++;
        else if (ctx <= 131072) ranges.large++;
        else ranges.xlarge++;
      });
      return [
        { value: "small", label: "≤8K", count: ranges.small },
        { value: "medium", label: "8K-32K", count: ranges.medium },
        { value: "large", label: "32K-128K", count: ranges.large },
        { value: "xlarge", label: ">128K", count: ranges.xlarge },
      ].filter((r) => r.count > 0);
    })();

    return {
      providerCounts,
      categoryCounts,
      deploymentCounts,
      inputPriceCounts,
      outputPriceCounts,
      contextCounts,
    };
  }, [models, lang, normalizeProvider]);

  const handleReset = useCallback(() => {
    setSearchQuery("");
    setFilterProvider("");
    setFilterCategory("");
    setFilterDeployment("");
    setFilterInputPrice("");
    setFilterOutputPrice("");
    setFilterContext("");
  }, []);

  const getModelForm = useCallback((model: LLMModel | null): LLMModelForm => {
    if (model) {
      return {
        name: model.name,
        displayName: model.displayName,
        provider: model.provider,
        apiEndpoint: model.apiEndpoint,
        version: model.version || "",
        category: model.category || "general",
        deploymentType: model.deploymentType || "api",
        inputPrice: model.inputPrice || 0,
        outputPrice: model.outputPrice || 0,
        isFree: model.isFree || false,
        contextWindow: model.contextWindow || 128000,
        maxOutputTokens: model.maxOutputTokens || 4096,
        capabilities: model.capabilities || [],
        description: model.description || "",
        dockerImage: model.dockerImage || "",
        hardwareRequirements: model.hardwareRequirements || {},
        rateLimit: model.rateLimit || {},
        latencyMs: model.latencyMs || 0,
        qualityScore: model.qualityScore || 8.0,
        license: model.license || "",
        releaseDate: model.releaseDate || "",
        isDeprecated: model.isDeprecated || false,
        fallbackModelId: model.fallbackModelId || "",
        isActive: model.isActive,
        isDefault: model.isDefault,
        config: model.config || {},
        sortOrder: model.sortOrder || 0,
      };
    }
    return {
      name: "",
      displayName: "",
      provider: "openai",
      apiEndpoint: "https://api.openai.com/v1",
      version: "",
      category: "general",
      deploymentType: "api",
      inputPrice: 0,
      outputPrice: 0,
      isFree: false,
      contextWindow: 128000,
      maxOutputTokens: 4096,
      capabilities: [],
      description: "",
      dockerImage: "",
      hardwareRequirements: {},
      rateLimit: {},
      latencyMs: 0,
      qualityScore: 8.0,
      license: "",
      releaseDate: "",
      isDeprecated: false,
      fallbackModelId: "",
      isActive: true,
      isDefault: false,
      config: {},
      sortOrder: 0,
    };
  }, []);

  const hasFilters = useMemo(
    () =>
      searchQuery ||
      filterProvider ||
      filterCategory ||
      filterDeployment ||
      filterInputPrice ||
      filterOutputPrice ||
      filterContext,
    [
      searchQuery,
      filterProvider,
      filterCategory,
      filterDeployment,
      filterInputPrice,
      filterOutputPrice,
      filterContext,
    ]
  );

  useEffect(() => {
    if (autoFetch) {
      fetchModels();
      fetchSyncSources();
    }
  }, [autoFetch, fetchModels, fetchSyncSources]);

  return {
    models,
    filteredModels,
    groupedModels,
    sortedGroups,
    syncSources,
    loading,
    syncing,
    syncResult,
    stats,
    filterCounts,
    searchQuery,
    setSearchQuery,
    filterProvider,
    setFilterProvider,
    filterCategory,
    setFilterCategory,
    filterDeployment,
    setFilterDeployment,
    filterInputPrice,
    setFilterInputPrice,
    filterOutputPrice,
    setFilterOutputPrice,
    filterContext,
    setFilterContext,
    collapsedGroups,
    toggleGroup,
    hasFilters,
    handleReset,
    normalizeProvider,
    getProviderLabel,
    getCategoryLabel,
    getDeploymentLabel,
    getModelForm,
    fetchModels,
    fetchSyncSources,
    create,
    update,
    remove,
    sync,
  };
}
