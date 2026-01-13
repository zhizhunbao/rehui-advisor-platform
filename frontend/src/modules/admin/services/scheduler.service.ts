// Admin 定时任务管理 API
import { http } from "@/common/http";
import type {
  ScheduledJob,
  JobType,
  JobExecution,
  ScheduledJobCreate,
} from "@/common/types";

export const schedulerService = {
  async getJobs() {
    return http.get<ScheduledJob[]>("/scheduler/jobs");
  },

  async getJobTypes() {
    return http.get<JobType[]>("/scheduler/job-types");
  },

  async getJobHistory(jobId: string) {
    return http.get<JobExecution[]>(`/scheduler/jobs/${jobId}/history`);
  },

  async create(data: ScheduledJobCreate) {
    return http.post<ScheduledJob>("/scheduler/jobs", data);
  },

  async update(id: string, data: ScheduledJobCreate) {
    return http.put<ScheduledJob>(`/scheduler/jobs/${id}`, data);
  },

  async delete(id: string) {
    return http.delete<void>(`/scheduler/jobs/${id}`);
  },

  async toggle(id: string) {
    return http.post<ScheduledJob>(`/scheduler/jobs/${id}/toggle`);
  },

  async trigger(id: string) {
    return http.post<{ success: boolean }>(`/scheduler/jobs/${id}/trigger`);
  },
};
