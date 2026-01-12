import { useState, useEffect, useCallback } from "react";
import { adminLocales, type Language } from "@/common/i18n";
import { StatCard } from "@/modules/admin/components/StatCard";
import { TagFilter } from "@/modules/admin/components/TagFilter";
import { getApiBase, getAuthHeaders } from "@/modules/admin/utils/api";
import { Button } from "@/libs/shadcn/ui/button";
import { Input } from "@/libs/shadcn/ui/input";
import { Textarea } from "@/libs/shadcn/ui/textarea";
import { Switch } from "@/libs/shadcn/ui/switch";
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

const API_BASE = getApiBase();
const getHeaders = getAuthHeaders;

// ========== Types ==========
interface RetrievalEngine {
  id: string;
  name: string;
  display_name: string;
  type: string;
  description: string;
  config: Record<string, unknown>;
  is_active: boolean;
  is_default: boolean;
  created_at: string;
  updated_at: string;
}

interface EngineType {
  type: string;
  name: string;
  description: string;
}

interface RetrievalViewProps {
  lang: Language;
}

// 引擎类型配置
const ENGINE_TYPE_CONFIG: Record<string, { icon: string; color: string }> = {
  keyword_match: { icon: "🔤", color: "slate" },
  structured_query: { icon: "📊", color: "blue" },
  rag_vector: { icon: "🧠", color: "violet" },
  page_index: { icon: "🌲", color: "emerald" },
  agent_tools: { icon: "🤖", color: "amber" },
  realtime_search: { icon: "🌐", color: "cyan" },
  hybrid: { icon: "⚡", color: "rose" },
};

const TYPE_COLORS: Record<string, string> = {
  keyword_match: "bg-slate-500/20 text-slate-600 dark:text-slate-400",
  structured_query: "bg-blue-500/20 text-blue-600 dark:text-blue-400",
  rag_vector: "bg-violet-500/20 text-violet-600 dark:text-violet-400",
  page_index: "bg-emerald-500/20 text-emerald-600 dark:text-emerald-400",
  agent_tools: "bg-amber-500/20 text-amber-600 dark:text-amber-400",
  realtime_search: "bg-cyan-500/20 text-cyan-600 dark:text-cyan-400",
  hybrid: "bg-rose-500/20 text-rose-600 dark:text-rose-400",
};

const defaultEngineForm = {
  name: "",
  display_name: "",
  type: "structured_query",
  description: "",
  config: {},
  is_active: true,
};

export default function RetrievalView({ lang }: RetrievalViewProps) {
  const t = adminLocales[lang];

  // ========== State ==========
  const [engines, setEngines] = useState<RetrievalEngine[]>([]);
  const [engineTypes, setEngineTypes] = useState<EngineType[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Filters
  const [filterType, setFilterType] = useState("");
  const [filterStatus, setFilterStatus] = useState("");

  // Engine Dialog
  const [showEngineDialog, setShowEngineDialog] = useState(false);
  const [editingEngine, setEditingEngine] = useState<RetrievalEngine | null>(
    null
  );
  const [engineForm, setEngineForm] = useState(defaultEngineForm);
  const [configJson, setConfigJson] = useState("{}");

  // Delete
  const [deleteTarget, setDeleteTarget] = useState<{
    id: string;
    name: string;
  } | null>(null);

  // Test
  const [showTestDialog, setShowTestDialog] = useState(false);
  const [testEngineId, setTestEngineId] = useState("");
  const [testQuery, setTestQuery] = useState("");
  const [testResult, setTestResult] = useState<Record<string, unknown> | null>(
    null
  );
  const [isTesting, setIsTesting] = useState(false);

  // ========== Fetch ==========
  const fetchEngines = useCallback(async () => {
    setIsLoading(true);
    try {
      const res = await fetch(`${API_BASE}/retrieval/engines?limit=100`, {
        headers: getHeaders(),
      });
      const json = await res.json();
      if (json.success) setEngines(json.data);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const fetchEngineTypes = useCallback(async () => {
    try {
      const res = await fetch(`${API_BASE}/retrieval/types`, {
        headers: getHeaders(),
      });
      const json = await res.json();
      if (json.success) setEngineTypes(json.data);
    } catch {
      // ignore
    }
  }, []);

  useEffect(() => {
    fetchEngines();
    fetchEngineTypes();
  }, [fetchEngines, fetchEngineTypes]);

  // ========== Filtered Engines ==========
  const filteredEngines = engines.filter((e) => {
    if (filterType && e.type !== filterType) return false;
    if (filterStatus === "active" && !e.is_active) return false;
    if (filterStatus === "inactive" && e.is_active) return false;
    return true;
  });

  // ========== Filter Options ==========
  const typeCounts = Object.keys(ENGINE_TYPE_CONFIG)
    .map((type) => ({
      value: type,
      label: `${ENGINE_TYPE_CONFIG[type].icon} ${type}`,
      count: engines.filter((e) => e.type === type).length,
    }))
    .filter((t) => t.count > 0);

  const statusCounts = [
    {
      value: "active",
      label: lang === "zh" ? "启用" : "Active",
      count: engines.filter((e) => e.is_active).length,
    },
    {
      value: "inactive",
      label: lang === "zh" ? "禁用" : "Inactive",
      count: engines.filter((e) => !e.is_active).length,
    },
  ].filter((s) => s.count > 0);

  // ========== Handlers ==========
  const handleCreateEngine = () => {
    setEditingEngine(null);
    setEngineForm(defaultEngineForm);
    setConfigJson("{}");
    setShowEngineDialog(true);
  };

  const handleEditEngine = (engine: RetrievalEngine) => {
    setEditingEngine(engine);
    setEngineForm({
      name: engine.name,
      display_name: engine.display_name,
      type: engine.type,
      description: engine.description,
      config: engine.config,
      is_active: engine.is_active,
    });
    setConfigJson(JSON.stringify(engine.config, null, 2));
    setShowEngineDialog(true);
  };

  const handleSaveEngine = async () => {
    let config = {};
    try {
      config = JSON.parse(configJson);
    } catch {
      alert(lang === "zh" ? "配置 JSON 格式错误" : "Invalid config JSON");
      return;
    }

    const payload = { ...engineForm, config };
    const url = editingEngine
      ? `${API_BASE}/retrieval/engines/${editingEngine.id}`
      : `${API_BASE}/retrieval/engines`;
    const method = editingEngine ? "PUT" : "POST";

    const res = await fetch(url, {
      method,
      headers: { ...getHeaders(), "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (res.ok) {
      setShowEngineDialog(false);
      fetchEngines();
    }
  };

  const handleDeleteEngine = async () => {
    if (!deleteTarget) return;
    await fetch(`${API_BASE}/retrieval/engines/${deleteTarget.id}`, {
      method: "DELETE",
      headers: getHeaders(),
    });
    setDeleteTarget(null);
    fetchEngines();
  };

  const handleSetDefault = async (engineId: string) => {
    await fetch(`${API_BASE}/retrieval/engines/default`, {
      method: "POST",
      headers: { ...getHeaders(), "Content-Type": "application/json" },
      body: JSON.stringify({ engine_id: engineId }),
    });
    fetchEngines();
  };

  const handleTest = async () => {
    if (!testEngineId || !testQuery) return;
    setIsTesting(true);
    setTestResult(null);
    try {
      const res = await fetch(`${API_BASE}/retrieval/test`, {
        method: "POST",
        headers: { ...getHeaders(), "Content-Type": "application/json" },
        body: JSON.stringify({
          engine_id: testEngineId,
          query: testQuery,
          context: {},
        }),
      });
      const json = await res.json();
      setTestResult(json.data);
    } finally {
      setIsTesting(false);
    }
  };

  // ========== Stats ==========
  const activeEngines = engines.filter((e) => e.is_active).length;
  const defaultEngine = engines.find((e) => e.is_default);

  // ========== Render ==========
  return (
    <div className="space-y-6">
      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        <StatCard
          label={lang === "zh" ? "引擎总数" : "Total"}
          value={engines.length}
        />
        <StatCard
          label={lang === "zh" ? "已启用" : "Active"}
          value={activeEngines}
          color="green"
        />
        <StatCard
          label={lang === "zh" ? "默认引擎" : "Default"}
          value={defaultEngine?.display_name || "-"}
          color="violet"
        />
      </div>

      {/* Actions */}
      <div className="flex justify-end gap-2">
        <Button variant="outline" onClick={() => setShowTestDialog(true)}>
          {lang === "zh" ? "🧪 测试" : "🧪 Test"}
        </Button>
        <Button onClick={handleCreateEngine}>
          {lang === "zh" ? "+ 添加引擎" : "+ Add Engine"}
        </Button>
      </div>

      {/* Filters */}
      <div className="space-y-2">
        {typeCounts.length > 0 && (
          <TagFilter
            lang={lang}
            label={lang === "zh" ? "类型" : "Type"}
            options={typeCounts}
            value={filterType || "__all__"}
            onChange={(v) => setFilterType(v === "__all__" ? "" : v)}
            color="violet"
          />
        )}
        {statusCounts.length > 1 && (
          <TagFilter
            lang={lang}
            label={lang === "zh" ? "状态" : "Status"}
            options={statusCounts}
            value={filterStatus || "__all__"}
            onChange={(v) => setFilterStatus(v === "__all__" ? "" : v)}
            color="emerald"
          />
        )}
        {(filterType || filterStatus) && (
          <Button
            variant="outline"
            size="sm"
            onClick={() => {
              setFilterType("");
              setFilterStatus("");
            }}
          >
            {lang === "zh" ? "重置筛选" : "Reset"}
          </Button>
        )}
      </div>

      {/* Engine Cards */}
      {isLoading ? (
        <div className="text-center py-8 text-slate-500">{t.loading}</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredEngines.map((engine) => {
            const typeConfig = ENGINE_TYPE_CONFIG[engine.type] || {
              icon: "📦",
              color: "slate",
            };
            return (
              <div
                key={engine.id}
                className={`bg-white dark:bg-admin-card-dark rounded-xl border border-admin-border-light dark:border-admin-border-dark hover:border-violet-500/50 transition-all ${
                  !engine.is_active ? "opacity-60" : ""
                }`}
              >
                <div className="p-4">
                  {/* Header */}
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex items-center gap-2">
                      <span className="text-2xl">{typeConfig.icon}</span>
                      <div>
                        <h3 className="font-medium text-lg text-slate-900 dark:text-white flex items-center gap-2">
                          {engine.display_name}
                          {engine.is_default && (
                            <span className="text-xs px-2 py-0.5 bg-violet-500/20 text-violet-600 dark:text-violet-400 rounded-full">
                              {lang === "zh" ? "默认" : "Default"}
                            </span>
                          )}
                        </h3>
                        <div className="text-xs text-slate-500 dark:text-slate-400 font-mono">
                          {engine.name}
                        </div>
                      </div>
                    </div>
                    <span
                      className={`text-xs px-2 py-1 rounded-full ${
                        engine.is_active
                          ? "bg-green-500/20 text-green-600 dark:text-green-400"
                          : "bg-slate-500/20 text-slate-600 dark:text-slate-400"
                      }`}
                    >
                      {engine.is_active
                        ? lang === "zh"
                          ? "启用"
                          : "Active"
                        : lang === "zh"
                        ? "禁用"
                        : "Off"}
                    </span>
                  </div>

                  {/* Description */}
                  {engine.description && (
                    <p className="text-sm text-slate-600 dark:text-slate-400 mb-3 line-clamp-2">
                      {engine.description}
                    </p>
                  )}

                  {/* Type Badge */}
                  <div className="flex flex-wrap gap-1 mb-3">
                    <span
                      className={`text-xs px-2 py-1 rounded-full ${
                        TYPE_COLORS[engine.type] || "bg-slate-500/20"
                      }`}
                    >
                      {engine.type}
                    </span>
                  </div>

                  {/* Actions */}
                  <div className="flex items-center justify-end gap-2 pt-3 border-t border-admin-border-light dark:border-admin-border-dark">
                    <button
                      onClick={() => handleEditEngine(engine)}
                      className="text-slate-500 hover:text-slate-700 dark:hover:text-slate-300"
                      title={t.edit}
                    >
                      ✏️
                    </button>
                    {!engine.is_default && engine.is_active && (
                      <button
                        onClick={() => handleSetDefault(engine.id)}
                        className="text-slate-500 hover:text-violet-500"
                        title={lang === "zh" ? "设为默认" : "Set Default"}
                      >
                        ⭐
                      </button>
                    )}
                    {!engine.is_default && (
                      <button
                        onClick={() =>
                          setDeleteTarget({
                            id: engine.id,
                            name: engine.display_name,
                          })
                        }
                        className="text-rose-500 hover:text-rose-400"
                        title={t.delete}
                      >
                        🗑️
                      </button>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Engine Dialog */}
      <Dialog open={showEngineDialog} onOpenChange={setShowEngineDialog}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>
              {editingEngine
                ? lang === "zh"
                  ? "编辑引擎"
                  : "Edit Engine"
                : lang === "zh"
                ? "添加引擎"
                : "Add Engine"}
            </DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">
                  {lang === "zh" ? "引擎标识" : "Name"}
                </label>
                <Input
                  value={engineForm.name}
                  onChange={(e) =>
                    setEngineForm({ ...engineForm, name: e.target.value })
                  }
                  placeholder="my_engine"
                  disabled={!!editingEngine}
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">
                  {lang === "zh" ? "显示名称" : "Display Name"}
                </label>
                <Input
                  value={engineForm.display_name}
                  onChange={(e) =>
                    setEngineForm({
                      ...engineForm,
                      display_name: e.target.value,
                    })
                  }
                  placeholder="My Engine"
                />
              </div>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">
                {lang === "zh" ? "引擎类型" : "Type"}
              </label>
              <Select
                value={engineForm.type}
                onValueChange={(v) => setEngineForm({ ...engineForm, type: v })}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {engineTypes.map((type) => (
                    <SelectItem key={type.type} value={type.type}>
                      {ENGINE_TYPE_CONFIG[type.type]?.icon || "📦"} {type.name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">
                {lang === "zh" ? "描述" : "Description"}
              </label>
              <Textarea
                value={engineForm.description}
                onChange={(e) =>
                  setEngineForm({ ...engineForm, description: e.target.value })
                }
                rows={2}
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">
                {lang === "zh" ? "配置 (JSON)" : "Config (JSON)"}
              </label>
              <Textarea
                value={configJson}
                onChange={(e) => setConfigJson(e.target.value)}
                rows={6}
                className="font-mono text-sm"
              />
            </div>
            <div className="flex items-center gap-2">
              <Switch
                checked={engineForm.is_active}
                onCheckedChange={(checked) =>
                  setEngineForm({ ...engineForm, is_active: checked })
                }
              />
              <label className="text-sm">
                {lang === "zh" ? "启用" : "Active"}
              </label>
            </div>
          </div>
          <DialogFooter>
            <Button
              variant="outline"
              onClick={() => setShowEngineDialog(false)}
            >
              {t.cancel}
            </Button>
            <Button onClick={handleSaveEngine}>{t.save}</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Test Dialog */}
      <Dialog open={showTestDialog} onOpenChange={setShowTestDialog}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>
              {lang === "zh" ? "测试引擎" : "Test Engine"}
            </DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">
                {lang === "zh" ? "选择引擎" : "Engine"}
              </label>
              <Select value={testEngineId} onValueChange={setTestEngineId}>
                <SelectTrigger>
                  <SelectValue
                    placeholder={lang === "zh" ? "选择" : "Select"}
                  />
                </SelectTrigger>
                <SelectContent>
                  {engines
                    .filter((e) => e.is_active)
                    .map((e) => (
                      <SelectItem key={e.id} value={e.id}>
                        {ENGINE_TYPE_CONFIG[e.type]?.icon} {e.display_name}
                      </SelectItem>
                    ))}
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">
                {lang === "zh" ? "测试查询" : "Query"}
              </label>
              <Textarea
                value={testQuery}
                onChange={(e) => setTestQuery(e.target.value)}
                placeholder={
                  lang === "zh" ? "输入测试问题..." : "Enter query..."
                }
                rows={3}
              />
            </div>
            <Button
              onClick={handleTest}
              disabled={isTesting || !testEngineId || !testQuery}
            >
              {isTesting
                ? lang === "zh"
                  ? "测试中..."
                  : "Testing..."
                : lang === "zh"
                ? "执行测试"
                : "Run"}
            </Button>
            {testResult && (
              <div className="space-y-2">
                <label className="text-sm font-medium">
                  {lang === "zh" ? "结果" : "Result"}
                </label>
                <pre className="p-4 bg-slate-100 dark:bg-slate-800 rounded-lg text-xs overflow-auto max-h-64">
                  {JSON.stringify(testResult, null, 2)}
                </pre>
              </div>
            )}
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowTestDialog(false)}>
              {t.close}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* Delete Confirm */}
      <AlertDialog
        open={!!deleteTarget}
        onOpenChange={() => setDeleteTarget(null)}
      >
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>{t.confirmDelete}</AlertDialogTitle>
            <AlertDialogDescription>
              {lang === "zh"
                ? `确定要删除引擎 "${deleteTarget?.name}" 吗？`
                : `Delete engine "${deleteTarget?.name}"?`}
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>{t.cancel}</AlertDialogCancel>
            <AlertDialogAction onClick={handleDeleteEngine}>
              {t.delete}
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
}
