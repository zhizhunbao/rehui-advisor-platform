// Admin 定时任务管理 Hook
import { useState, useEffect, useCallback } from "react";
import type {
  ScheduledJob,
  JobType,
  JobExecution,
  ScheduledJobCreate,
} from "@/common/types";
import { schedulerService } from "../services/scheduler.service";

interface UseSchedulerOptions {
  autoFetch?: boolean;
}

export function useScheduler(options: UseSchedulerOptions = {}) {
  const { autoFetch = true } = options;
  const [jobs, setJobs] = useState<ScheduledJob[]>([]);
  const [jobTypes, setJobTypes] = useState<JobType[]>([]);
  const [executionsMap, setExecutionsMap] = useState<
    Record<string, JobExecution[]>
  >({});
  const [loading, setLoading] = useState(false);
  const [loadingHistory, setLoadingHistory] = useState(false);

  const fetchJobs = useCallback(async () => {
    setLoading(true);
    try {
      const data = await schedulerService.getJobs();
      setJobs(data);
      return data;
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchJobTypes = useCallback(async () => {
    const data = await schedulerService.getJobTypes();
    setJobTypes(data);
    return data;
  }, []);

  const fetchHistory = useCallback(async (jobId: string) => {
    setLoadingHistory(true);
    try {
      const data = await schedulerService.getJobHistory(jobId);
      setExecutionsMap((prev) => ({ ...prev, [jobId]: data }));
      return data;
    } finally {
      setLoadingHistory(false);
    }
  }, []);

  const create = useCallback(async (data: ScheduledJobCreate) => {
    const job = await schedulerService.create(data);
    setJobs((prev) => [...prev, job]);
    return job;
  }, []);

  const update = useCallback(async (id: string, data: ScheduledJobCreate) => {
    const job = await schedulerService.update(id, data);
    setJobs((prev) => prev.map((j) => (j.id === id ? job : j)));
    return job;
  }, []);

  const remove = useCallback(async (id: string) => {
    await schedulerService.delete(id);
    setJobs((prev) => prev.filter((j) => j.id !== id));
  }, []);

  const toggle = useCallback(async (id: string) => {
    const job = await schedulerService.toggle(id);
    setJobs((prev) => prev.map((j) => (j.id === id ? job : j)));
    return job;
  }, []);

  const trigger = useCallback(async (id: string) => {
    return schedulerService.trigger(id);
  }, []);

  useEffect(() => {
    if (autoFetch) {
      fetchJobs();
      fetchJobTypes();
    }
  }, [autoFetch, fetchJobs, fetchJobTypes]);

  return {
    jobs,
    jobTypes,
    executionsMap,
    loading,
    loadingHistory,
    fetchJobs,
    fetchJobTypes,
    fetchHistory,
    create,
    update,
    remove,
    toggle,
    trigger,
  };
}
