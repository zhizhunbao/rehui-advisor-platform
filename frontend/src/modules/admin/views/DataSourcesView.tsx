import { useState, useEffect, useCallback } from "react";
import { adminLocales, type Language } from "@/common/i18n";
import { useInfiniteScroll } from "@/common/hooks";
import { StatCard } from "@/modules/admin/components/StatCard";
import { LoadMoreIndicator } from "@/modules/admin/components/LoadMoreIndicator";
import { TagFilter } from "@/modules/admin/components/TagFilter";
import { getApiBase, getAuthHeaders } from "@/common/helper";
import {
  DataSourceCard,
  type DataSource,
} from "@/modules/admin/components/DataSourceCard";
import {
  SourceDetailModal,
  AddSourceModal,
} from "@/modules/admin/components/DataSourceModals";
import { GitHubDiscoverModal } from "@/modules/admin/components/GitHubDiscoverModal";
import { Button } from "@/libs/shadcn/ui/button";
import { Input } from "@/libs/shadcn/ui/input";
import { Card, CardContent } from "@/libs/shadcn/ui/card";

interface Stats {
  total: number;
  by_type: Record<string, number>;
  by_status: Record<string, number>;
  by_category: { category: string; count: number }[];
}

interface Category {
  id: string;
  code: string;
  name: string;
  nameEn: string;
  count: number;
}

interface Domain {
  id: string;
  code: string;
  name: string;
  nameEn: string;
  count: number;
}

interface TypeItem {
  type: string;
  count: number;
}

interface StatusItem {
  status: string;
  count: number;
}

interface LanguageItem {
  language: string;
  count: number;
}

interface DataSourcesViewProps {
  lang: Language;
}

const API_BASE = getApiBase();
const getHeaders = getAuthHeaders;

export default function DataSourcesView({ lang }: DataSourcesViewProps) {
  const t = adminLocales[lang];
  const [stats, setStats] = useState<Stats | null>(null);
  const [categories, setCategories] = useState<Category[]>([]);
  const [domains, setDomains] = useState<Domain[]>([]);
  const [types, setTypes] = useState<TypeItem[]>([]);
  const [statuses, setStatuses] = useState<StatusItem[]>([]);
  const [languages, setLanguages] = useState<LanguageItem[]>([]);
  const [selectedSource, setSelectedSource] = useState<DataSource | null>(null);
  const [showAddModal, setShowAddModal] = useState(false);
  const [showDiscoverModal, setShowDiscoverModal] = useState(false);
  const [search, setSearch] = useState("");
  const [categoryId, setCategoryId] = useState("__all__");
  const [domainId, setDomainId] = useState("__all__");
  const [status, setStatus] = useState("__all__");
  const [type, setType] = useState("__all__");
  const [language, setLanguage] = useState("__all__");

  // 是否为分组模式（没有任何筛选条件时按分类分组显示）
  const isGroupedMode =
    !search &&
    categoryId === "__all__" &&
    domainId === "__all__" &&
    status === "__all__" &&
    type === "__all__" &&
    language === "__all__";

  const fetchCategories = useCallback(async () => {
    try {
      const res = await fetch(`${API_BASE}/data-sources/categories`, {
        headers: getHeaders(),
      });
      const json = await res.json();
      if (json.success) setCategories(json.data);
    } catch (err) {
      console.error("Failed to fetch categories:", err);
    }
  }, []);

  const fetchDomains = useCallback(async (catId: string) => {
    try {
      // 如果是全部分类，获取所有领域；否则获取指定分类下的领域
      const url =
        catId === "__all__"
          ? `${API_BASE}/data-sources/domains`
          : `${API_BASE}/data-sources/categories/${catId}/domains`;
      const res = await fetch(url, {
        headers: getHeaders(),
      });
      const json = await res.json();
      if (json.success) setDomains(json.data);
    } catch (err) {
      console.error("Failed to fetch domains:", err);
    }
  }, []);

  const fetchSources = useCallback(
    async (page: number) => {
      const params = new URLSearchParams();
      params.set("page", page.toString());
      params.set("limit", "20");
      if (search) params.set("search", search);
      if (categoryId && categoryId !== "__all__")
        params.set("category_id", categoryId);
      if (domainId && domainId !== "__all__") params.set("domain_id", domainId);
      if (status && status !== "__all__") params.set("status", status);
      if (type && type !== "__all__") params.set("type", type);
      if (language && language !== "__all__") params.set("language", language);

      const res = await fetch(`${API_BASE}/data-sources?${params}`, {
        headers: getHeaders(),
      });
      const json = await res.json();
      return { data: json.data || [], total: json.meta?.total || 0 };
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
  } = useInfiniteScroll<DataSource>({
    fetchFn: fetchSources,
  });

  const fetchStats = useCallback(async () => {
    try {
      const res = await fetch(`${API_BASE}/data-sources/stats`, {
        headers: getHeaders(),
      });
      const json = await res.json();
      if (json.success) setStats(json.data);
    } catch (err) {
      console.error("Failed to fetch stats:", err);
    }
  }, []);

  useEffect(() => {
    const loadInitialData = async () => {
      try {
        const [statsRes, categoriesRes, typesRes, statusesRes, languagesRes] =
          await Promise.all([
            fetch(`${API_BASE}/data-sources/stats`, { headers: getHeaders() }),
            fetch(`${API_BASE}/data-sources/categories`, {
              headers: getHeaders(),
            }),
            fetch(`${API_BASE}/data-sources/types`, { headers: getHeaders() }),
            fetch(`${API_BASE}/data-sources/statuses`, {
              headers: getHeaders(),
            }),
            fetch(`${API_BASE}/data-sources/languages`, {
              headers: getHeaders(),
            }),
          ]);
        const statsJson = await statsRes.json();
        const categoriesJson = await categoriesRes.json();
        const typesJson = await typesRes.json();
        const statusesJson = await statusesRes.json();
        const languagesJson = await languagesRes.json();
        if (statsJson.success) setStats(statsJson.data);
        if (categoriesJson.success) setCategories(categoriesJson.data);
        if (typesJson.success) setTypes(typesJson.data);
        if (statusesJson.success) setStatuses(statusesJson.data);
        if (languagesJson.success) setLanguages(languagesJson.data);
      } catch (err) {
        console.error("Failed to fetch initial data:", err);
      }
    };
    loadInitialData();
  }, []);

  // �?categoryId 变化时，重新获取 domains
  useEffect(() => {
    fetchDomains(categoryId);
    // 重置 domainId
    setDomainId("__all__");
  }, [categoryId, fetchDomains]);

  const handleRefresh = async (id: string) => {
    await fetch(`${API_BASE}/data-sources/${id}/refresh`, {
      method: "POST",
      headers: getHeaders(),
    });
    refresh();
    fetchStats();
  };

  const handleDelete = async (id: string) => {
    if (!confirm(t.confirmDelete)) return;
    await fetch(`${API_BASE}/data-sources/${id}`, {
      method: "DELETE",
      headers: getHeaders(),
    });
    refresh();
    fetchStats();
  };

  const handleRefreshAll = async () => {
    if (!confirm(t.confirmRefreshAll)) return;
    const res = await fetch(`${API_BASE}/data-sources/refresh-all`, {
      method: "POST",
      headers: getHeaders(),
    });
    const json = await res.json();
    if (json.success) {
      alert(t.syncedCount.replace("{count}", json.data.refreshed));
      refresh();
      fetchStats();
    }
  };

  const handleReset = () => {
    setSearch("");
    setCategoryId("__all__");
    setDomainId("__all__");
    setStatus("__all__");
    setType("__all__");
    setLanguage("__all__");
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-foreground">{t.dataSources}</h1>
        <div className="flex gap-2">
          <Button variant="outline" onClick={() => setShowDiscoverModal(true)}>
            🔍 {t.discover}
          </Button>
          <Button variant="outline" onClick={handleRefreshAll}>
            {t.refreshAll}
          </Button>
          <Button onClick={() => setShowAddModal(true)}>{t.addSource}</Button>
        </div>
      </div>

      {stats && (
        <div className="grid grid-cols-5 gap-4">
          <StatCard value={stats.total} label={t.total} />
          <StatCard
            value={stats.by_status.active || 0}
            label={t.active}
            color="green"
          />
          <StatCard
            value={stats.by_type.github || 0}
            label="GitHub"
            color="violet"
          />
          <StatCard value={stats.by_type.api || 0} label="API" color="blue" />
          <StatCard
            value={stats.by_type.website || 0}
            label="Website"
            color="amber"
          />
        </div>
      )}

      <Card>
        <CardContent className="p-4 space-y-4">
          {/* 搜索和重�?*/}
          <div className="flex gap-4 items-center">
            <Input
              type="text"
              placeholder={t.search}
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-64"
            />
            <Button variant="outline" onClick={handleReset}>
              {t.reset}
            </Button>
          </div>

          {/* Type 标签 */}
          {types.length > 0 && (
            <TagFilter
              lang={lang}
              label={t.type}
              options={types.map((t) => ({
                value: t.type,
                label: t.type,
                count: t.count,
              }))}
              value={type}
              onChange={setType}
              color="violet"
            />
          )}

          {/* Category 标签 (一级分�? */}
          {categories.filter((c) => c.id).length > 0 && (
            <TagFilter
              lang={lang}
              label={t.category}
              options={categories
                .filter((c) => c.id)
                .map((c) => ({
                  value: c.id,
                  label: lang === "zh" ? c.name : c.nameEn || c.name,
                  count: c.count,
                }))}
              value={categoryId}
              onChange={setCategoryId}
              color="blue"
            />
          )}

          {/* Domain 标签 (二级领域) */}
          {domains.length > 0 && (
            <TagFilter
              lang={lang}
              label={t.domain}
              options={domains.map((d) => ({
                value: d.id,
                label: lang === "zh" ? d.name : d.nameEn || d.name,
                count: d.count,
              }))}
              value={domainId}
              onChange={setDomainId}
              color="emerald"
            />
          )}

          {/* Status 标签 */}
          {statuses.length > 0 && (
            <TagFilter
              lang={lang}
              label={t.status}
              options={statuses.map((s) => ({
                value: s.status,
                label: s.status,
                count: s.count,
              }))}
              value={status}
              onChange={setStatus}
              color="amber"
            />
          )}

          {/* Language 标签 */}
          {languages.length > 0 && (
            <TagFilter
              lang={lang}
              label={t.language}
              options={languages.map((l) => ({
                value: l.language,
                label: l.language,
                count: l.count,
              }))}
              value={language}
              onChange={setLanguage}
              color="rose"
            />
          )}
        </CardContent>
      </Card>

      {isLoading && sources.length === 0 ? (
        <div className="flex items-center justify-center h-64 text-muted-foreground">
          {t.loading}
        </div>
      ) : isGroupedMode ? (
        <GroupedSourcesView
          lang={lang}
          sources={sources}
          categories={categories}
          onSelect={setSelectedSource}
          onRefresh={handleRefresh}
          onDelete={handleDelete}
        />
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {sources.map((source) => (
              <DataSourceCard
                key={source.id}
                source={source}
                lang={lang}
                onClick={() => setSelectedSource(source)}
                onRefresh={() => handleRefresh(source.id)}
                onDelete={() => handleDelete(source.id)}
              />
            ))}
          </div>
          <LoadMoreIndicator
            loadMoreRef={loadMoreRef}
            hasMore={hasMore}
            isLoading={isLoading}
            total={total}
            count={sources.length}
            lang={lang}
          />
        </>
      )}

      {selectedSource && (
        <SourceDetailModal
          lang={lang}
          source={selectedSource}
          onClose={() => setSelectedSource(null)}
          onRefresh={() => {
            handleRefresh(selectedSource.id);
            setSelectedSource(null);
          }}
        />
      )}
      {showAddModal && (
        <AddSourceModal
          lang={lang}
          categories={categories}
          onClose={() => setShowAddModal(false)}
          onSuccess={() => {
            setShowAddModal(false);
            refresh();
            fetchStats();
            fetchCategories();
          }}
        />
      )}
      {showDiscoverModal && (
        <GitHubDiscoverModal
          lang={lang}
          categories={categories}
          onClose={() => setShowDiscoverModal(false)}
          onSuccess={() => {
            refresh();
            fetchStats();
            fetchCategories();
          }}
        />
      )}
    </div>
  );
}

// ============ GroupedSourcesView ============
interface GroupedSourcesViewProps {
  lang: Language;
  sources: DataSource[];
  categories: Category[];
  onSelect: (source: DataSource) => void;
  onRefresh: (id: string) => void;
  onDelete: (id: string) => void;
}

function GroupedSourcesView({
  lang,
  sources,
  categories,
  onSelect,
  onRefresh,
  onDelete,
}: GroupedSourcesViewProps) {
  const t = adminLocales[lang];

  // 按分类分组数据源
  const groupedSources = categories
    .filter((cat) => cat.id && sources.some((s) => s.category_id === cat.id))
    .map((cat) => ({
      category: cat,
      sources: sources.filter((s) => s.category_id === cat.id),
    }));

  // 未分类的数据�?
  const uncategorizedSources = sources.filter(
    (s) => !s.category_id || !categories.some((c) => c.id === s.category_id)
  );

  if (groupedSources.length === 0 && uncategorizedSources.length === 0) {
    return (
      <div className="text-center text-muted-foreground py-12">{t.noData}</div>
    );
  }

  return (
    <div className="space-y-8">
      {groupedSources.map(({ category, sources: catSources }) => (
        <Card key={category.id}>
          <CardContent className="p-6">
            <div className="flex items-center gap-2 mb-4">
              <h2 className="text-xl font-bold text-foreground">
                {lang === "zh"
                  ? category.name
                  : category.nameEn || category.name}{" "}
                <span className="text-sm font-normal text-muted-foreground">
                  ({catSources.length})
                </span>
              </h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {catSources.map((source) => (
                <DataSourceCard
                  key={source.id}
                  source={source}
                  lang={lang}
                  onClick={() => onSelect(source)}
                  onRefresh={() => onRefresh(source.id)}
                  onDelete={() => onDelete(source.id)}
                />
              ))}
            </div>
          </CardContent>
        </Card>
      ))}
      {uncategorizedSources.length > 0 && (
        <Card>
          <CardContent className="p-6">
            <div className="flex items-center gap-2 mb-4">
              <h2 className="text-xl font-bold text-foreground">
                {t.uncategorized}{" "}
                <span className="text-sm font-normal text-muted-foreground">
                  ({uncategorizedSources.length})
                </span>
              </h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {uncategorizedSources.map((source) => (
                <DataSourceCard
                  key={source.id}
                  source={source}
                  lang={lang}
                  onClick={() => onSelect(source)}
                  onRefresh={() => onRefresh(source.id)}
                  onDelete={() => onDelete(source.id)}
                />
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
