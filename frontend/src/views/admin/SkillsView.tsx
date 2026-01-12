import { useState, useEffect, useCallback } from "react";
import { adminLocales, type Language } from "@/locales";
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

interface Skill {
  id: string;
  name: string;
  description: string;
  category: string;
  source: string;
  repo: string;
  content: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

interface SkillStats {
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

interface SkillsViewProps {
  lang: Language;
}

const getSourceVariant = (
  src: string
): "default" | "secondary" | "destructive" | "outline" => {
  switch (src) {
    case "official":
      return "default";
    case "claude-code":
      return "secondary";
    default:
      return "outline";
  }
};

const API_BASE = getApiBase();
const getHeaders = getAuthHeaders;

export default function SkillsView({ lang }: SkillsViewProps) {
  const t = adminLocales[lang];
  const [stats, setStats] = useState<SkillStats | null>(null);
  const [isSyncing, setIsSyncing] = useState(false);
  const [selectedSkill, setSelectedSkill] = useState<Skill | null>(null);
  const [search, setSearch] = useState("");
  const [filterCategory, setFilterCategory] = useState("__all__");
  const [filterSource, setFilterSource] = useState("__all__");
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
      const response = await fetch(`${API_BASE}/skills/labels`, {
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
      const response = await fetch(`${API_BASE}/skills/stats`, {
        headers: getHeaders(),
      });
      const json = await response.json();
      if (json.success) setStats(json.data);
    } catch {
      // 由中间件统一处理
    }
  }, []);

  const fetchSkills = useCallback(
    async (page: number) => {
      const params = new URLSearchParams();
      params.set("page", page.toString());
      params.set("limit", "20");
      if (search) params.set("search", search);
      if (filterCategory && filterCategory !== "__all__")
        params.set("category", filterCategory);
      if (filterSource && filterSource !== "__all__")
        params.set("source", filterSource);

      const res = await fetch(`${API_BASE}/skills?${params}`, {
        headers: getHeaders(),
      });
      const json = await res.json();
      return { data: json.data || [], total: json.meta?.total || 0 };
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
  } = useInfiniteScroll<Skill>({
    fetchFn: fetchSkills,
  });

  useEffect(() => {
    fetchLabels();
    fetchStats();
  }, [fetchLabels, fetchStats]);

  const handleToggle = async (id: string) => {
    await fetch(`${API_BASE}/skills/${id}/toggle`, {
      method: "POST",
      headers: getHeaders(),
    });
    fetchStats();
    refresh();
  };

  const handleSync = async () => {
    setIsSyncing(true);
    try {
      const response = await fetch(`${API_BASE}/skills/sync`, {
        method: "POST",
        headers: getHeaders(),
      });
      const json = await response.json();
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
    setFilterCategory("__all__");
    setFilterSource("__all__");
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-foreground">{t.skills}</h1>
        <Button onClick={handleSync} disabled={isSyncing}>
          {isSyncing ? t.loading : t.syncSkills}
        </Button>
      </div>

      {stats && (
        <div className="grid grid-cols-4 gap-4">
          <StatCard value={stats.total} label={t.totalSkills} />
          <StatCard value={stats.active} label={t.activeSkills} color="green" />
          <StatCard
            value={stats.inactive}
            label={t.inactiveSkills}
            color="muted"
          />
          <StatCard
            value={stats.categories.length}
            label={t.skillCategory}
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
          value={filterCategory}
          onChange={setFilterCategory}
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
          value={filterSource}
          onChange={setFilterSource}
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
        {(search ||
          filterCategory !== "__all__" ||
          filterSource !== "__all__") && (
          <Button variant="outline" size="sm" onClick={handleReset}>
            {t.reset}
          </Button>
        )}
      </div>

      {isLoading && skills.length === 0 ? (
        <div className="flex items-center justify-center h-64 text-muted-foreground">
          {t.loading}
        </div>
      ) : skills.length === 0 ? (
        <div className="text-center text-muted-foreground py-12">
          {t.noData}
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
            {skills.map((skill) => (
              <SkillCard
                key={skill.id}
                skill={skill}
                lang={lang}
                onClick={() => setSelectedSkill(skill)}
                onToggle={() => handleToggle(skill.id)}
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
            count={skills.length}
            lang={lang}
          />
        </>
      )}

      {selectedSkill && (
        <SkillDetailModal
          lang={lang}
          skill={selectedSkill}
          onClose={() => setSelectedSkill(null)}
          onToggle={() => {
            handleToggle(selectedSkill.id);
            setSelectedSkill(null);
          }}
          getCategoryLabel={getCategoryLabel}
          getSourceLabel={getSourceLabel}
        />
      )}
    </div>
  );
}

function SkillCard({
  skill,
  lang,
  onClick,
  onToggle,
  getCategoryLabel,
  getSourceLabel,
}: {
  skill: Skill;
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
        !skill.is_active ? "opacity-60" : ""
      }`}
      onClick={onClick}
    >
      <CardContent className="p-4">
        <div className="flex items-start justify-between mb-2">
          <h3 className="font-medium truncate flex-1 text-foreground">
            {skill.name}
          </h3>
          <Badge variant={getSourceVariant(skill.source)} className="ml-2">
            {getSourceLabel(skill.source)}
          </Badge>
        </div>
        <p className="text-sm text-muted-foreground line-clamp-2 mb-3">
          {skill.description}
        </p>
        <div className="flex items-center justify-between">
          <Badge variant="outline">{getCategoryLabel(skill.category)}</Badge>
          <Button
            variant="ghost"
            size="sm"
            onClick={(e) => {
              e.stopPropagation();
              onToggle();
            }}
          >
            <Badge variant={skill.is_active ? "default" : "secondary"}>
              {skill.is_active ? t.active : t.inactive}
            </Badge>
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}

function SkillDetailModal({
  lang,
  skill,
  onClose,
  onToggle,
  getCategoryLabel,
  getSourceLabel,
}: {
  lang: Language;
  skill: Skill;
  onClose: () => void;
  onToggle: () => void;
  getCategoryLabel: (code: string) => string;
  getSourceLabel: (code: string) => string;
}) {
  const t = adminLocales[lang];

  const handleExportMd = () => {
    // 构建 markdown 内容
    const lines: string[] = [];
    lines.push(`# ${skill.name}`);
    lines.push("");
    lines.push(`- **Category**: ${getCategoryLabel(skill.category)}`);
    lines.push(`- **Source**: ${getSourceLabel(skill.source)}`);
    if (skill.repo) {
      lines.push(`- **Repo**: ${skill.repo}`);
    }
    lines.push("");

    if (skill.description) {
      lines.push("## Description");
      lines.push("");
      lines.push(skill.description);
      lines.push("");
    }

    if (skill.content) {
      lines.push("## Content");
      lines.push("");
      lines.push(skill.content);
    }

    const mdContent = lines.join("\n");

    // 创建下载
    const blob = new Blob([mdContent], { type: "text/markdown;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${skill.name}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <Dialog open={true} onOpenChange={(o) => !o && onClose()}>
      <DialogContent className="max-w-2xl max-h-[80vh] overflow-hidden flex flex-col">
        <DialogHeader>
          <DialogTitle className="truncate">{skill.name}</DialogTitle>
          <div className="flex items-center gap-2 mt-2">
            <Badge variant={getSourceVariant(skill.source)}>
              {getSourceLabel(skill.source)}
            </Badge>
            <Badge variant="outline">{getCategoryLabel(skill.category)}</Badge>
          </div>
        </DialogHeader>

        <div className="flex-1 overflow-y-auto space-y-4">
          {skill.description && (
            <div>
              <h3 className="text-sm font-medium text-muted-foreground mb-2">
                {t.skillDescription}
              </h3>
              <p className="text-foreground">{skill.description}</p>
            </div>
          )}

          {skill.repo && (
            <div>
              <h3 className="text-sm font-medium text-muted-foreground mb-2">
                {t.skillRepo}
              </h3>
              <a
                href={skill.repo}
                target="_blank"
                rel="noopener noreferrer"
                className="text-primary hover:underline break-all"
              >
                {skill.repo}
              </a>
            </div>
          )}

          {skill.content && (
            <div>
              <h3 className="text-sm font-medium text-muted-foreground mb-2">
                {t.skillContent}
              </h3>
              <pre className="bg-muted rounded-lg p-4 text-sm text-foreground overflow-x-auto whitespace-pre-wrap">
                {skill.content}
              </pre>
            </div>
          )}
        </div>

        <DialogFooter className="flex justify-between sm:justify-between gap-2">
          <div className="flex gap-2">
            <Button
              variant={skill.is_active ? "outline" : "default"}
              onClick={onToggle}
            >
              {skill.is_active ? t.inactive : t.active}
            </Button>
            <Button variant="outline" onClick={handleExportMd}>
              {t.exportMd || "导出 MD"}
            </Button>
          </div>
          <Button variant="outline" onClick={onClose}>
            {t.close}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
