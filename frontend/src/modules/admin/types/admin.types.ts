// 领域分类
export interface DomainCategory {
  id: string;
  code: string;
  name: string;
  nameEn: string;
  description: string;
  descriptionEn: string;
  isActive: boolean;
  sortOrder: number;
  createdAt: string;
  updatedAt: string;
}

export interface CreateDomainCategoryDto {
  code: string;
  name: string;
  nameEn: string;
  description: string;
  descriptionEn: string;
  sortOrder: number;
}

export interface UpdateDomainCategoryDto {
  name: string;
  nameEn: string;
  description: string;
  descriptionEn: string;
  isActive: boolean;
  sortOrder: number;
}

// 领域配置
export interface Domain {
  id: string;
  code: string;
  name: string;
  nameEn: string;
  description: string;
  descriptionEn: string;
  icon: string;
  color: string;
  categoryId: string;
  promptTemplateId: string;
  isActive: boolean;
  sortOrder: number;
  discoveryKeywords: string[];
  createdAt: string;
  updatedAt: string;
  // Joined from prompt_templates table (snake_case -> camelCase by http client)
  promptTemplates?: {
    id: string;
    name: string;
    template: string;
    templateEn: string;
  };
}

export interface CreateDomainDto {
  code: string;
  name: string;
  nameEn: string;
  description: string;
  descriptionEn: string;
  icon: string;
  color: string;
  categoryId: string;
  promptTemplateId: string;
  sortOrder: number;
  discoveryKeywords: string[];
}

export interface UpdateDomainDto {
  name: string;
  nameEn: string;
  description: string;
  descriptionEn: string;
  icon: string;
  color: string;
  categoryId: string;
  promptTemplateId: string;
  isActive: boolean;
  sortOrder: number;
  discoveryKeywords: string[];
}

// Prompt 模板
export interface PromptTemplate {
  id: string;
  name: string;
  description: string;
  content: string;
  contentEn: string;
  category: string;
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface CreatePromptDto {
  name: string;
  description: string;
  content: string;
  contentEn: string;
  category: string;
}

export interface UpdatePromptDto {
  name: string;
  description: string;
  content: string;
  contentEn: string;
  category: string;
  isActive: boolean;
}

// 问题库
export interface Question {
  id: string;
  domainId: string;
  text: string;
  textEn: string;
  type: "single" | "multiple" | "text";
  options: QuestionOption[];
  sortOrder: number;
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface QuestionOption {
  id: string;
  text: string;
  textEn: string;
  value: string;
}

export interface CreateQuestionDto {
  domainId: string;
  text: string;
  textEn: string;
  type: "single" | "multiple" | "text";
  options: Omit<QuestionOption, "id">[];
  sortOrder: number;
}

// 数据抓取
export interface CrawlSource {
  id: string;
  name: string;
  url: string;
  domainId: string;
  schedule: string;
  isActive: boolean;
  lastRunAt: string;
  lastStatus: string;
  createdAt: string;
  updatedAt: string;
}

export interface CrawlTask {
  id: string;
  sourceId: string;
  status: "pending" | "running" | "success" | "failed";
  startedAt: string;
  finishedAt: string;
  recordsCount: number;
  errorMessage: string;
}

// 分析统计
export interface AnalyticsSummary {
  totalUsers: number;
  totalSessions: number;
  totalMessages: number;
  activeUsersToday: number;
  popularDomains: { domainId: string; count: number }[];
  recentActivity: { date: string; sessions: number; messages: number }[];
}

// 分页响应
export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  limit: number;
}

// 用户管理
export interface AdminUser {
  id: string;
  email: string;
  name: string;
  userType: "ANONYMOUS" | "REGISTERED" | "PREMIUM";
  status: "ACTIVE" | "INACTIVE" | "BANNED";
  subscriptionPlanId: string;
  searchCount: number;
  createdAt: string;
  updatedAt: string;
}

export interface UpdateUserDto {
  name: string;
  status: "ACTIVE" | "INACTIVE" | "BANNED";
  subscriptionPlanId: string;
}

// 对话记录
export interface AdminConversation {
  id: string;
  userId: string;
  title: string;
  messageCount: number;
  lastMessageAt: string;
  createdAt: string;
  updatedAt: string;
  messages: AdminMessage[];
}

export interface AdminMessage {
  id: string;
  conversationId: string;
  role: "user" | "assistant";
  content: string;
  createdAt: string;
}

// 订阅方案
export interface SubscriptionPlan {
  id: string;
  name: string;
  nameEn: string;
  description: string;
  descriptionEn: string;
  price: number;
  currency: string;
  dailyQuota: number;
  features: string[];
  isActive: boolean;
  sortOrder: number;
  createdAt: string;
  updatedAt: string;
}

export interface CreateSubscriptionDto {
  name: string;
  nameEn: string;
  description: string;
  descriptionEn: string;
  price: number;
  currency: string;
  dailyQuota: number;
  features: string[];
  sortOrder: number;
}

export interface UpdateSubscriptionDto {
  name: string;
  nameEn: string;
  description: string;
  descriptionEn: string;
  price: number;
  currency: string;
  dailyQuota: number;
  features: string[];
  isActive: boolean;
  sortOrder: number;
}

// 推荐方案
export interface AdminRecommendation {
  id: string;
  userId: string;
  domainId: string;
  title: string;
  content: string;
  status: "PENDING" | "APPROVED" | "REJECTED";
  createdAt: string;
  updatedAt: string;
}

export interface UpdateRecommendationDto {
  title: string;
  content: string;
  status: "PENDING" | "APPROVED" | "REJECTED";
}

// 系统配置
export interface SystemConfig {
  id: string;
  key: string;
  value: string;
  category: string;
  description: string;
  isSensitive: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface CreateConfigDto {
  key: string;
  value: string;
  category: string;
  description: string;
  isSensitive: boolean;
}

export interface UpdateConfigDto {
  value: string;
  category: string;
  description: string;
  isSensitive: boolean;
}
