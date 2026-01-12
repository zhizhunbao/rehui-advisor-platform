import { useState, useEffect, useCallback } from "react";
import { adminLocales, type Language } from "@/locales";
import { StatCard } from "@/modules/admin/components/StatCard";
import { TagFilter } from "@/modules/admin/components/TagFilter";
import { getApiBase, getAuthHeaders } from "@/modules/admin/utils/api";
import { Button } from "@/libs/shadcn/ui/button";
import { Input } from "@/libs/shadcn/ui/input";
import { Badge } from "@/libs/shadcn/ui/badge";

import { Switch } from "@/libs/shadcn/ui/switch";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/libs/shadcn/ui/tabs";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/libs/shadcn/ui/select";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/libs/shadcn/ui/dialog";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/libs/shadcn/ui/alert-dialog";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/libs/shadcn/ui/table";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/libs/shadcn/ui/collapsible";
import { ChevronDown, ChevronRight } from "lucide-react";

const API_BASE = getApiBase();
const getHeaders = getAuthHeaders;

// ========== Types ==========
interface LLMModel {
  id: string;
  name: string;
  display_name: string;
  provider: string;
  api_endpoint: string;
  version: string;
  category: string;
  deployment_type: string;
  input_price: number;
  output_price: number;
  is_free: boolean;
  context_window: number;
  max_output_tokens: number;
  capabilities: string[];
  description: string;
  docker_image: string;
  hardware_requirements: Record<string, string>;
  rate_limit: Record<string, number>;
  latency_ms: number;
  quality_score: number;
  license: string;
  release_date: string;
  is_deprecated: boolean;
  fallback_model_id: string;
  is_active: boolean;
  is_default: boolean;
  config: Record<string, string>;
  sort_order: number;
  created_at: string;
}

interface SyncSource {
  id: string;
  name: string;
  url: string;
  status: string;
}

interface LLMViewProps {
  lang: Language;
}

const PROVIDERS = [
  { value: "openai", label: "OpenAI", priority: 1 },
  { value: "anthropic", label: "Anthropic", priority: 2 },
  { value: "google", label: "Google", priority: 3 },
  { value: "meta-llama", label: "Meta Llama", priority: 4 },
  { value: "mistralai", label: "Mistral AI", priority: 5 },
  { value: "deepseek", label: "DeepSeek", priority: 6 },
  { value: "qwen", label: "Qwen (阿里)", priority: 7 },
  { value: "microsoft", label: "Microsoft", priority: 8 },
  { value: "cohere", label: "Cohere", priority: 9 },
  { value: "groq", label: "Groq", priority: 10 },
  { value: "x-ai", label: "xAI (Grok)", priority: 11 },
  { value: "amazon", label: "Amazon", priority: 12 },
  { value: "nvidia", label: "NVIDIA", priority: 13 },
  { value: "perplexity", label: "Perplexity", priority: 14 },
  { value: "openrouter", label: "OpenRouter", priority: 15 },
  { value: "azure", label: "Azure", priority: 16 },
  { value: "vertex_ai", label: "Vertex AI", priority: 17 },
  { value: "bedrock", label: "AWS Bedrock", priority: 18 },
  { value: "ollama", label: "Ollama", priority: 90 },
  { value: "vllm", label: "vLLM", priority: 91 },
];

// Provider priority map for sorting
const PROVIDER_PRIORITY: Record<string, number> = PROVIDERS.reduce(
  (acc, p) => ({ ...acc, [p.value]: p.priority }),
  {}
);

const CATEGORIES = [
  { value: "general", label: { zh: "通用", en: "General" } },
  { value: "chat", label: { zh: "对话", en: "Chat" } },
  { value: "coding", label: { zh: "编程", en: "Coding" } },
  { value: "reasoning", label: { zh: "推理", en: "Reasoning" } },
  { value: "vision", label: { zh: "视觉", en: "Vision" } },
  { value: "embedding", label: { zh: "嵌入", en: "Embedding" } },
];

const DEPLOYMENT_TYPES = [
  { value: "api", label: { zh: "API 调用", en: "API" } },
  { value: "local", label: { zh: "本地部署", en: "Local" } },
  { value: "hybrid", label: { zh: "混合", en: "Hybrid" } },
];

const CAPABILITIES_OPTIONS = [
  "vision",
  "function_calling",
  "json_mode",
  "streaming",
  "code_interpreter",
  "web_search",
];

const defaultModelForm = {
  name: "",
  display_name: "",
  provider: "openai",
  api_endpoint: "https://api.openai.com/v1",
  version: "",
  category: "general",
  deployment_type: "api",
  input_price: 0,
  output_price: 0,
  is_free: false,
  context_window: 128000,
  max_output_tokens: 4096,
  capabilities: [] as string[],
  description: "",
  docker_image: "",
  hardware_requirements: {} as Record<string, string>,
  rate_limit: {} as Record<string, number>,
  latency_ms: 0,
  quality_score: 8.0,
  license: "",
  release_date: "",
  is_deprecated: false,
  fallback_model_id: "",
  is_active: true,
  is_default: false,
  config: {} as Record<string, string>,
  sort_order: 0,
};

export default function LLMView({ lang }: LLMViewProps) {
  const t = adminLocales[lang];

  // ========== State ==========
  const [models, setModels] = useState<LLMModel[]>([]);
  const [syncSources, setSyncSources] = useState<SyncSource[]>([]);
  const [isSyncing, setIsSyncing] = useState(false);
  const [syncResult, setSyncResult] = useState<{
    synced: number;
    errors: { source: string; error: string }[];
  } | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [showDialog, setShowDialog] = useState(false);
  const [editingModel, setEditingModel] = useState<LLMModel | null>(null);
  const [modelForm, setModelForm] = useState(defaultModelForm);
  const [activeTab, setActiveTab] = useState("basic");

  // Filters
  const [searchQuery, setSearchQuery] = useState("");
  const [filterProvider, setFilterProvider] = useState("");
  const [filterCategory, setFilterCategory] = useState("");
  const [filterDeployment, setFilterDeployment] = useState("");
  const [filterInputPrice, setFilterInputPrice] = useState("");
  const [filterOutputPrice, setFilterOutputPrice] = useState("");
  const [filterContext, setFilterContext] = useState("");

  // Filter options from API - removed, now calculated from models

  // Delete
  const [deleteTarget, setDeleteTarget] = useState<{
    id: string;
    name: string;
  } | null>(null);

  // Collapsed groups
  const [collapsedGroups, setCollapsedGroups] = useState<Set<string>>(
    new Set()
  );

  // ========== Fetch ==========
  const fetchModels = useCallback(async () => {
    setIsLoading(true);
    try {
      const res = await fetch(`${API_BASE}/llm/models?limit=1000`, {
        headers: getHeaders(),
      });
      const json = await res.json();
      if (json.success) {
        setModels(json.data);
      }
    } finally {
      setIsLoading(false);
    }
  }, []);

  const fetchSyncSources = useCallback(async () => {
    try {
      const res = await fetch(`${API_BASE}/llm/sync/sources`, {
        headers: getHeaders(),
      });
      const json = await res.json();
      if (json.success) {
        setSyncSources(json.data);
      }
    } catch {
      // ignore
    }
  }, []);

  useEffect(() => {
    fetchModels();
    fetchSyncSources();
  }, [fetchModels, fetchSyncSources]);

  // ========== Filtered & Grouped Models ==========
  const filteredModels = models
    .filter((m) => {
      // Search filter
      if (searchQuery) {
        const query = searchQuery.toLowerCase();
        const matchesSearch =
          m.name.toLowerCase().includes(query) ||
          m.display_name.toLowerCase().includes(query) ||
          m.provider.toLowerCase().includes(query);
        if (!matchesSearch) return false;
      }
      if (filterProvider && m.provider !== filterProvider) return false;
      if (filterCategory && m.category !== filterCategory) return false;
      if (filterDeployment && m.deployment_type !== filterDeployment)
        return false;

      // Input Price filter
      if (filterInputPrice) {
        const isFree = m.is_free || m.input_price === 0;
        if (filterInputPrice === "free" && !isFree) return false;
        if (filterInputPrice === "low" && (isFree || m.input_price >= 1))
          return false;
        if (
          filterInputPrice === "medium" &&
          (m.input_price < 1 || m.input_price >= 10)
        )
          return false;
        if (filterInputPrice === "high" && m.input_price < 10) return false;
      }

      // Output Price filter
      if (filterOutputPrice) {
        const isFree = m.is_free || m.output_price === 0;
        if (filterOutputPrice === "free" && !isFree) return false;
        if (filterOutputPrice === "low" && (isFree || m.output_price >= 1))
          return false;
        if (
          filterOutputPrice === "medium" &&
          (m.output_price < 1 || m.output_price >= 10)
        )
          return false;
        if (filterOutputPrice === "high" && m.output_price < 10) return false;
      }

      // Context filter
      if (filterContext) {
        const ctx = m.context_window || 0;
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
      // Models with release_date come first (newest first), then models without release_date
      const hasDateA = !!a.release_date;
      const hasDateB = !!b.release_date;

      // If one has date and other doesn't, the one with date comes first
      if (hasDateA && !hasDateB) return -1;
      if (!hasDateA && hasDateB) return 1;

      // Both have dates: sort by release_date (newest first)
      if (hasDateA && hasDateB) {
        return (
          new Date(b.release_date).getTime() -
          new Date(a.release_date).getTime()
        );
      }

      // Neither has date: sort by created_at (newest first)
      return (
        new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
      );
    });

  // Helper to normalize provider name
  const normalizeProvider = (provider: string): string => {
    let p = provider || "unknown";
    if (p.includes("/")) {
      const parts = p.split("/");
      if (parts[0] === "openrouter" && parts.length > 1) {
        p = parts[1];
      } else {
        p = parts[0];
      }
    }
    p = p.toLowerCase();
    if (p === "meta" || p === "llama") p = "meta-llama";
    if (p === "mistral") p = "mistralai";
    if (p === "alibaba" || p === "aliyun") p = "qwen";
    return p;
  };

  // Group models by provider
  const groupedModels = filteredModels.reduce((acc, model) => {
    const key = normalizeProvider(model.provider);
    if (!acc[key]) acc[key] = [];
    acc[key].push(model);
    return acc;
  }, {} as Record<string, LLMModel[]>);

  // Sort groups by provider priority
  const sortedGroups = Object.keys(groupedModels).sort((a, b) => {
    const priorityA = PROVIDER_PRIORITY[a] ?? 100;
    const priorityB = PROVIDER_PRIORITY[b] ?? 100;
    if (priorityA !== priorityB) return priorityA - priorityB;
    return groupedModels[b].length - groupedModels[a].length;
  });

  const toggleGroup = (group: string) => {
    setCollapsedGroups((prev) => {
      const next = new Set(prev);
      if (next.has(group)) {
        next.delete(group);
      } else {
        next.add(group);
      }
      return next;
    });
  };

  // Get provider label
  const getProviderLabel = (key: string): string => {
    return PROVIDERS.find((p) => p.value === key)?.label || key;
  };

  // ========== Handlers ==========
  const handleCreate = () => {
    setEditingModel(null);
    setModelForm(defaultModelForm);
    setActiveTab("basic");
    setShowDialog(true);
  };

  const handleEdit = (model: LLMModel) => {
    setEditingModel(model);
    setModelForm({
      name: model.name,
      display_name: model.display_name,
      provider: model.provider,
      api_endpoint: model.api_endpoint,
      version: model.version || "",
      category: model.category || "general",
      deployment_type: model.deployment_type || "api",
      input_price: model.input_price || 0,
      output_price: model.output_price || 0,
      is_free: model.is_free || false,
      context_window: model.context_window || 128000,
      max_output_tokens: model.max_output_tokens || 4096,
      capabilities: model.capabilities || [],
      description: model.description || "",
      docker_image: model.docker_image || "",
      hardware_requirements: model.hardware_requirements || {},
      rate_limit: model.rate_limit || {},
      latency_ms: model.latency_ms || 0,
      quality_score: model.quality_score || 8.0,
      license: model.license || "",
      release_date: model.release_date || "",
      is_deprecated: model.is_deprecated || false,
      fallback_model_id: model.fallback_model_id || "",
      is_active: model.is_active,
      is_default: model.is_default,
      config: model.config || {},
      sort_order: model.sort_order || 0,
    });
    setActiveTab("basic");
    setShowDialog(true);
  };

  const handleSave = async () => {
    const url = editingModel
      ? `${API_BASE}/llm/models/${editingModel.id}`
      : `${API_BASE}/llm/models`;
    const method = editingModel ? "PUT" : "POST";

    const payload = {
      ...modelForm,
      fallback_model_id: modelForm.fallback_model_id || null,
    };

    const res = await fetch(url, {
      method,
      headers: { ...getHeaders(), "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (res.ok) {
      setShowDialog(false);
      fetchModels();
    }
  };

  const handleDelete = async () => {
    if (!deleteTarget) return;
    await fetch(`${API_BASE}/llm/models/${deleteTarget.id}`, {
      method: "DELETE",
      headers: getHeaders(),
    });
    setDeleteTarget(null);
    fetchModels();
  };

  const toggleCapability = (cap: string) => {
    const caps = modelForm.capabilities.includes(cap)
      ? modelForm.capabilities.filter((c) => c !== cap)
      : [...modelForm.capabilities, cap];
    setModelForm({ ...modelForm, capabilities: caps });
  };

  const handleSync = async (sourceId?: string) => {
    setIsSyncing(true);
    setSyncResult(null);
    try {
      const url = sourceId
        ? `${API_BASE}/llm/sync?source_id=${sourceId}`
        : `${API_BASE}/llm/sync`;
      const res = await fetch(url, {
        method: "POST",
        headers: getHeaders(),
      });
      const json = await res.json();
      if (json.success) {
        setSyncResult(json.data);
        fetchModels();
      }
    } finally {
      setIsSyncing(false);
    }
  };

  // ========== Stats ==========
  const activeModels = models.filter((m) => m.is_active).length;
  const apiModels = models.filter((m) => m.deployment_type === "api").length;
  const localModels = models.filter(
    (m) => m.deployment_type === "local"
  ).length;
  const freeModels = models.filter((m) => m.is_free).length;

  // ========== Filter Counts ==========
  const providerCounts = PROVIDERS.map((p) => ({
    ...p,
    count: models.filter((m) => normalizeProvider(m.provider) === p.value)
      .length,
  })).filter((p) => p.count > 0);

  const categoryCounts = CATEGORIES.map((c) => ({
    value: c.value,
    label: c.label[lang],
    count: models.filter((m) => m.category === c.value).length,
  })).filter((c) => c.count > 0);

  const deploymentCounts = DEPLOYMENT_TYPES.map((d) => ({
    value: d.value,
    label: d.label[lang],
    count: models.filter((m) => m.deployment_type === d.value).length,
  })).filter((d) => d.count > 0);

  // Input Price 筛选（基于前端数据）
  const inputPriceCounts = (() => {
    const ranges = { free: 0, low: 0, medium: 0, high: 0 };
    models.forEach((m) => {
      if (m.is_free || m.input_price === 0) ranges.free++;
      else if (m.input_price < 1) ranges.low++;
      else if (m.input_price < 10) ranges.medium++;
      else ranges.high++;
    });
    return [
      { value: "free", label: "Free", count: ranges.free },
      { value: "low", label: "<$1", count: ranges.low },
      { value: "medium", label: "$1-10", count: ranges.medium },
      { value: "high", label: ">$10", count: ranges.high },
    ].filter((r) => r.count > 0);
  })();

  // Output Price 筛选（基于前端数据）
  const outputPriceCounts = (() => {
    const ranges = { free: 0, low: 0, medium: 0, high: 0 };
    models.forEach((m) => {
      if (m.is_free || m.output_price === 0) ranges.free++;
      else if (m.output_price < 1) ranges.low++;
      else if (m.output_price < 10) ranges.medium++;
      else ranges.high++;
    });
    return [
      { value: "free", label: "Free", count: ranges.free },
      { value: "low", label: "<$1", count: ranges.low },
      { value: "medium", label: "$1-10", count: ranges.medium },
      { value: "high", label: ">$10", count: ranges.high },
    ].filter((r) => r.count > 0);
  })();

  // Context 筛选（基于前端数据）
  const contextCounts = (() => {
    const ranges = { small: 0, medium: 0, large: 0, xlarge: 0 };
    models.forEach((m) => {
      const ctx = m.context_window || 0;
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

  return (
    <div className="space-y-6">
      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        <StatCard
          label={lang === "zh" ? "模型总数" : "Total"}
          value={models.length}
        />
        <StatCard
          label={lang === "zh" ? "活跃" : "Active"}
          value={activeModels}
          color="green"
        />
        <StatCard
          label={lang === "zh" ? "API 调用" : "API"}
          value={apiModels}
          color="violet"
        />
        <StatCard
          label={lang === "zh" ? "本地部署" : "Local"}
          value={localModels}
          color="amber"
        />
        <StatCard
          label={lang === "zh" ? "免费" : "Free"}
          value={freeModels}
          color="rose"
        />
      </div>

      {/* Actions */}
      <div className="flex flex-wrap gap-4 items-center justify-end">
        <Button
          variant="outline"
          onClick={() => handleSync()}
          disabled={isSyncing}
        >
          {isSyncing
            ? lang === "zh"
              ? "同步中..."
              : "Syncing..."
            : lang === "zh"
            ? "🔄 同步模型"
            : "🔄 Sync Models"}
        </Button>
        <Button onClick={handleCreate}>
          {lang === "zh" ? "+ 添加模型" : "+ Add Model"}
        </Button>
      </div>

      {/* Provider 标签 */}
      {providerCounts.length > 0 && (
        <TagFilter
          lang={lang}
          label={lang === "zh" ? "公司" : "Company"}
          options={providerCounts.map((p) => ({
            value: p.value,
            label: p.label,
            count: p.count,
          }))}
          value={filterProvider || "__all__"}
          onChange={(v) => setFilterProvider(v === "__all__" ? "" : v)}
          color="violet"
        />
      )}

      {/* Category 标签 */}
      {categoryCounts.length > 0 && (
        <TagFilter
          lang={lang}
          label={lang === "zh" ? "类别" : "Category"}
          options={categoryCounts.map((c) => ({
            value: c.value,
            label: c.label,
            count: c.count,
          }))}
          value={filterCategory || "__all__"}
          onChange={(v) => setFilterCategory(v === "__all__" ? "" : v)}
          color="blue"
        />
      )}

      {/* Deployment 标签 */}
      {deploymentCounts.length > 0 && (
        <TagFilter
          lang={lang}
          label={lang === "zh" ? "部署类型" : "Deployment"}
          options={deploymentCounts.map((d) => ({
            value: d.value,
            label: d.label,
            count: d.count,
          }))}
          value={filterDeployment || "__all__"}
          onChange={(v) => setFilterDeployment(v === "__all__" ? "" : v)}
          color="emerald"
        />
      )}

      {/* Input Price 标签 */}
      {inputPriceCounts.length > 0 && (
        <TagFilter
          lang={lang}
          label={lang === "zh" ? "输入价格" : "Input Price"}
          options={inputPriceCounts}
          value={filterInputPrice || "__all__"}
          onChange={(v) => setFilterInputPrice(v === "__all__" ? "" : v)}
          color="amber"
        />
      )}

      {/* Output Price 标签 */}
      {outputPriceCounts.length > 0 && (
        <TagFilter
          lang={lang}
          label={lang === "zh" ? "输出价格" : "Output Price"}
          options={outputPriceCounts}
          value={filterOutputPrice || "__all__"}
          onChange={(v) => setFilterOutputPrice(v === "__all__" ? "" : v)}
          color="orange"
        />
      )}

      {/* Context 标签 */}
      {contextCounts.length > 0 && (
        <TagFilter
          lang={lang}
          label="Context"
          options={contextCounts}
          value={filterContext || "__all__"}
          onChange={(v) => setFilterContext(v === "__all__" ? "" : v)}
          color="rose"
        />
      )}

      {/* 搜索和重置 */}
      <div className="flex gap-4 items-center">
        <Input
          placeholder={lang === "zh" ? "搜索模型..." : "Search models..."}
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-[200px]"
        />
        {(searchQuery ||
          filterProvider ||
          filterCategory ||
          filterDeployment ||
          filterInputPrice ||
          filterOutputPrice ||
          filterContext) && (
          <Button
            variant="outline"
            size="sm"
            onClick={() => {
              setSearchQuery("");
              setFilterProvider("");
              setFilterCategory("");
              setFilterDeployment("");
              setFilterInputPrice("");
              setFilterOutputPrice("");
              setFilterContext("");
            }}
          >
            {lang === "zh" ? "重置筛选" : "Reset"}
          </Button>
        )}
      </div>

      {/* Sync Result */}
      {syncResult && (
        <div
          className={`p-4 rounded-lg ${
            syncResult.errors.length > 0
              ? "bg-amber-50 dark:bg-amber-950"
              : "bg-green-50 dark:bg-green-950"
          }`}
        >
          <div className="font-medium">
            {lang === "zh"
              ? `同步完成：${syncResult.synced} 个模型`
              : `Sync completed: ${syncResult.synced} models`}
          </div>
          {syncResult.errors.length > 0 && (
            <div className="text-sm text-muted-foreground mt-1">
              {lang === "zh" ? "错误" : "Errors"}:{" "}
              {syncResult.errors.map((e) => e.error).join(", ")}
            </div>
          )}
        </div>
      )}

      {/* Sync Sources Info */}
      {syncSources.length > 0 && (
        <div className="text-sm text-muted-foreground">
          {lang === "zh" ? "同步源" : "Sync sources"}:{" "}
          {syncSources.map((s) => s.name).join(", ")}
          <span className="ml-2 text-xs">
            (
            {lang === "zh"
              ? "在 GitHub Links 中管理"
              : "Manage in GitHub Links"}
            )
          </span>
        </div>
      )}

      {/* Tables by Group */}
      {isLoading ? (
        <div className="text-center py-8 text-muted-foreground">
          {t.loading}
        </div>
      ) : (
        <div className="space-y-4">
          {sortedGroups.map((groupKey) => {
            const groupModels = groupedModels[groupKey];
            const isCollapsed = collapsedGroups.has(groupKey);
            const groupLabel = getProviderLabel(groupKey);

            return (
              <Collapsible
                key={groupKey}
                open={!isCollapsed}
                onOpenChange={() => toggleGroup(groupKey)}
              >
                <div className="border rounded-lg overflow-hidden">
                  <CollapsibleTrigger className="w-full">
                    <div className="flex items-center justify-between px-4 py-3 bg-muted/50 hover:bg-muted transition-colors">
                      <div className="flex items-center gap-3">
                        {isCollapsed ? (
                          <ChevronRight className="h-4 w-4" />
                        ) : (
                          <ChevronDown className="h-4 w-4" />
                        )}
                        <span className="font-medium">{groupLabel}</span>
                        <Badge variant="secondary">{groupModels.length}</Badge>
                      </div>
                      <div className="flex gap-2 text-xs text-muted-foreground">
                        <span>
                          {lang === "zh" ? "活跃" : "Active"}:{" "}
                          {groupModels.filter((m) => m.is_active).length}
                        </span>
                        <span>
                          {lang === "zh" ? "免费" : "Free"}:{" "}
                          {groupModels.filter((m) => m.is_free).length}
                        </span>
                      </div>
                    </div>
                  </CollapsibleTrigger>
                  <CollapsibleContent>
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead>
                            {lang === "zh" ? "模型" : "Model"}
                          </TableHead>
                          <TableHead>
                            {lang === "zh" ? "公司" : "Company"}
                          </TableHead>
                          <TableHead>
                            {lang === "zh" ? "发布时间" : "Released"}
                          </TableHead>
                          <TableHead>
                            {lang === "zh" ? "类别" : "Category"}
                          </TableHead>
                          <TableHead>
                            {lang === "zh" ? "价格 ($/1M)" : "Price ($/1M)"}
                          </TableHead>
                          <TableHead>
                            {lang === "zh" ? "上下文" : "Context"}
                          </TableHead>
                          <TableHead>
                            {lang === "zh" ? "状态" : "Status"}
                          </TableHead>
                          <TableHead>
                            {lang === "zh" ? "操作" : "Actions"}
                          </TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {groupModels.map((model) => (
                          <TableRow key={model.id}>
                            <TableCell>
                              <div>
                                <div className="font-medium">
                                  {model.display_name}
                                </div>
                                <code className="text-xs text-muted-foreground">
                                  {model.name}
                                </code>
                              </div>
                            </TableCell>
                            <TableCell>
                              <Badge variant="outline">
                                {normalizeProvider(model.provider)}
                              </Badge>
                            </TableCell>
                            <TableCell>
                              <span className="text-xs text-muted-foreground">
                                {model.release_date
                                  ? new Date(model.release_date)
                                      .toISOString()
                                      .split("T")[0]
                                  : "-"}
                              </span>
                            </TableCell>
                            <TableCell>
                              {CATEGORIES.find(
                                (c) => c.value === model.category
                              )?.label[lang] || model.category}
                            </TableCell>
                            <TableCell>
                              {model.is_free ? (
                                <Badge variant="secondary">
                                  {lang === "zh" ? "免费" : "Free"}
                                </Badge>
                              ) : (
                                <span className="text-xs font-mono">
                                  ${model.input_price} / ${model.output_price}
                                </span>
                              )}
                            </TableCell>
                            <TableCell>
                              <span className="text-xs">
                                {model.context_window
                                  ? `${(model.context_window / 1000).toFixed(
                                      0
                                    )}K`
                                  : "-"}
                              </span>
                            </TableCell>
                            <TableCell>
                              <div className="flex gap-1">
                                {model.is_default && (
                                  <Badge>
                                    {lang === "zh" ? "默认" : "Default"}
                                  </Badge>
                                )}
                                {model.is_deprecated && (
                                  <Badge variant="destructive">
                                    {lang === "zh" ? "弃用" : "Deprecated"}
                                  </Badge>
                                )}
                                {!model.is_active && (
                                  <Badge variant="outline">
                                    {lang === "zh" ? "禁用" : "Disabled"}
                                  </Badge>
                                )}
                                {model.is_active && !model.is_deprecated && (
                                  <Badge variant="secondary">
                                    {lang === "zh" ? "启用" : "Active"}
                                  </Badge>
                                )}
                              </div>
                            </TableCell>
                            <TableCell>
                              <div className="flex gap-2">
                                <Button
                                  variant="outline"
                                  size="sm"
                                  onClick={() => handleEdit(model)}
                                >
                                  {t.edit}
                                </Button>
                                <Button
                                  variant="destructive"
                                  size="sm"
                                  onClick={() =>
                                    setDeleteTarget({
                                      id: model.id,
                                      name: model.display_name,
                                    })
                                  }
                                >
                                  {t.delete}
                                </Button>
                              </div>
                            </TableCell>
                          </TableRow>
                        ))}
                      </TableBody>
                    </Table>
                  </CollapsibleContent>
                </div>
              </Collapsible>
            );
          })}
        </div>
      )}

      {/* Edit Dialog */}
      <Dialog open={showDialog} onOpenChange={setShowDialog}>
        <DialogContent className="max-w-3xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>
              {editingModel
                ? lang === "zh"
                  ? "编辑模型"
                  : "Edit Model"
                : lang === "zh"
                ? "添加模型"
                : "Add Model"}
            </DialogTitle>
          </DialogHeader>

          <Tabs value={activeTab} onValueChange={setActiveTab}>
            <TabsList className="grid grid-cols-4 w-full">
              <TabsTrigger value="basic">
                {lang === "zh" ? "基本信息" : "Basic"}
              </TabsTrigger>
              <TabsTrigger value="pricing">
                {lang === "zh" ? "价格配置" : "Pricing"}
              </TabsTrigger>
              <TabsTrigger value="capabilities">
                {lang === "zh" ? "能力配置" : "Capabilities"}
              </TabsTrigger>
              <TabsTrigger value="deployment">
                {lang === "zh" ? "部署配置" : "Deployment"}
              </TabsTrigger>
            </TabsList>

            {/* Basic Tab */}
            <TabsContent value="basic" className="space-y-4 mt-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium">
                    {lang === "zh" ? "模型标识" : "Model Name"}
                  </label>
                  <Input
                    value={modelForm.name}
                    onChange={(e) =>
                      setModelForm({ ...modelForm, name: e.target.value })
                    }
                    placeholder="gpt-4o"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium">
                    {lang === "zh" ? "显示名称" : "Display Name"}
                  </label>
                  <Input
                    value={modelForm.display_name}
                    onChange={(e) =>
                      setModelForm({
                        ...modelForm,
                        display_name: e.target.value,
                      })
                    }
                    placeholder="GPT-4o"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium">
                    {lang === "zh" ? "公司" : "Company"}
                  </label>
                  <Select
                    value={modelForm.provider}
                    onValueChange={(v) =>
                      setModelForm({ ...modelForm, provider: v })
                    }
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {PROVIDERS.map((p) => (
                        <SelectItem key={p.value} value={p.value}>
                          {p.label}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium">
                    {lang === "zh" ? "类别" : "Category"}
                  </label>
                  <Select
                    value={modelForm.category}
                    onValueChange={(v) =>
                      setModelForm({ ...modelForm, category: v })
                    }
                  >
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      {CATEGORIES.map((c) => (
                        <SelectItem key={c.value} value={c.value}>
                          {c.label[lang]}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div>
                  <label className="text-sm font-medium">
                    {lang === "zh" ? "版本" : "Version"}
                  </label>
                  <Input
                    value={modelForm.version}
                    onChange={(e) =>
                      setModelForm({ ...modelForm, version: e.target.value })
                    }
                    placeholder="2024-01-01"
                  />
                </div>
              </div>

              <div>
                <label className="text-sm font-medium">
                  {lang === "zh" ? "描述" : "Description"}
                </label>
                <Input
                  value={modelForm.description}
                  onChange={(e) =>
                    setModelForm({ ...modelForm, description: e.target.value })
                  }
                />
              </div>

              <div className="grid grid-cols-3 gap-4">
                <div>
                  <label className="text-sm font-medium">
                    {lang === "zh" ? "开源协议" : "License"}
                  </label>
                  <Input
                    value={modelForm.license}
                    onChange={(e) =>
                      setModelForm({ ...modelForm, license: e.target.value })
                    }
                    placeholder="MIT / Apache / Commercial"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium">
                    {lang === "zh" ? "发布日期" : "Release Date"}
                  </label>
                  <Input
                    type="date"
                    value={modelForm.release_date}
                    onChange={(e) =>
                      setModelForm({
                        ...modelForm,
                        release_date: e.target.value,
                      })
                    }
                  />
                </div>
                <div>
                  <label className="text-sm font-medium">
                    {lang === "zh" ? "排序" : "Sort Order"}
                  </label>
                  <Input
                    type="number"
                    value={modelForm.sort_order}
                    onChange={(e) =>
                      setModelForm({
                        ...modelForm,
                        sort_order: parseInt(e.target.value) || 0,
                      })
                    }
                  />
                </div>
              </div>

              <div className="flex gap-6">
                <div className="flex items-center gap-2">
                  <Switch
                    checked={modelForm.is_active}
                    onCheckedChange={(v) =>
                      setModelForm({ ...modelForm, is_active: v })
                    }
                  />
                  <span className="text-sm">
                    {lang === "zh" ? "启用" : "Active"}
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <Switch
                    checked={modelForm.is_default}
                    onCheckedChange={(v) =>
                      setModelForm({ ...modelForm, is_default: v })
                    }
                  />
                  <span className="text-sm">
                    {lang === "zh" ? "设为默认" : "Default"}
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <Switch
                    checked={modelForm.is_deprecated}
                    onCheckedChange={(v) =>
                      setModelForm({ ...modelForm, is_deprecated: v })
                    }
                  />
                  <span className="text-sm">
                    {lang === "zh" ? "已弃用" : "Deprecated"}
                  </span>
                </div>
              </div>
            </TabsContent>

            {/* Pricing Tab */}
            <TabsContent value="pricing" className="space-y-4 mt-4">
              <div className="flex items-center gap-2 mb-4">
                <Switch
                  checked={modelForm.is_free}
                  onCheckedChange={(v) =>
                    setModelForm({ ...modelForm, is_free: v })
                  }
                />
                <span className="text-sm font-medium">
                  {lang === "zh" ? "免费模型" : "Free Model"}
                </span>
              </div>

              {!modelForm.is_free && (
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-medium">
                      {lang === "zh"
                        ? "输入价格 ($/1M tokens)"
                        : "Input Price ($/1M)"}
                    </label>
                    <Input
                      type="number"
                      step="0.01"
                      value={modelForm.input_price}
                      onChange={(e) =>
                        setModelForm({
                          ...modelForm,
                          input_price: parseFloat(e.target.value) || 0,
                        })
                      }
                    />
                  </div>
                  <div>
                    <label className="text-sm font-medium">
                      {lang === "zh"
                        ? "输出价格 ($/1M tokens)"
                        : "Output Price ($/1M)"}
                    </label>
                    <Input
                      type="number"
                      step="0.01"
                      value={modelForm.output_price}
                      onChange={(e) =>
                        setModelForm({
                          ...modelForm,
                          output_price: parseFloat(e.target.value) || 0,
                        })
                      }
                    />
                  </div>
                </div>
              )}

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium">
                    {lang === "zh" ? "上下文窗口" : "Context Window"}
                  </label>
                  <Input
                    type="number"
                    value={modelForm.context_window}
                    onChange={(e) =>
                      setModelForm({
                        ...modelForm,
                        context_window: parseInt(e.target.value) || 0,
                      })
                    }
                  />
                </div>
                <div>
                  <label className="text-sm font-medium">
                    {lang === "zh" ? "最大输出 Tokens" : "Max Output Tokens"}
                  </label>
                  <Input
                    type="number"
                    value={modelForm.max_output_tokens}
                    onChange={(e) =>
                      setModelForm({
                        ...modelForm,
                        max_output_tokens: parseInt(e.target.value) || 0,
                      })
                    }
                  />
                </div>
              </div>

              <div className="grid grid-cols-3 gap-4">
                <div>
                  <label className="text-sm font-medium">
                    {lang === "zh" ? "RPM 限制" : "RPM Limit"}
                  </label>
                  <Input
                    type="number"
                    value={modelForm.rate_limit.rpm || ""}
                    onChange={(e) =>
                      setModelForm({
                        ...modelForm,
                        rate_limit: {
                          ...modelForm.rate_limit,
                          rpm: parseInt(e.target.value) || 0,
                        },
                      })
                    }
                    placeholder="500"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium">
                    {lang === "zh" ? "TPM 限制" : "TPM Limit"}
                  </label>
                  <Input
                    type="number"
                    value={modelForm.rate_limit.tpm || ""}
                    onChange={(e) =>
                      setModelForm({
                        ...modelForm,
                        rate_limit: {
                          ...modelForm.rate_limit,
                          tpm: parseInt(e.target.value) || 0,
                        },
                      })
                    }
                    placeholder="100000"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium">
                    {lang === "zh" ? "平均延迟 (ms)" : "Latency (ms)"}
                  </label>
                  <Input
                    type="number"
                    value={modelForm.latency_ms}
                    onChange={(e) =>
                      setModelForm({
                        ...modelForm,
                        latency_ms: parseInt(e.target.value) || 0,
                      })
                    }
                  />
                </div>
              </div>

              <div>
                <label className="text-sm font-medium">
                  {lang === "zh" ? "质量评分 (1-10)" : "Quality Score (1-10)"}
                </label>
                <Input
                  type="number"
                  step="0.1"
                  min="1"
                  max="10"
                  value={modelForm.quality_score}
                  onChange={(e) =>
                    setModelForm({
                      ...modelForm,
                      quality_score: parseFloat(e.target.value) || 0,
                    })
                  }
                />
              </div>

              <div>
                <label className="text-sm font-medium">
                  {lang === "zh" ? "备用模型" : "Fallback Model"}
                </label>
                <Select
                  value={modelForm.fallback_model_id || "__none__"}
                  onValueChange={(v) =>
                    setModelForm({
                      ...modelForm,
                      fallback_model_id: v === "__none__" ? "" : v,
                    })
                  }
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="__none__">
                      {lang === "zh" ? "无" : "None"}
                    </SelectItem>
                    {models
                      .filter((m) => m.id !== editingModel?.id && m.is_active)
                      .map((m) => (
                        <SelectItem key={m.id} value={m.id}>
                          {m.display_name}
                        </SelectItem>
                      ))}
                  </SelectContent>
                </Select>
              </div>
            </TabsContent>

            {/* Capabilities Tab */}
            <TabsContent value="capabilities" className="space-y-4 mt-4">
              <div>
                <label className="text-sm font-medium mb-2 block">
                  {lang === "zh" ? "模型能力" : "Capabilities"}
                </label>
                <div className="flex flex-wrap gap-2">
                  {CAPABILITIES_OPTIONS.map((cap) => (
                    <Badge
                      key={cap}
                      variant={
                        modelForm.capabilities.includes(cap)
                          ? "default"
                          : "outline"
                      }
                      className="cursor-pointer"
                      onClick={() => toggleCapability(cap)}
                    >
                      {cap}
                    </Badge>
                  ))}
                </div>
              </div>
            </TabsContent>

            {/* Deployment Tab */}
            <TabsContent value="deployment" className="space-y-4 mt-4">
              <div>
                <label className="text-sm font-medium">
                  {lang === "zh" ? "部署类型" : "Deployment Type"}
                </label>
                <Select
                  value={modelForm.deployment_type}
                  onValueChange={(v) =>
                    setModelForm({ ...modelForm, deployment_type: v })
                  }
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {DEPLOYMENT_TYPES.map((d) => (
                      <SelectItem key={d.value} value={d.value}>
                        {d.label[lang]}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {modelForm.deployment_type === "api" && (
                <>
                  <div>
                    <label className="text-sm font-medium">API Endpoint</label>
                    <Input
                      value={modelForm.api_endpoint}
                      onChange={(e) =>
                        setModelForm({
                          ...modelForm,
                          api_endpoint: e.target.value,
                        })
                      }
                      placeholder="https://api.openai.com/v1"
                    />
                  </div>
                  <div>
                    <label className="text-sm font-medium">
                      API Key (
                      {lang === "zh" ? "可选，覆盖全局配置" : "Optional"})
                    </label>
                    <Input
                      type="password"
                      value={modelForm.config.api_key || ""}
                      onChange={(e) =>
                        setModelForm({
                          ...modelForm,
                          config: {
                            ...modelForm.config,
                            api_key: e.target.value,
                          },
                        })
                      }
                      placeholder="sk-..."
                    />
                  </div>
                </>
              )}

              {modelForm.deployment_type === "local" && (
                <>
                  <div>
                    <label className="text-sm font-medium">Docker Image</label>
                    <Input
                      value={modelForm.docker_image}
                      onChange={(e) =>
                        setModelForm({
                          ...modelForm,
                          docker_image: e.target.value,
                        })
                      }
                      placeholder="ollama/ollama:latest"
                    />
                  </div>
                  <div className="grid grid-cols-3 gap-4">
                    <div>
                      <label className="text-sm font-medium">GPU</label>
                      <Input
                        value={modelForm.hardware_requirements.gpu || ""}
                        onChange={(e) =>
                          setModelForm({
                            ...modelForm,
                            hardware_requirements: {
                              ...modelForm.hardware_requirements,
                              gpu: e.target.value,
                            },
                          })
                        }
                        placeholder="NVIDIA RTX 4090"
                      />
                    </div>
                    <div>
                      <label className="text-sm font-medium">VRAM</label>
                      <Input
                        value={modelForm.hardware_requirements.vram || ""}
                        onChange={(e) =>
                          setModelForm({
                            ...modelForm,
                            hardware_requirements: {
                              ...modelForm.hardware_requirements,
                              vram: e.target.value,
                            },
                          })
                        }
                        placeholder="24GB"
                      />
                    </div>
                    <div>
                      <label className="text-sm font-medium">RAM</label>
                      <Input
                        value={modelForm.hardware_requirements.ram || ""}
                        onChange={(e) =>
                          setModelForm({
                            ...modelForm,
                            hardware_requirements: {
                              ...modelForm.hardware_requirements,
                              ram: e.target.value,
                            },
                          })
                        }
                        placeholder="32GB"
                      />
                    </div>
                  </div>
                </>
              )}

              {modelForm.deployment_type === "hybrid" && (
                <div className="text-sm text-muted-foreground">
                  {lang === "zh"
                    ? "混合模式：同时配置 API 和本地部署信息，系统会根据负载自动选择"
                    : "Hybrid mode: Configure both API and local deployment, system will auto-select based on load"}
                </div>
              )}
            </TabsContent>
          </Tabs>

          <DialogFooter>
            <Button variant="outline" onClick={() => setShowDialog(false)}>
              {t.cancel}
            </Button>
            <Button onClick={handleSave}>{t.save}</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Delete Confirmation */}
      <AlertDialog
        open={!!deleteTarget}
        onOpenChange={() => setDeleteTarget(null)}
      >
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>{t.confirmDelete}</AlertDialogTitle>
            <AlertDialogDescription>
              {lang === "zh"
                ? `确定要删除 "${deleteTarget?.name}" 吗？此操作不可撤销。`
                : `Are you sure you want to delete "${deleteTarget?.name}"? This action cannot be undone.`}
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>{t.cancel}</AlertDialogCancel>
            <AlertDialogAction onClick={handleDelete}>
              {t.delete}
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
}
