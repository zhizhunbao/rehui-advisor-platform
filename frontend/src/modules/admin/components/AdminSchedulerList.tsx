// Admin 调度任务列表组件
import type { ScheduledJob, JobType, JobExecution } from "@/common/types";
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import { formatDateTime } from "@/common/helper";
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
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/libs/shadcn/ui/collapsible";
import { ChevronDown, ChevronRight } from "lucide-react";

interface AdminSchedulerListProps {
  jobs: ScheduledJob[];
  jobTypes: JobType[];
  isLoading: boolean;
  expandedJobId: string | null;
  executionsMap: Record<string, JobExecution[]>;
  isLoadingHistory: boolean;
  collapsedGroups: Set<string>;
  onViewHistory: (job: ScheduledJob) => void;
  onToggle: (id: string) => void;
  onTrigger: (id: string) => void;
  onEdit: (job: ScheduledJob) => void;
  onDelete: (id: string) => void;
  onToggleGroup: (group: string) => void;
}

export function AdminSchedulerList({
  jobs,
  jobTypes,
  isLoading,
  expandedJobId,
  executionsMap,
  isLoadingHistory,
  collapsedGroups,
  onViewHistory,
  onToggle,
  onTrigger,
  onEdit,
  onDelete,
  onToggleGroup,
}: AdminSchedulerListProps) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  if (isLoading) {
    return (
      <div className="text-center py-8 text-muted-foreground">{t.loading}</div>
    );
  }

  if (jobs.length === 0) {
    return (
      <div className="text-center py-8 text-muted-foreground">{t.noData}</div>
    );
  }

  const groupedJobs = jobTypes.reduce((acc, jt) => {
    const typeJobs = jobs.filter((j) => j.jobType === jt.type);
    if (typeJobs.length > 0) acc[jt.type] = typeJobs;
    return acc;
  }, {} as Record<string, ScheduledJob[]>);

  const getStatusBadge = (status: string) => {
    if (status === "success")
      return <Badge className="bg-green-500">{t.success}</Badge>;
    if (status === "failed")
      return <Badge variant="destructive">{t.failed}</Badge>;
    if (status === "running")
      return <Badge className="bg-blue-500">{t.running}</Badge>;
    return <Badge variant="secondary">{status || "-"}</Badge>;
  };

  return (
    <div className="space-y-4">
      {Object.keys(groupedJobs).map((groupKey) => {
        const groupJobs = groupedJobs[groupKey];
        const jobType = jobTypes.find((jt) => jt.type === groupKey);
        const isCollapsed = collapsedGroups.has(groupKey);
        const groupLabel = jobType
          ? lang === "zh"
            ? jobType.nameZh
            : jobType.nameEn
          : groupKey;

        return (
          <Collapsible
            key={groupKey}
            open={!isCollapsed}
            onOpenChange={() => onToggleGroup(groupKey)}
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
                      {t.enabled}: {groupJobs.filter((j) => j.isActive).length}
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
                      <JobRow
                        key={job.id}
                        job={job}
                        isExpanded={expandedJobId === job.id}
                        executions={executionsMap[job.id]}
                        isLoadingHistory={isLoadingHistory}
                        onViewHistory={() => onViewHistory(job)}
                        onToggle={() => onToggle(job.id)}
                        onTrigger={() => onTrigger(job.id)}
                        onEdit={() => onEdit(job)}
                        onDelete={() => onDelete(job.id)}
                        getStatusBadge={getStatusBadge}
                      />
                    ))}
                  </TableBody>
                </Table>
              </CollapsibleContent>
            </div>
          </Collapsible>
        );
      })}
    </div>
  );
}

interface JobRowProps {
  job: ScheduledJob;
  isExpanded: boolean;
  executions?: JobExecution[];
  isLoadingHistory: boolean;
  onViewHistory: () => void;
  onToggle: () => void;
  onTrigger: () => void;
  onEdit: () => void;
  onDelete: () => void;
  getStatusBadge: (status: string) => React.ReactNode;
}

function JobRow({
  job,
  isExpanded,
  executions,
  isLoadingHistory,
  onViewHistory,
  onToggle,
  onTrigger,
  onEdit,
  onDelete,
  getStatusBadge,
}: JobRowProps) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  return (
    <>
      <TableRow
        className={`cursor-pointer hover:bg-muted/30 ${
          isExpanded ? "bg-muted/50" : ""
        }`}
        onClick={onViewHistory}
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
            {job.cronExpression}
          </code>
        </TableCell>
        <TableCell>
          <Badge variant={job.isActive ? "default" : "secondary"}>
            {job.isActive ? t.enabled : t.disabled}
          </Badge>
        </TableCell>
        <TableCell>{formatDateTime(job.lastRunAt)}</TableCell>
        <TableCell>{getStatusBadge(job.lastStatus)}</TableCell>
        <TableCell onClick={(e) => e.stopPropagation()}>
          <div className="flex gap-2">
            <Button size="sm" variant="outline" onClick={onTrigger}>
              {t.triggerNow}
            </Button>
            <Button size="sm" variant="outline" onClick={onToggle}>
              {job.isActive ? t.disable : t.enable}
            </Button>
            <Button size="sm" variant="outline" onClick={onEdit}>
              {t.edit}
            </Button>
            <Button size="sm" variant="destructive" onClick={onDelete}>
              {t.delete}
            </Button>
          </div>
        </TableCell>
      </TableRow>
      {isExpanded && (
        <TableRow>
          <TableCell colSpan={6} className="bg-muted/30 p-4">
            <JobHistory
              executions={executions}
              isLoading={isLoadingHistory}
              getStatusBadge={getStatusBadge}
            />
          </TableCell>
        </TableRow>
      )}
    </>
  );
}

interface JobHistoryProps {
  executions?: JobExecution[];
  isLoading: boolean;
  getStatusBadge: (status: string) => React.ReactNode;
}

function JobHistory({
  executions,
  isLoading,
  getStatusBadge,
}: JobHistoryProps) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  if (isLoading && !executions) {
    return (
      <div className="text-center py-4 text-muted-foreground">{t.loading}</div>
    );
  }

  if (!executions || executions.length === 0) {
    return (
      <div className="text-center py-4 text-muted-foreground">
        {t.noHistory}
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <div className="font-medium text-sm">{t.jobHistory}</div>
      <div className="space-y-3 max-h-[500px] overflow-y-auto">
        {executions.map((exec) => (
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
                  {formatDateTime(exec.startedAt)}
                </span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-sm text-muted-foreground">
                  {t.finishedAt}:
                </span>
                <span className="text-sm font-medium">
                  {formatDateTime(exec.finishedAt)}
                </span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-sm text-muted-foreground">
                  {t.status}:
                </span>
                {getStatusBadge(exec.status)}
              </div>
            </div>
            {exec.errorMessage && (
              <div className="bg-red-50 border border-red-200 rounded p-3">
                <div className="text-sm font-medium text-red-700 mb-1">
                  {t.errorMessage}
                </div>
                <pre className="text-xs text-red-600 whitespace-pre-wrap break-all">
                  {exec.errorMessage}
                </pre>
              </div>
            )}
            {exec.result && Object.keys(exec.result).length > 0 && (
              <div className="bg-muted rounded p-3">
                <div className="text-sm font-medium mb-2">{t.result}</div>
                <pre className="text-xs whitespace-pre-wrap break-all">
                  {JSON.stringify(exec.result, null, 2)}
                </pre>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
