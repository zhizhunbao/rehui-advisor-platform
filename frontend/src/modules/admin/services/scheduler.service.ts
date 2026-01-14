// Admin 调度任务 Service
import type {
  ScheduledJob,
  JobType,
  JobExecution,
  ScheduledJobCreate,
} from "@/common/types";
import { getApiBase, getAuthHeaders, keysToCamel } from "@/common/helper";

const API_BASE = getApiBase();

export const schedulerService = {
  async getJobs(): Promise<ScheduledJob[]> {
    const res = await fetch(`${API_BASE}/scheduler/jobs`, {
      headers: getAuthHeaders(),
    });
    const json = await res.json();
    return (json.data || []).map(keysToCamel) as ScheduledJob[];
  },

  async getJobTypes(): Promise<JobType[]> {
    const res = await fetch(`${API_BASE}/scheduler/job-types`, {
      headers: getAuthHeaders(),
    });
    const json = await res.json();
    return (json.data || []).map(keysToCamel) as JobType[];
  },

  async getHistory(jobId: string): Promise<JobExecution[]> {
    const res = await fetch(`${API_BASE}/scheduler/jobs/${jobId}/history`, {
      headers: getAuthHeaders(),
    });
    const json = await res.json();
    return (json.data || []).map(keysToCamel) as JobExecution[];
  },

  async create(data: ScheduledJobCreate): Promise<ScheduledJob> {
    const res = await fetch(`${API_BASE}/scheduler/jobs`, {
      method: "POST",
      headers: { ...getAuthHeaders(), "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    const json = await res.json();
    return keysToCamel(json.data) as ScheduledJob;
  },

  async update(id: string, data: ScheduledJobCreate): Promise<ScheduledJob> {
    const res = await fetch(`${API_BASE}/scheduler/jobs/${id}`, {
      method: "PUT",
      headers: { ...getAuthHeaders(), "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    const json = await res.json();
    return keysToCamel(json.data) as ScheduledJob;
  },

  async delete(id: string): Promise<void> {
    await fetch(`${API_BASE}/scheduler/jobs/${id}`, {
      method: "DELETE",
      headers: getAuthHeaders(),
    });
  },

  async toggle(id: string): Promise<void> {
    await fetch(`${API_BASE}/scheduler/jobs/${id}/toggle`, {
      method: "POST",
      headers: getAuthHeaders(),
    });
  },

  async trigger(id: string): Promise<boolean> {
    const res = await fetch(`${API_BASE}/scheduler/jobs/${id}/trigger`, {
      method: "POST",
      headers: getAuthHeaders(),
    });
    const json = await res.json();
    return json.success;
  },
};
