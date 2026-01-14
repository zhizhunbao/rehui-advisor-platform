// Admin 调度任务筛选组件
import type { JobType, ScheduledJob } from "@/common/types";
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import { AdminTagFilter } from "./AdminTagFilter";

interface AdminSchedulerFilterProps {
  jobs: ScheduledJob[];
  jobTypes: JobType[];
  filterType: string;
  onFilterTypeChange: (type: string) => void;
}

export function AdminSchedulerFilter({
  jobs,
  jobTypes,
  filterType,
  onFilterTypeChange,
}: AdminSchedulerFilterProps) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  const typeCounts = jobTypes
    .map((jt) => ({
      value: jt.type,
      label: lang === "zh" ? jt.nameZh : jt.nameEn,
      count: jobs.filter((j) => j.jobType === jt.type).length,
    }))
    .filter((tc) => tc.count > 0);

  if (typeCounts.length === 0) return null;

  return (
    <AdminTagFilter
      label={t.jobType}
      options={typeCounts}
      value={filterType || "__all__"}
      onChange={(v) => onFilterTypeChange(v === "__all__" ? "" : v)}
      color="violet"
    />
  );
}
