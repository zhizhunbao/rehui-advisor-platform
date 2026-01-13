import { useState, useEffect, useCallback } from "react";
import { adminLocales, type Language } from "@/common/i18n";
import { getApiBase, getAuthHeaders } from "@/common/helper";
import { Button } from "@/libs/shadcn/ui/button";
import { Input } from "@/libs/shadcn/ui/input";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/libs/shadcn/ui/card";
import { Badge } from "@/libs/shadcn/ui/badge";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/libs/shadcn/ui/dialog";

interface AgentFramework {
  id: string;
  url: string;
  name: string;
  description: string;
  tags: string[];
  status: string;
  github_stars?: number;
  github_forks?: number;
  github_language?: string;
  last_synced_at?: string;
  created_at: string;
}

interface AgentFrameworksViewProps {
  lang: Language;
}

const API_BASE = getApiBase();
const getHeaders = getAuthHeaders;

export default function AgentFrameworksView({
  lang,
}: AgentFrameworksViewProps) {
  const t = adminLocales[lang];
  const [frameworks, setFrameworks] = useState<AgentFramework[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [selectedFramework, setSelectedFramework] =
    useState<AgentFramework | null>(null);
  const [showAddModal, setShowAddModal] = useState(false);

  const fetchFrameworks = useCallback(async () => {
    setIsLoading(true);
    try {
      // 获取 agent_framework domain 的数据源
      const res = await fetch(
        `${API_BASE}/data-sources?domain_code=agent_framework&limit=100`,
        { headers: getHeaders() }
      );
      const json = await res.json();
      if (json.success) {
        setFrameworks(json.data || []);
      }
    } catch (err) {
      console.error("Failed to fetch agent frameworks:", err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchFrameworks();
  }, [fetchFrameworks]);

  const handleRefresh = async (id: string) => {
    await fetch(`${API_BASE}/data-sources/${id}/refresh`, {
      method: "POST",
      headers: getHeaders(),
    });
    fetchFrameworks();
  };

  const handleDelete = async (id: string) => {
    if (!confirm(t.confirmDelete)) return;
    await fetch(`${API_BASE}/data-sources/${id}`, {
      method: "DELETE",
      headers: getHeaders(),
    });
    fetchFrameworks();
  };

  const filteredFrameworks = frameworks.filter(
    (f) =>
      f.name.toLowerCase().includes(search.toLowerCase()) ||
      f.description.toLowerCase().includes(search.toLowerCase())
  );

  const totalStars = frameworks.reduce(
    (sum, f) => sum + (f.github_stars || 0),
    0
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-foreground">
            {lang === "zh" ? "Agent 框架" : "Agent Frameworks"}
          </h1>
          <p className="text-muted-foreground mt-1">
            {lang === "zh"
              ? "管理 AI Agent 和多智能体框架资源"
              : "Manage AI Agent and Multi-Agent framework resources"}
          </p>
        </div>
        <Button onClick={() => setShowAddModal(true)}>
          {lang === "zh" ? "添加框架" : "Add Framework"}
        </Button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="text-2xl font-bold">{frameworks.length}</div>
            <div className="text-sm text-muted-foreground">
              {lang === "zh" ? "框架总数" : "Total Frameworks"}
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-yellow-500">
              {totalStars.toLocaleString()} ⭐
            </div>
            <div className="text-sm text-muted-foreground">
              {lang === "zh" ? "总 Stars" : "Total Stars"}
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-green-500">
              {frameworks.filter((f) => f.status === "active").length}
            </div>
            <div className="text-sm text-muted-foreground">
              {lang === "zh" ? "活跃项目" : "Active"}
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="p-4">
            <div className="text-2xl font-bold text-blue-500">
              {new Set(frameworks.flatMap((f) => f.tags || [])).size}
            </div>
            <div className="text-sm text-muted-foreground">
              {lang === "zh" ? "标签" : "Tags"}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Search */}
      <Card>
        <CardContent className="p-4">
          <Input
            type="text"
            placeholder={lang === "zh" ? "搜索框架..." : "Search frameworks..."}
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-64"
          />
        </CardContent>
      </Card>

      {/* Framework List */}
      {isLoading ? (
        <div className="flex items-center justify-center h-64 text-muted-foreground">
          {t.loading}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredFrameworks.map((framework) => (
            <FrameworkCard
              key={framework.id}
              framework={framework}
              onClick={() => setSelectedFramework(framework)}
              onRefresh={() => handleRefresh(framework.id)}
              onDelete={() => handleDelete(framework.id)}
            />
          ))}
        </div>
      )}

      {filteredFrameworks.length === 0 && !isLoading && (
        <div className="text-center text-muted-foreground py-12">
          {lang === "zh" ? "暂无数据" : "No data"}
        </div>
      )}

      {/* Detail Modal */}
      {selectedFramework && (
        <FrameworkDetailModal
          framework={selectedFramework}
          lang={lang}
          onClose={() => setSelectedFramework(null)}
          onRefresh={() => {
            handleRefresh(selectedFramework.id);
            setSelectedFramework(null);
          }}
        />
      )}

      {/* Add Modal */}
      {showAddModal && (
        <AddFrameworkModal
          lang={lang}
          onClose={() => setShowAddModal(false)}
          onSuccess={() => {
            setShowAddModal(false);
            fetchFrameworks();
          }}
        />
      )}
    </div>
  );
}

// ============ FrameworkCard ============
interface FrameworkCardProps {
  framework: AgentFramework;
  onClick: () => void;
  onRefresh: () => void;
  onDelete: () => void;
}

function FrameworkCard({
  framework,
  onClick,
  onRefresh,
  onDelete,
}: FrameworkCardProps) {
  const repoName = framework.url.split("/").slice(-2).join("/");

  return (
    <Card
      className="cursor-pointer hover:shadow-lg transition-shadow"
      onClick={onClick}
    >
      <CardHeader className="pb-2">
        <div className="flex items-start justify-between">
          <CardTitle className="text-lg">{framework.name}</CardTitle>
          <Badge
            variant={framework.status === "active" ? "default" : "secondary"}
          >
            {framework.status}
          </Badge>
        </div>
        <a
          href={framework.url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-sm text-muted-foreground hover:text-primary"
          onClick={(e) => e.stopPropagation()}
        >
          {repoName}
        </a>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-muted-foreground line-clamp-2 mb-3">
          {framework.description}
        </p>

        {/* GitHub Stats */}
        <div className="flex items-center gap-4 text-sm mb-3">
          {framework.github_stars !== undefined && (
            <span className="flex items-center gap-1">
              ⭐ {framework.github_stars.toLocaleString()}
            </span>
          )}
          {framework.github_forks !== undefined && (
            <span className="flex items-center gap-1">
              🍴 {framework.github_forks.toLocaleString()}
            </span>
          )}
          {framework.github_language && (
            <span className="text-muted-foreground">
              {framework.github_language}
            </span>
          )}
        </div>

        {/* Tags */}
        <div className="flex flex-wrap gap-1 mb-3">
          {(framework.tags || []).slice(0, 4).map((tag) => (
            <Badge key={tag} variant="outline" className="text-xs">
              {tag}
            </Badge>
          ))}
          {(framework.tags || []).length > 4 && (
            <Badge variant="outline" className="text-xs">
              +{framework.tags.length - 4}
            </Badge>
          )}
        </div>

        {/* Actions */}
        <div className="flex gap-2" onClick={(e) => e.stopPropagation()}>
          <Button size="sm" variant="outline" onClick={onRefresh}>
            🔄
          </Button>
          <Button size="sm" variant="destructive" onClick={onDelete}>
            🗑️
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}

// ============ FrameworkDetailModal ============
interface FrameworkDetailModalProps {
  framework: AgentFramework;
  lang: Language;
  onClose: () => void;
  onRefresh: () => void;
}

function FrameworkDetailModal({
  framework,
  lang,
  onClose,
  onRefresh,
}: FrameworkDetailModalProps) {
  return (
    <Dialog open onOpenChange={onClose}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>{framework.name}</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <div>
            <a
              href={framework.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary hover:underline"
            >
              {framework.url}
            </a>
          </div>

          <p className="text-muted-foreground">{framework.description}</p>

          <div className="grid grid-cols-3 gap-4">
            <div className="text-center p-4 bg-muted rounded-lg">
              <div className="text-2xl font-bold">
                {framework.github_stars?.toLocaleString() || "-"}
              </div>
              <div className="text-sm text-muted-foreground">Stars</div>
            </div>
            <div className="text-center p-4 bg-muted rounded-lg">
              <div className="text-2xl font-bold">
                {framework.github_forks?.toLocaleString() || "-"}
              </div>
              <div className="text-sm text-muted-foreground">Forks</div>
            </div>
            <div className="text-center p-4 bg-muted rounded-lg">
              <div className="text-2xl font-bold">
                {framework.github_language || "-"}
              </div>
              <div className="text-sm text-muted-foreground">Language</div>
            </div>
          </div>

          <div>
            <div className="text-sm font-medium mb-2">
              {lang === "zh" ? "标签" : "Tags"}
            </div>
            <div className="flex flex-wrap gap-2">
              {(framework.tags || []).map((tag) => (
                <Badge key={tag} variant="secondary">
                  {tag}
                </Badge>
              ))}
            </div>
          </div>

          <div className="text-sm text-muted-foreground">
            {lang === "zh" ? "最后同步" : "Last synced"}:{" "}
            {framework.last_synced_at
              ? new Date(framework.last_synced_at).toLocaleString()
              : "-"}
          </div>

          <div className="flex gap-2 justify-end">
            <Button variant="outline" onClick={onRefresh}>
              {lang === "zh" ? "刷新数据" : "Refresh"}
            </Button>
            <Button variant="outline" onClick={onClose}>
              {lang === "zh" ? "关闭" : "Close"}
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}

// ============ AddFrameworkModal ============
interface AddFrameworkModalProps {
  lang: Language;
  onClose: () => void;
  onSuccess: () => void;
}

function AddFrameworkModal({
  lang,
  onClose,
  onSuccess,
}: AddFrameworkModalProps) {
  const [url, setUrl] = useState("");
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [tags, setTags] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async () => {
    if (!url) return;
    setIsSubmitting(true);

    try {
      // 先获取 agent_framework domain ID
      const domainRes = await fetch(`${API_BASE}/data-sources/domains`, {
        headers: getHeaders(),
      });
      const domainJson = await domainRes.json();
      const agentDomain = domainJson.data?.find(
        (d: { code: string }) => d.code === "agent_framework"
      );

      if (!agentDomain) {
        alert(
          lang === "zh"
            ? "未找到 agent_framework 领域"
            : "agent_framework domain not found"
        );
        return;
      }

      // 获取 tech category ID
      const catRes = await fetch(`${API_BASE}/data-sources/categories`, {
        headers: getHeaders(),
      });
      const catJson = await catRes.json();
      const techCat = catJson.data?.find(
        (c: { code: string }) => c.code === "tech"
      );

      const res = await fetch(`${API_BASE}/data-sources`, {
        method: "POST",
        headers: {
          ...getHeaders(),
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          url,
          name: name || url.split("/").pop(),
          description,
          type: "github",
          category_id: techCat?.id,
          domain_id: agentDomain.id,
          tags: tags
            .split(",")
            .map((t) => t.trim())
            .filter(Boolean),
        }),
      });

      const json = await res.json();
      if (json.success) {
        onSuccess();
      } else {
        alert(json.message || "Failed to add");
      }
    } catch (err) {
      console.error(err);
      alert("Failed to add framework");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Dialog open onOpenChange={onClose}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>
            {lang === "zh" ? "添加 Agent 框架" : "Add Agent Framework"}
          </DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <div>
            <label className="text-sm font-medium">GitHub URL *</label>
            <Input
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://github.com/owner/repo"
            />
          </div>
          <div>
            <label className="text-sm font-medium">
              {lang === "zh" ? "名称" : "Name"}
            </label>
            <Input
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder={lang === "zh" ? "可选，默认使用仓库名" : "Optional"}
            />
          </div>
          <div>
            <label className="text-sm font-medium">
              {lang === "zh" ? "描述" : "Description"}
            </label>
            <Input
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder={lang === "zh" ? "框架描述" : "Framework description"}
            />
          </div>
          <div>
            <label className="text-sm font-medium">
              {lang === "zh" ? "标签 (逗号分隔)" : "Tags (comma separated)"}
            </label>
            <Input
              value={tags}
              onChange={(e) => setTags(e.target.value)}
              placeholder="agent, multi-agent, workflow"
            />
          </div>
          <div className="flex gap-2 justify-end">
            <Button variant="outline" onClick={onClose}>
              {lang === "zh" ? "取消" : "Cancel"}
            </Button>
            <Button onClick={handleSubmit} disabled={!url || isSubmitting}>
              {isSubmitting
                ? lang === "zh"
                  ? "添加中..."
                  : "Adding..."
                : lang === "zh"
                ? "添加"
                : "Add"}
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
