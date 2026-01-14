// Admin 调度任务管理 Hook
import { useState, useEffect, useCallback } from "react";
import type {
  ScheduledJob,
  JobType,
  JobExecution,
  ScheduledJobCreate,
} from "@/common/types";
import { schedulerService } from "../services/scheduler.service";

export function useScheduler() {
  const [jobs, setJobs] = useState<ScheduledJob[]>([]);
  const [jobTypes, setJobTypes] = useState<JobType[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [executionsMap, setExecutionsMap] = useState<
    Record<string, JobExecution[]>
  >({});
  const [isLoadingHistory, setIsLoadingHistory] = useState(false);

  const [showJobModal, setShowJobModal] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [selectedJob, setSelectedJob] = useState<ScheduledJob | null>(null);
  const [expandedJobId, setExpandedJobId] = useState<string | null>(null);
  const [filterType, setFilterType] = useState("");
  const [collapsedGroups, setCollapsedGroups] = useState<Set<string>>(
    new Set()
  );

  const [formData, setFormData] = useState<ScheduledJobCreate>(
    getDefaultForm()
  );

  const fetchJobs = useCallback(async () => {
    setIsLoading(true);
    try {
      const data = await schedulerService.getJobs();
      setJobs(data);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const fetchJobTypes = useCallback(async () => {
    const data = await schedulerService.getJobTypes();
    setJobTypes(data);
  }, []);

  const fetchHistory = useCallback(async (jobId: string) => {
    setIsLoadingHistory(true);
    try {
      const data = await schedulerService.getHistory(jobId);
      setExecutionsMap((prev) => ({ ...prev, [jobId]: data }));
    } finally {
      setIsLoadingHistory(false);
    }
  }, []);

  useEffect(() => {
    fetchJobs();
    fetchJobTypes();
  }, [fetchJobs, fetchJobTypes]);

  const handleCreate = useCallback(() => {
    setSelectedJob(null);
    setFormData(getDefaultForm());
    setShowJobModal(true);
  }, []);

  const handleEdit = useCallback((job: ScheduledJob) => {
    setSelectedJob(job);
    setFormData({
      name: job.name,
      description: job.description || "",
      jobType: job.jobType,
      cronExpression: job.cronExpression,
      parameters: job.parameters || {},
      isActive: job.isActive,
    });
    setShowJobModal(true);
  }, []);

  const handleSave = useCallback(async () => {
    setIsSubmitting(true);
    try {
      if (selectedJob) {
        await schedulerService.update(selectedJob.id, formData);
      } else {
        await schedulerService.create(formData);
      }
      setShowJobModal(false);
      fetchJobs();
    } finally {
      setIsSubmitting(false);
    }
  }, [selectedJob, formData, fetchJobs]);

  const handleDelete = useCallback(
    async (id: string) => {
      await schedulerService.delete(id);
      fetchJobs();
    },
    [fetchJobs]
  );

  const handleToggle = useCallback(
    async (id: string) => {
      await schedulerService.toggle(id);
      fetchJobs();
    },
    [fetchJobs]
  );

  const handleTrigger = useCallback(
    async (id: string) => {
      const success = await schedulerService.trigger(id);
      fetchJobs();
      return success;
    },
    [fetchJobs]
  );

  const handleViewHistory = useCallback(
    (job: ScheduledJob) => {
      if (expandedJobId === job.id) {
        setExpandedJobId(null);
      } else {
        setExpandedJobId(job.id);
        if (!executionsMap[job.id]) {
          fetchHistory(job.id);
        }
      }
    },
    [expandedJobId, executionsMap, fetchHistory]
  );

  const toggleGroup = useCallback((group: string) => {
    setCollapsedGroups((prev) => {
      const next = new Set(prev);
      if (next.has(group)) next.delete(group);
      else next.add(group);
      return next;
    });
  }, []);

  const handleCloseModal = useCallback(() => {
    setShowJobModal(false);
  }, []);

  const filteredJobs = filterType
    ? jobs.filter((j) => j.jobType === filterType)
    : jobs;

  return {
    jobs: filteredJobs,
    jobTypes,
    isLoading,
    executionsMap,
    isLoadingHistory,
    showJobModal,
    isSubmitting,
    selectedJob,
    expandedJobId,
    filterType,
    setFilterType,
    collapsedGroups,
    formData,
    setFormData,
    handleCreate,
    handleEdit,
    handleSave,
    handleDelete,
    handleToggle,
    handleTrigger,
    handleViewHistory,
    toggleGroup,
    handleCloseModal,
  };
}

function getDefaultForm(): ScheduledJobCreate {
  return {
    name: "",
    description: "",
    jobType: "",
    cronExpression: "0 0 * * *",
    parameters: {},
    isActive: true,
  };
}
