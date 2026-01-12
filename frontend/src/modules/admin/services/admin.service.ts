import { http } from "@/common/http";
import type {
  Domain,
  DomainCategory,
  CreateDomainCategoryDto,
  UpdateDomainCategoryDto,
  CreateDomainDto,
  UpdateDomainDto,
  PromptTemplate,
  CreatePromptDto,
  UpdatePromptDto,
  Question,
  CreateQuestionDto,
  CrawlSource,
  CrawlTask,
  AnalyticsSummary,
} from "../types/admin.types";

// 领域分类管理
export const domainCategoryService = {
  getAll() {
    return http.get<DomainCategory[]>("/admin/domain-categories");
  },
  getById(id: string) {
    return http.get<DomainCategory>(`/admin/domain-categories/${id}`);
  },
  create(data: CreateDomainCategoryDto) {
    return http.post<DomainCategory>("/admin/domain-categories", data);
  },
  update(id: string, data: UpdateDomainCategoryDto) {
    return http.put<DomainCategory>(`/admin/domain-categories/${id}`, data);
  },
  delete(id: string) {
    return http.delete<void>(`/admin/domain-categories/${id}`);
  },
};

// 领域管理
export const domainService = {
  getAll(categoryId?: string) {
    const query = categoryId ? `?category_id=${categoryId}` : "";
    return http.get<Domain[]>(`/admin/domains${query}`);
  },
  getById(id: string) {
    return http.get<Domain>(`/admin/domains/${id}`);
  },
  create(data: CreateDomainDto) {
    return http.post<Domain>("/admin/domains", data);
  },
  update(id: string, data: UpdateDomainDto) {
    return http.put<Domain>(`/admin/domains/${id}`, data);
  },
  delete(id: string) {
    return http.delete<void>(`/admin/domains/${id}`);
  },
};

// Prompt 管理
export const promptService = {
  getAll() {
    return http.get<PromptTemplate[]>("/admin/prompts");
  },
  getById(id: string) {
    return http.get<PromptTemplate>(`/admin/prompts/${id}`);
  },
  create(data: CreatePromptDto) {
    return http.post<PromptTemplate>("/admin/prompts", data);
  },
  update(id: string, data: UpdatePromptDto) {
    return http.put<PromptTemplate>(`/admin/prompts/${id}`, data);
  },
  delete(id: string) {
    return http.delete<void>(`/admin/prompts/${id}`);
  },
};

// 问题库管理
export const questionService = {
  getAll(domainId?: string) {
    const query = domainId ? `?domainId=${domainId}` : "";
    return http.get<Question[]>(`/admin/questions${query}`);
  },
  getById(id: string) {
    return http.get<Question>(`/admin/questions/${id}`);
  },
  create(data: CreateQuestionDto) {
    return http.post<Question>("/admin/questions", data);
  },
  update(id: string, data: Partial<CreateQuestionDto>) {
    return http.put<Question>(`/admin/questions/${id}`, data);
  },
  delete(id: string) {
    return http.delete<void>(`/admin/questions/${id}`);
  },
};

// 数据抓取管理
export const crawlerService = {
  getSources() {
    return http.get<CrawlSource[]>("/admin/crawlers/sources");
  },
  createSource(data: Partial<CrawlSource>) {
    return http.post<CrawlSource>("/admin/crawlers/sources", data);
  },
  updateSource(id: string, data: Partial<CrawlSource>) {
    return http.put<CrawlSource>(`/admin/crawlers/sources/${id}`, data);
  },
  deleteSource(id: string) {
    return http.delete<void>(`/admin/crawlers/sources/${id}`);
  },
  getTasks(sourceId?: string) {
    const query = sourceId ? `?sourceId=${sourceId}` : "";
    return http.get<CrawlTask[]>(`/admin/crawlers/tasks${query}`);
  },
  runTask(sourceId: string) {
    return http.post<CrawlTask>(`/admin/crawlers/sources/${sourceId}/run`);
  },
};

// 分析统计
export const analyticsService = {
  getSummary() {
    return http.get<AnalyticsSummary>("/admin/analytics/summary");
  },
};
