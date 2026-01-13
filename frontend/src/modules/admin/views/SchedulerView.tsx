import { useState, useEffect, useCallback } from "react";
import { adminLocales } from "@/common/i18n";
import type { Language } from "@/common/types";
import { AdminTagFilter } from "../components/AdminTagFilter";
import { Button } from "@/libs/shadcn/ui/button";
import { Badge } from "@/libs/shadcn/ui/badge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/libs/shadcn/ui/table";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/libs/shadcn/ui/dialog";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/libs/shadcn/ui/select";
import { Switch } from "@/libs/shadcn/ui/switch";
import { Textarea } from "@/libs/shadcn/ui/textarea";
import { Input } from "@/libs/shadcn/ui/input";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/libs/shadcn/ui/collapsible";
import { ChevronDown, ChevronRight } from "lucide-react";

// ============ Types ============
interface SchedulerViewProps {
  lang: Language;
}

interface ScheduledJob {
  id: string;
  name: string;
  description: string;
  job_type: string;
  cron_expression: string;
  parameters: Record<string, unknown>;
  is_active: boolean;
  last_run_at: string;
  next_run_at: string;
  last_status: string;
  created_at: string;
  updated_at: string;
}

interface JobType {
  type: string;
  name_zh: string;
  name_en: string;
  description_zh: string;
  description_en: string;
  parameters_schema: Record<string, unknown>;
}

interface JobExecution {
  id: string;
  job_id: string;
  started_at: string;
  finished_at: string;
  status: string;
  result: Record<string, unknown>;
  error_message: string;
  created_at: string;
}

// ============ Constants ============
const API_BASE = import.meta.env.VITE_API_URL || "/api";
const getHeaders = () => ({
  "Content-Type": "application/json",
  Authorization: `Bearer ${localStorage.getItem("admin_token") || ""}`,
});

// ============ Main Component ============
export default function SchedulerView({ lang }: SchedulerViewProps) {
  const t = adminLocales[lang];

  // UI State
  const [isLoading, setIsLoading] = useState(true);
  const [showJobModal, setShowJobModal] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [expandedJobId, setExpandedJobId] = useState<string | null>(null);
  const [isLoadingHistory, setIsLoadingHistory] = useState(false);

  // Data State
  const [jobs, setJobs] = useState<ScheduledJob[]>([]);
  const [jobTypes, setJobTypes] = useState<JobType[]>([]);
  const [selectedJob, setSelectedJob] = useState<ScheduledJob | null>(null);
  const [executionsMap, setExecutionsMap] = useState<
    Record<string, JobExecution[]>
  >({});

  // Form State
  const [formData, setFormData] = useState({
    name: "",
    description: "",
    job_type: "",
    cron_expression: "0 0 * * *",
    parameters: "{}",
    is_active: true,
  });

  // Filter State
  const [filterType, setFilterType] = useState("");

  // Collapsed groups
  const [collapsedGroups, setCollapsedGroups] = useState<Set<string>>(
    new Set()
  );

  // ============ Data Fetching ============
  const fetchJobs = useCallback(async () => {
    setIsLoading(true);
    try {
      const res = await fetch(`${API_BASE}/scheduler/jobs`, {
        headers: getHeaders(),
      });
      const json = await res.json();
      if (json.success) {
        setJobs(json.data || []);
      }
    } catch (err) {
      console.error("Failed to fetch jobs:", err);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const fetchJobTypes = useCallback(async () => {
    try {
      const res = await fetch(`${API_BASE}/scheduler/job-types`, {
        headers: getHeaders(),
      });
      const json = await res.json();
      if (json.success) {
        setJobTypes(json.data || []);
      }
    } catch (err) {
      console.error("Failed to fetch job types:", err);
    }
  }, []);

  const fetchHistory = useCallback(async (jobId: string) => {
    setIsLoadingHistory(true);
    try {
      const res = await fetch(`${API_BASE}/scheduler/jobs/${jobId}/history`, {
        headers: getHeaders(),
      });
      const json = await res.json();
      if (json.success) {
        setExecutionsMap((prev) => ({
          ...prev,
          [jobId]: json.data || [],
        }));
      }
    } catch (err) {
      console.error("Failed to fetch history:", err);
    } finally {
      setIsLoadingHistory(false);
    }
  }, []);

  useEffect(() => {
    fetchJobs();
    fetchJobTypes();
  }, [fetchJobs, fetchJobTypes]);

  // ============ Event Handlers ============
  const handleCreate = () => {
    setSelectedJob(null);
    setFormData({
      name: "",
      description: "",
      job_type: "",
      cron_expression: "0 0 * * *",
      parameters: "{}",
      is_active: true,
    });
    setShowJobModal(true);
  };

  const handleEdit = (job: ScheduledJob) => {
    setSelectedJob(job);
    setFormData({
      name: job.name,
      description: job.description || "",
      job_type: job.job_type,
      cron_expression: job.cron_expression,
      parameters: JSON.stringify(job.parameters || {}, null, 2),
      is_active: job.is_active,
    });
    setShowJobModal(true);
  };

  const handleSave = async () => {
    setIsSubmitting(true);
    try {
      let parsedParams = {};
      try {
        parsedParams = JSON.parse(formData.parameters);
      } catch {
        parsedParams = {};
      }

      const payload = {
        name: formData.name,
        description: formData.description,
        job_type: formData.job_type,
        cron_expression: formData.cron_expression,
        parameters: parsedParams,
        is_active: formData.is_active,
      };

      const url = selectedJob
        ? `${API_BASE}/scheduler/jobs/${selectedJob.id}`
        : `${API_BASE}/scheduler/jobs`;
      const method = selectedJob ? "PUT" : "POST";

      const res = await fetch(url, {
        method,
        headers: getHeaders(),
        body: JSON.stringify(payload),
      });
      const json = await res.json();
      if (json.success) {
        setShowJobModal(false);
        fetchJobs();
      }
    } catch (err) {
      console.error("Failed to save job:", err);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm(t.confirmDelete)) return;
    try {
      await fetch(`${API_BASE}/scheduler/jobs/${id}`, {
        method: "DELETE",
        headers: getHeaders(),
      });
      fetchJobs();
    } catch (err) {
      console.error("Failed to delete job:", err);
    }
  };

  const handleToggle = async (id: string) => {
    try {
      await fetch(`${API_BASE}/scheduler/jobs/${id}/toggle`, {
        method: "POST",
        headers: getHeaders(),
      });
      fetchJobs();
    } catch (err) {
      console.error("Failed to toggle job:", err);
    }
  };

  const handleTrigger = async (id: string) => {
    try {
      const res = await fetch(`${API_BASE}/scheduler/jobs/${id}/trigger`, {
        method: "POST",
        headers: getHeaders(),
      });
      const json = await res.json();
      if (json.success) {
        alert(t.triggerSuccess);
        fetchJobs();
      } else {
        alert(t.triggerFailed);
      }
    } catch (err) {
      console.error("Failed to trigger job:", err);
      alert(t.triggerFailed);
    }
  };

  const handleViewHistory = (job: ScheduledJob) => {
    if (expandedJobId === job.id) {
      setExpandedJobId(null);
    } else {
      setExpandedJobId(job.id);
      if (!executionsMap[job.id]) {
        fetchHistory(job.id);
      }
    }
  };

  // ============ Helper Functions ============
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

  const getStatusBadge = (status: string) => {
    if (status === "success") {
      return <Badge className="bg-green-500">{t.success}</Badge>;
    } else if (status === "failed") {
      return <Badge variant="destructive">{t.failed}</Badge>;
    } else if (status === "running") {
      return <Badge className="bg-blue-500">{t.running}</Badge>;
    }
    return <Badge variant="secondary">{status || "-"}</Badge>;
  };

  const formatDateTime = (dateStr: string) => {
    if (!dateStr) return "-";
    return new Date(dateStr).toLocaleString(lang === "zh" ? "zh-CN" : "en-US");
  };

  const renderResult = (result: Record<string, unknown>) => {
    if (!result || Object.keys(result).length === 0) return null;

    // 刷新数据源结�?(新格�?
    if ("total" in result && "updated" in result && "unchanged" in result) {
      const total = result.total as number;
      const updated = result.updated as number;
      const unchanged = result.unchanged as number;
      const errors = result.errors as
        | Array<{ url: string; error: string }>
        | undefined;
      const byCategory = result.by_category as
        | Array<{
            category: string;
            total: number;
            updated: number;
            unchanged: number;
            errors: number;
          }>
        | undefined;
      const changes = result.changes as
        | Array<{
            url: string;
            name: string;
            stars?: { old: number; new: number; diff: number };
            forks?: { old: number; new: number; diff: number };
          }>
        | undefined;

      return (
        <div className="space-y-3">
          {/* 总体统计 */}
          <div className="flex items-center gap-4 flex-wrap">
            <span className="text-muted-foreground">
              {t.resultTotal}: {total} {t.resultItems}
            </span>
            <span className="text-green-600 font-medium">
              �?{t.resultUpdated}: {updated}
            </span>
            <span className="text-muted-foreground">
              {t.resultUnchanged}: {unchanged}
            </span>
            {errors && errors.length > 0 && (
              <span className="text-red-600 font-medium">
                �?{t.resultErrors}: {errors.length}
              </span>
            )}
          </div>

          {/* 分类统计 */}
          {byCategory && byCategory.length > 0 && (
            <div className="text-xs space-y-1">
              <div className="font-medium text-muted-foreground">
                {t.resultByCategory}:
              </div>
              <div className="flex flex-wrap gap-2">
                {byCategory.map((cat, idx) => (
                  <Badge
                    key={idx}
                    variant={cat.updated > 0 ? "default" : "secondary"}
                    className="text-xs"
                  >
                    {cat.category}: {cat.updated}/{cat.total}
                  </Badge>
                ))}
              </div>
            </div>
          )}

          {/* 变化详情 */}
          {changes && changes.length > 0 && (
            <div className="text-xs space-y-1">
              <div className="font-medium text-muted-foreground">
                {t.resultChanges}:
              </div>
              {changes.slice(0, 5).map((change, idx) => (
                <div key={idx} className="flex gap-2 items-center">
                  <span className="text-green-500">�?/span>
                  <span className="truncate max-w-xs">{change.name}</span>
                  {change.stars && (
                    <span className="text-yellow-600">
                      �?{change.stars.old} �?{change.stars.new}
                      {change.stars.diff > 0 && (
                        <span className="text-green-500">
                          {" "}
                          (+{change.stars.diff})
                        </span>
                      )}
                    </span>
                  )}
                  {change.forks && (
                    <span className="text-blue-600">
                      🍴 {change.forks.old} �?{change.forks.new}
                    </span>
                  )}
                </div>
              ))}
              {changes.length > 5 && (
                <div className="text-muted-foreground">
                  ... +{changes.length - 5} more
                </div>
              )}
            </div>
          )}

          {/* 错误详情 */}
          {errors && errors.length > 0 && (
            <div className="text-xs text-muted-foreground space-y-1">
              <div className="font-medium text-red-600">{t.resultErrors}:</div>
              {errors.slice(0, 3).map((err, idx) => (
                <div key={idx} className="flex gap-2">
                  <span className="text-red-500">�?/span>
                  <span className="truncate max-w-md" title={err.url}>
                    {err.url}
                  </span>
                  <span className="text-red-500">({err.error})</span>
                </div>
              ))}
              {errors.length > 3 && (
                <div className="text-muted-foreground">
                  ... +{errors.length - 3} more
                </div>
              )}
            </div>
          )}
        </div>
      );
    }

    // 旧格式兼�?(refreshed)
    if ("refreshed" in result) {
      const refreshed = result.refreshed as number;
      const errors = result.errors as
        | Array<{ url: string; error: string }>
        | undefined;
      return (
        <div className="space-y-2">
          <div className="flex items-center gap-4">
            <span className="text-green-600 font-medium">
              �?{t.resultRefreshed}: {refreshed} {t.resultItems}
            </span>
            {errors && errors.length > 0 && (
              <span className="text-red-600 font-medium">
                �?{t.resultErrors}: {errors.length} {t.resultItems}
              </span>
            )}
          </div>
          {errors && errors.length > 0 && (
            <div className="text-xs text-muted-foreground space-y-1 mt-2">
              {errors.slice(0, 5).map((err, idx) => (
                <div key={idx} className="flex gap-2">
                  <span className="text-red-500">�?/span>
                  <span className="truncate max-w-md" title={err.url}>
                    {err.url}
                  </span>
                  <span className="text-red-500">({err.error})</span>
                </div>
              ))}
              {errors.length > 5 && (
                <div className="text-muted-foreground">
                  ... +{errors.length - 5} more
                </div>
              )}
            </div>
          )}
        </div>
      );
    }

    // 自动探索结果
    if ("domain" in result && "total" in result) {
      const total = result.total as number;
      const nameZh = result.name_zh as string;
      const nameEn = result.name_en as string;
      const keywords = result.keywords_used as string[] | undefined;
      const strategies = result.strategies_used as
        | Array<{ strategy: string; count: number }>
        | undefined;
      const results = result.results as
        | Array<{ url: string; name: string; stars: number }>
        | undefined;

      return (
        <div className="space-y-3">
          <div className="flex items-center gap-4 flex-wrap">
            <span className="font-medium">
              {t.resultDomain}: {lang === "zh" ? nameZh : nameEn}
            </span>
            <span
              className={
                total > 0
                  ? "text-green-600 font-medium"
                  : "text-muted-foreground"
              }
            >
              {t.resultDiscovered}: {total} {t.resultItems}
            </span>
          </div>

          {strategies && strategies.length > 0 && (
            <div className="flex items-center gap-2 flex-wrap text-sm">
              <span className="text-muted-foreground">
                {t.resultStrategies}:
              </span>
              {strategies.map((s, idx) => (
                <Badge
                  key={idx}
                  variant={s.count > 0 ? "default" : "secondary"}
                  className="text-xs"
                >
                  {s.strategy}: {s.count}
                </Badge>
              ))}
            </div>
          )}

          {keywords && keywords.length > 0 && (
            <div className="text-xs text-muted-foreground">
              <span>{t.resultKeywords}: </span>
              {keywords.join(", ")}
            </div>
          )}

          {results && results.length > 0 && (
            <div className="text-xs space-y-1 mt-2">
              <div className="font-medium">{t.resultDetails}:</div>
              {results.slice(0, 5).map((r, idx) => (
                <div key={idx} className="flex gap-2 items-center">
                  <span className="text-green-500">+</span>
                  <span className="truncate max-w-md">{r.name || r.url}</span>
                  <span className="text-muted-foreground">�?{r.stars}</span>
                </div>
              ))}
              {results.length > 5 && (
                <div className="text-muted-foreground">
                  ... +{results.length - 5} more
                </div>
              )}
            </div>
          )}
        </div>
      );
    }

    // 默认 JSON 显示
    return (
      <pre className="text-xs whitespace-pre-wrap break-all overflow-x-auto max-h-64 overflow-y-auto">
        {JSON.stringify(result, null, 2)}
      </pre>
    );
  };

  // ============ Filter counts ============
  const typeCounts = jobTypes
    .map((jt) => ({
      value: jt.type,
      label: lang === "zh" ? jt.name_zh : jt.name_en,
      count: jobs.filter((j) => j.job_type === jt.type).length,
    }))
    .filter((tc) => tc.count > 0);

  // Filter jobs
  const filteredJobs = filterType
    ? jobs.filter((j) => j.job_type === filterType)
    : jobs;

  // Group jobs by type
  const groupedJobs = jobTypes.reduce((acc, jt) => {
    const typeJobs = filteredJobs.filter((j) => j.job_type === jt.type);
    if (typeJobs.length > 0) {
      acc[jt.type] = typeJobs;
    }
    return acc;
  }, {} as Record<string, ScheduledJob[]>);

  const sortedGroupKeys = Object.keys(groupedJobs);

  // ============ Render ============
  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">{t.scheduler}</h2>
        <Button onClick={handleCreate}>{t.addJob}</Button>
      </div>

      {/* Type Filter */}
      {typeCounts.length > 0 && (
        <AdminTagFilter
          lang={lang}
          label={t.jobType}
          options={typeCounts}
          value={filterType || "__all__"}
          onChange={(v) => setFilterType(v === "__all__" ? "" : v)}
          color="violet"
        />
      )}

      {/* Jobs grouped by type */}
      {isLoading ? (
        <div className="text-center py-8 text-muted-foreground">
          {t.loading}
        </div>
      ) : filteredJobs.length === 0 ? (
        <div className="text-center py-8 text-muted-foreground">{t.noData}</div>
      ) : (
        <div className="space-y-4">
          {sortedGroupKeys.map((groupKey) => {
            const groupJobs = groupedJobs[groupKey];
            const jobType = jobTypes.find((jt) => jt.type === groupKey);
            const isCollapsed = collapsedGroups.has(groupKey);
            const groupLabel = jobType
              ? lang === "zh"
                ? jobType.name_zh
                : jobType.name_en
              : groupKey;

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
                        <Badge variant="secondary">{groupJobs.length}</Badge>
                      </div>
                      <div className="flex gap-4 text-xs text-muted-foreground">
                        <span>
                          {t.enabled}:{" "}
                          {groupJobs.filter((j) => j.is_active).length}
                        </span>
                      </div>
                    </div>
                  </CollapsibleTrigger>
                  <CollapsibleContent>
                    <Table>
                      <TableHeader>
                        <TableRow>
                          <TableHead>{t.jobName}</TableHead>
                          <TableHead>{t.cronExpression}</TableHead>
                          <TableHead>{t.status}</TableHead>
                          <TableHead>{t.lastRunAt}</TableHead>
                          <TableHead>{t.lastStatus}</TableHead>
                          <TableHead>{t.actions}</TableHead>
                        </TableRow>
                      </TableHeader>
                      <TableBody>
                        {groupJobs.map((job) => (
                          <>
                            <TableRow
                              key={job.id}
                              className={`cursor-pointer hover:bg-muted/30 ${
                                expandedJobId === job.id ? "bg-muted/50" : ""
                              }`}
                              onClick={() => handleViewHistory(job)}
                            >
                              <TableCell>
                                <div>
                                  <div className="font-medium">{job.name}</div>
                                  {job.description && (
                                    <div className="text-sm text-muted-foreground">
                                      {job.description}
                                    </div>
                                  )}
                                </div>
                              </TableCell>
                              <TableCell>
                                <code className="text-sm bg-muted px-2 py-1 rounded">
                                  {job.cron_expression}
                                </code>
                              </TableCell>
                              <TableCell>
                                <Badge
                                  variant={
                                    job.is_active ? "default" : "secondary"
                                  }
                                >
                                  {job.is_active ? t.enabled : t.disabled}
                                </Badge>
                              </TableCell>
                              <TableCell>
                                {formatDateTime(job.last_run_at)}
                              </TableCell>
                              <TableCell>
                                {getStatusBadge(job.last_status)}
                              </TableCell>
                              <TableCell onClick={(e) => e.stopPropagation()}>
                                <div className="flex gap-2">
                                  <Button
                                    size="sm"
                                    variant="outline"
                                    onClick={() => handleTrigger(job.id)}
                                  >
                                    {t.triggerNow}
                                  </Button>
                                  <Button
                                    size="sm"
                                    variant="outline"
                                    onClick={() => handleToggle(job.id)}
                                  >
                                    {job.is_active ? t.disable : t.enable}
                                  </Button>
                                  <Button
                                    size="sm"
                                    variant="outline"
                                    onClick={() => handleEdit(job)}
                                  >
                                    {t.edit}
                                  </Button>
                                  <Button
                                    size="sm"
                                    variant="destructive"
                                    onClick={() => handleDelete(job.id)}
                                  >
                                    {t.delete}
                                  </Button>
                                </div>
                              </TableCell>
                            </TableRow>
                            {/* Inline History */}
                            {expandedJobId === job.id && (
                              <TableRow key={`${job.id}-history`}>
                                <TableCell
                                  colSpan={6}
                                  className="bg-muted/30 p-4"
                                >
                                  <div className="space-y-3">
                                    <div className="font-medium text-sm">
                                      {t.jobHistory}
                                    </div>
                                    {isLoadingHistory &&
                                    !executionsMap[job.id] ? (
                                      <div className="text-center py-4 text-muted-foreground">
                                        {t.loading}
                                      </div>
                                    ) : !executionsMap[job.id] ||
                                      executionsMap[job.id].length === 0 ? (
                                      <div className="text-center py-4 text-muted-foreground">
                                        {t.noHistory}
                                      </div>
                                    ) : (
                                      <div className="space-y-3 max-h-[500px] overflow-y-auto">
                                        {executionsMap[job.id].map((exec) => (
                                          <div
                                            key={exec.id}
                                            className="border rounded-lg p-4 bg-background space-y-3"
                                          >
                                            <div className="flex items-center gap-4 flex-wrap">
                                              <div className="flex items-center gap-2">
                                                <span className="text-sm text-muted-foreground">
                                                  {t.startedAt}:
                                                </span>
                                                <span className="text-sm font-medium">
                                                  {formatDateTime(
                                                    exec.started_at
                                                  )}
                                                </span>
                                              </div>
                                              <div className="flex items-center gap-2">
                                                <span className="text-sm text-muted-foreground">
                                                  {t.finishedAt}:
                                                </span>
                                                <span className="text-sm font-medium">
                                                  {formatDateTime(
                                                    exec.finished_at
                                                  )}
                                                </span>
                                              </div>
                                              <div className="flex items-center gap-2">
                                                <span className="text-sm text-muted-foreground">
                                                  {t.status}:
                                                </span>
                                                {getStatusBadge(exec.status)}
                                              </div>
                                            </div>

                                            {exec.error_message && (
                                              <div className="bg-red-50 border border-red-200 rounded p-3">
                                                <div className="text-sm font-medium text-red-700 mb-1">
                                                  {t.errorMessage}
                                                </div>
                                                <pre className="text-xs text-red-600 whitespace-pre-wrap break-all">
                                                  {exec.error_message}
                                                </pre>
                                              </div>
                                            )}

                                            {exec.result && (
                                              <div className="bg-muted rounded p-3">
                                                <div className="text-sm font-medium mb-2">
                                                  {t.result}
                                                </div>
                                                {renderResult(exec.result)}
                                              </div>
                                            )}
                                          </div>
                                        ))}
                                      </div>
                                    )}
                                  </div>
                                </TableCell>
                              </TableRow>
                            )}
                          </>
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

      {/* Job Modal */}
      <Dialog open={showJobModal} onOpenChange={setShowJobModal}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>{selectedJob ? t.editJob : t.addJob}</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div>
              <label className="text-sm font-medium">{t.jobName}</label>
              <Input
                value={formData.name}
                onChange={(e) =>
                  setFormData({ ...formData, name: e.target.value })
                }
              />
            </div>
            <div>
              <label className="text-sm font-medium">{t.description}</label>
              <Input
                value={formData.description}
                onChange={(e) =>
                  setFormData({ ...formData, description: e.target.value })
                }
              />
            </div>
            <div>
              <label className="text-sm font-medium">{t.jobType}</label>
              <Select
                value={formData.job_type}
                onValueChange={(v) => setFormData({ ...formData, job_type: v })}
                disabled={!!selectedJob}
              >
                <SelectTrigger>
                  <SelectValue placeholder={t.jobType} />
                </SelectTrigger>
                <SelectContent>
                  {jobTypes.map((jt) => (
                    <SelectItem key={jt.type} value={jt.type}>
                      {lang === "zh" ? jt.name_zh : jt.name_en}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
            <div>
              <label className="text-sm font-medium">{t.cronExpression}</label>
              <Input
                value={formData.cron_expression}
                onChange={(e) =>
                  setFormData({ ...formData, cron_expression: e.target.value })
                }
                placeholder="0 0 * * *"
              />
              <p className="text-xs text-muted-foreground mt-1">{t.cronHelp}</p>
            </div>
            <div>
              <label className="text-sm font-medium">{t.parameters}</label>
              <Textarea
                value={formData.parameters}
                onChange={(e) =>
                  setFormData({ ...formData, parameters: e.target.value })
                }
                rows={4}
                placeholder="{}"
              />
            </div>
            <div className="flex items-center gap-2">
              <Switch
                checked={formData.is_active}
                onCheckedChange={(v) =>
                  setFormData({ ...formData, is_active: v })
                }
              />
              <label className="text-sm">{t.enabled}</label>
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowJobModal(false)}>
              {t.cancel}
            </Button>
            <Button onClick={handleSave} disabled={isSubmitting}>
              {isSubmitting ? t.loading : t.save}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
