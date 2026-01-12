import { useState, useEffect, useCallback } from "react";
import { adminLocales, type Language } from "@/common/i18n";
import { useInfiniteScroll } from "@/common/hooks";
import { StatCard } from "@/modules/admin/components/StatCard";
import { LoadMoreIndicator } from "@/modules/admin/components/LoadMoreIndicator";
import { TagFilter } from "@/modules/admin/components/TagFilter";
import { getApiBase, getAuthHeaders } from "@/modules/admin/utils/api";
import { Button } from "@/libs/shadcn/ui/button";
import { Input } from "@/libs/shadcn/ui/input";
import { Badge } from "@/libs/shadcn/ui/badge";
import { Card, CardContent } from "@/libs/shadcn/ui/card";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/libs/shadcn/ui/dialog";

const API_BASE = getApiBase();
const getHeaders = getAuthHeaders;

interface Prompt {
  id: string;
  name: string;
  description: string;
  template: string;
  category: string;
  source: string;
  repo: string;
  is_active: boolean;
  created_at: string;
}

interface PromptStats {
  total: number;
  active: number;
  inactive: number;
  categories: { category: string; count: number }[];
  sources: { source: string; count: number }[];
}

interface CategoryLabel {
  id: string;
  code: string;
  label_zh: string;
  label_en: string;
  type: string;
  sort_order: number;
}

interface PromptsViewProps {
  lang: Language;
}

const getSourceVariant = (
  src: string
): "default" | "secondary" | "destructive" | "outline" => {
  if (src?.includes("system")) return "secondary";
  if (src?.includes("anthropic")) return "default";
  if (src?.includes("claude")) return "default";
  return "outline";
};

export default function PromptsView({ lang }: PromptsViewProps) {
  const t = adminLocales[lang];
  const [stats, setStats] = useState<PromptStats | null>(null);
  const [isSyncing, setIsSyncing] = useState(false);
  const [selectedPrompt, setSelectedPrompt] = useState<Prompt | null>(null);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("__all__");
  const [source, setSource] = useState("__all__");
  const [categoryLabels, setCategoryLabels] = useState<CategoryLabel[]>([]);
  const [sourceLabels, setSourceLabels] = useState<CategoryLabel[]>([]);

  const getCategoryLabel = useCallback(
    (code: string) => {
      if (!code) return "";
      const label = categoryLabels.find((l) => l.code === code);
      return label ? (lang === "zh" ? label.label_zh : label.label_en) : code;
    },
    [categoryLabels, lang]
  );

  const getSourceLabel = useCallback(
    (code: string) => {
      if (!code) return "";
      const label = sourceLabels.find((l) => l.code === code);
      return label ? (lang === "zh" ? label.label_zh : label.label_en) : code;
    },
    [sourceLabels, lang]
  );

  const fetchLabels = useCallback(async () => {
    try {
      const response = await fetch(`${API_BASE}/prompts/labels`, {
        headers: getHeaders(),
      });
      const json = await response.json();
      if (json.success) {
        setCategoryLabels(json.data.categories || []);
        setSourceLabels(json.data.sources || []);
      }
    } catch {
      // ignore
    }
  }, []);

  const fetchStats = useCallback(async () => {
    try {
      const res = await fetch(`${API_BASE}/prompts/stats`, {
        headers: getHeaders(),
      });
      const json = await res.json();
      if (json.success) setStats(json.data);
    } catch {
      // 由中间件统一处理
    }
  }, []);

  const fetchPrompts = useCallback(
    async (page: number) => {
      const params = new URLSearchParams();
      params.set("page", page.toString());
      params.set("limit", "20");
      if (search) params.set("search", search);
      if (category && category !== "__all__") params.set("category", category);
      if (source && source !== "__all__") params.set("source", source);

      const res = await fetch(`${API_BASE}/prompts?${params}`, {
        headers: getHeaders(),
      });
      const json = await res.json();
      return { data: json.data || [], total: json.meta?.total || 0 };
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
  } = useInfiniteScroll<Prompt>({
    fetchFn: fetchPrompts,
  });

  useEffect(() => {
    fetchLabels();
    fetchStats();
  }, [fetchLabels, fetchStats]);

  const handleToggle = async (id: string) => {
    await fetch(`${API_BASE}/prompts/${id}/toggle`, {
      method: "POST",
      headers: getHeaders(),
    });
    fetchStats();
    refresh();
  };

  const handleSync = async () => {
    setIsSyncing(true);
    try {
      const res = await fetch(`${API_BASE}/prompts/sync`, {
        method: "POST",
        headers: getHeaders(),
      });
      const json = await res.json();
      if (json.success) {
        alert(t.syncedCount.replace("{count}", String(json.data.synced)));
        fetchStats();
        refresh();
      }
    } catch {
      alert(t.syncFailed);
    } finally {
      setIsSyncing(false);
    }
  };

  const handleReset = () => {
    setSearch("");
    setCategory("__all__");
    setSource("__all__");
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-foreground">{t.prompts}</h1>
        <Button onClick={handleSync} disabled={isSyncing}>
          {isSyncing ? t.loading : t.syncPrompts}
        </Button>
      </div>

      {stats && (
        <div className="grid grid-cols-4 gap-4">
          <StatCard value={stats.total} label={t.total} />
          <StatCard value={stats.active} label={t.active} color="green" />
          <StatCard value={stats.inactive} label={t.inactive} color="muted" />
          <StatCard
            value={stats.categories.length}
            label={t.promptCategory}
            color="violet"
          />
        </div>
      )}

      {/* Category 标签 */}
      {stats && stats.categories.length > 0 && (
        <TagFilter
          lang={lang}
          label={t.category}
          options={stats.categories
            .filter((c) => c.category)
            .map((c) => ({
              value: c.category,
              label: getCategoryLabel(c.category),
              count: c.count,
            }))}
          value={category}
          onChange={setCategory}
          color="violet"
        />
      )}

      {/* Source 标签 */}
      {stats && stats.sources.length > 0 && (
        <TagFilter
          lang={lang}
          label={t.source}
          options={stats.sources
            .filter((s) => s.source)
            .map((s) => ({
              value: s.source,
              label: getSourceLabel(s.source),
              count: s.count,
            }))}
          value={source}
          onChange={setSource}
          color="blue"
        />
      )}

      {/* 搜索和重置 */}
      <div className="flex gap-4 items-center">
        <Input
          type="text"
          placeholder={t.search}
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-64"
        />
        {(search || category !== "__all__" || source !== "__all__") && (
          <Button variant="outline" size="sm" onClick={handleReset}>
            {t.reset}
          </Button>
        )}
      </div>

      {isLoading && prompts.length === 0 ? (
        <div className="flex items-center justify-center h-64 text-muted-foreground">
          {t.loading}
        </div>
      ) : prompts.length === 0 ? (
        <div className="text-center text-muted-foreground py-12">
          {t.noData}
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {prompts.map((prompt) => (
              <PromptCard
                key={prompt.id}
                prompt={prompt}
                lang={lang}
                onClick={() => setSelectedPrompt(prompt)}
                onToggle={() => handleToggle(prompt.id)}
                getCategoryLabel={getCategoryLabel}
                getSourceLabel={getSourceLabel}
              />
            ))}
          </div>
          <LoadMoreIndicator
            loadMoreRef={loadMoreRef}
            hasMore={hasMore}
            isLoading={isLoading}
            total={total}
            count={prompts.length}
            lang={lang}
          />
        </>
      )}

      {selectedPrompt && (
        <PromptDetailModal
          lang={lang}
          prompt={selectedPrompt}
          onClose={() => setSelectedPrompt(null)}
          onToggle={() => {
            handleToggle(selectedPrompt.id);
            setSelectedPrompt(null);
          }}
          getCategoryLabel={getCategoryLabel}
          getSourceLabel={getSourceLabel}
        />
      )}
    </div>
  );
}

function PromptCard({
  prompt,
  lang,
  onClick,
  onToggle,
  getCategoryLabel,
  getSourceLabel,
}: {
  prompt: Prompt;
  lang: Language;
  onClick: () => void;
  onToggle: () => void;
  getCategoryLabel: (code: string) => string;
  getSourceLabel: (code: string) => string;
}) {
  const t = adminLocales[lang];
  return (
    <Card
      className={`cursor-pointer hover:border-primary/50 transition-all ${
        !prompt.is_active ? "opacity-60" : ""
      }`}
      onClick={onClick}
    >
      <CardContent className="p-4">
        <div className="flex items-start justify-between mb-2">
          <h3 className="font-medium truncate flex-1 text-foreground">
            {prompt.name}
          </h3>
          <Badge variant={getSourceVariant(prompt.source)} className="ml-2">
            {getSourceLabel(prompt.source)}
          </Badge>
        </div>
        <p className="text-sm text-muted-foreground line-clamp-2 mb-3">
          {prompt.description}
        </p>
        <div className="flex items-center justify-between">
          <Badge variant="outline">{getCategoryLabel(prompt.category)}</Badge>
          <Button
            variant="ghost"
            size="sm"
            onClick={(e) => {
              e.stopPropagation();
              onToggle();
            }}
          >
            <Badge variant={prompt.is_active ? "default" : "secondary"}>
              {prompt.is_active ? t.active : t.inactive}
            </Badge>
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}

function PromptDetailModal({
  lang,
  prompt,
  onClose,
  onToggle,
  getCategoryLabel,
  getSourceLabel,
}: {
  lang: Language;
  prompt: Prompt;
  onClose: () => void;
  onToggle: () => void;
  getCategoryLabel: (code: string) => string;
  getSourceLabel: (code: string) => string;
}) {
  const t = adminLocales[lang];

  const handleCopyTemplate = () => {
    if (prompt.template) {
      navigator.clipboard.writeText(prompt.template);
      alert(t.copied);
    }
  };

  return (
    <Dialog open={true} onOpenChange={(o) => !o && onClose()}>
      <DialogContent className="max-w-2xl max-h-[80vh] overflow-hidden flex flex-col">
        <DialogHeader>
          <DialogTitle className="truncate">{prompt.name}</DialogTitle>
          <div className="flex items-center gap-2 mt-2">
            <Badge variant={getSourceVariant(prompt.source)}>
              {getSourceLabel(prompt.source)}
            </Badge>
            <Badge variant="outline">{getCategoryLabel(prompt.category)}</Badge>
          </div>
        </DialogHeader>

        <div className="flex-1 overflow-y-auto space-y-4">
          {prompt.description && (
            <div>
              <h3 className="text-sm font-medium text-muted-foreground mb-2">
                {t.description}
              </h3>
              <p className="text-foreground">{prompt.description}</p>
            </div>
          )}

          {prompt.repo && (
            <div>
              <h3 className="text-sm font-medium text-muted-foreground mb-2">
                {t.repo}
              </h3>
              <a
                href={prompt.repo}
                target="_blank"
                rel="noopener noreferrer"
                className="text-primary hover:underline break-all"
              >
                {prompt.repo}
              </a>
            </div>
          )}

          {prompt.template && (
            <div>
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-medium text-muted-foreground">
                  {t.template}
                </h3>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleCopyTemplate}
                >
                  {t.copy}
                </Button>
              </div>
              <pre className="bg-muted rounded-lg p-4 text-sm text-foreground overflow-x-auto whitespace-pre-wrap">
                {prompt.template}
              </pre>
            </div>
          )}
        </div>

        <DialogFooter className="flex justify-between sm:justify-between">
          <Button
            variant={prompt.is_active ? "outline" : "default"}
            onClick={onToggle}
          >
            {prompt.is_active ? t.inactive : t.active}
          </Button>
          <Button variant="outline" onClick={onClose}>
            {t.close}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
