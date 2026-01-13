// 通用业务类型 - 可被任何层导入
import type {
  Lang,
  ThemeMode,
  AppView,
  MessageRole,
  ChartType,
  UserType,
  AssignmentStatus,
  ResourceType,
  FileType,
} from "./enum";

// ==================== 基础类型 ====================

export type Language = Lang;
export type Theme = ThemeMode;

// ==================== 共享类型 ====================

export interface User {
  id: string;
  email: string | null;
  name: string | null;
  userType: UserType;
  isAnonymous?: boolean;
}

export interface QuotaStatus {
  userType: UserType;
  searchCount: number;
  searchLimit: number;
  remaining: number;
  resetAt: string | null;
  canSearch: boolean;
  message?: string;
}

export interface GroundingSource {
  title: string;
  uri: string;
}

export interface ChartData {
  type: ChartType;
  title: string;
  labels: string[];
  values: number[];
  unit?: string;
}

export interface Message {
  id: string;
  role: MessageRole;
  content: string;
  timestamp: number;
  sources?: GroundingSource[];
  isStreaming?: boolean;
  chartData?: ChartData;
  suggestedQuestions?: string[];
  metadata?: {
    hidden?: boolean;
  };
}

export interface Conversation {
  id: string;
  title: string;
  messages: Message[];
  topicId?: string;
  updatedAt: number;
}

export interface Topic {
  id: string;
  title: string;
  description: string;
  icon: string;
  color: string;
  prompt: string;
  route?: string | null;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  limit: number;
}

// ==================== Learning 类型 ====================

export interface Course {
  id: string;
  name: string;
  code: string | null;
  description: string | null;
  semester: string | null;
  instructor: string | null;
  createdAt: string;
  updatedAt: string;
}

export interface CourseCreate {
  name: string;
  code?: string;
  description?: string;
  semester?: string;
  instructor?: string;
}

export type CourseUpdate = Partial<CourseCreate>;

export interface Lab {
  id: string;
  courseId: string;
  title: string;
  description: string | null;
  instructionsMd: string | null;
  originalFileId: string | null;
  dueDate: string | null;
  order: number;
  createdAt: string;
  updatedAt: string;
}

export interface LabCreate {
  courseId: string;
  title: string;
  description?: string;
  instructionsMd?: string;
  originalFileId?: string;
  dueDate?: string;
  order?: number;
}

export type LabUpdate = Partial<Omit<LabCreate, "courseId">>;

export interface Assignment {
  id: string;
  labId: string;
  title: string | null;
  notebookFileId: string | null;
  notes: string | null;
  status: AssignmentStatus;
  score: number | null;
  feedback: string | null;
  createdAt: string;
  updatedAt: string;
}

export interface AssignmentCreate {
  labId: string;
  title?: string;
  notebookFileId?: string;
  notes?: string;
}

export interface AssignmentUpdate {
  title?: string;
  notebookFileId?: string;
  notes?: string;
  status?: AssignmentStatus;
  score?: number;
  feedback?: string;
}

export interface Resource {
  id: string;
  url: string;
  title: string;
  description: string | null;
  type: ResourceType;
  courseId: string | null;
  labId: string | null;
  cachedContent: string | null;
  createdAt: string;
  updatedAt: string;
}

export interface ResourceCreate {
  url: string;
  title: string;
  description?: string;
  type?: ResourceType;
  courseId?: string;
  labId?: string;
}

export type ResourceUpdate = Partial<ResourceCreate>;

export interface UploadedFile {
  id: string;
  filename: string;
  fileType: FileType;
  size: number;
  path: string;
  url: string | null;
  createdAt: string;
}

export interface ConvertResult {
  fileId: string;
  markdown: string;
  originalFilename: string;
}

// ==================== Member 类型 ====================

export interface LoginDto {
  email: string;
  password: string;
}

export interface RegisterDto {
  email: string;
  password: string;
  name?: string;
}

export interface UpdatePasswordDto {
  oldPassword: string;
  newPassword: string;
}

// ==================== Admin 类型 ====================

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

export interface AnalyticsSummary {
  totalUsers: number;
  totalSessions: number;
  totalMessages: number;
  activeUsersToday: number;
  popularDomains: { domainId: string; count: number }[];
  recentActivity: { date: string; sessions: number; messages: number }[];
}

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
}

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

// ==================== Admin Skill ====================

export interface Skill {
  id: string;
  name: string;
  description: string;
  category: string;
  source: string;
  repo: string;
  content: string;
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface SkillStats {
  total: number;
  active: number;
  inactive: number;
  categories: { category: string; count: number }[];
  sources: { source: string; count: number }[];
}

export interface SkillLabel {
  id: string;
  code: string;
  labelZh: string;
  labelEn: string;
  type: string;
  sortOrder: number;
}

export interface SkillLabels {
  categories: SkillLabel[];
  sources: SkillLabel[];
}

export interface SkillListParams {
  page?: number;
  limit?: number;
  search?: string;
  category?: string;
  source?: string;
}

// ==================== Admin Prompt (列表页) ====================

export interface AdminPrompt {
  id: string;
  name: string;
  description: string;
  template: string;
  category: string;
  source: string;
  repo: string;
  isActive: boolean;
  createdAt: string;
}

export interface AdminPromptStats {
  total: number;
  active: number;
  inactive: number;
  categories: { category: string; count: number }[];
  sources: { source: string; count: number }[];
}

// ==================== Admin LLM ====================

export interface LLMModel {
  id: string;
  name: string;
  displayName: string;
  provider: string;
  apiEndpoint: string;
  version: string;
  category: string;
  deploymentType: string;
  inputPrice: number;
  outputPrice: number;
  isFree: boolean;
  contextWindow: number;
  maxOutputTokens: number;
  capabilities: string[];
  description: string;
  dockerImage: string;
  hardwareRequirements: Record<string, string>;
  rateLimit: Record<string, number>;
  latencyMs: number;
  qualityScore: number;
  license: string;
  releaseDate: string;
  isDeprecated: boolean;
  fallbackModelId: string;
  isActive: boolean;
  isDefault: boolean;
  config: Record<string, string>;
  sortOrder: number;
  createdAt: string;
}

export interface LLMSyncSource {
  id: string;
  name: string;
  url: string;
  status: string;
}

export interface LLMSyncResult {
  synced: number;
  errors: { source: string; error: string }[];
}

export interface LLMModelCreate {
  name: string;
  displayName: string;
  provider: string;
  apiEndpoint: string;
  version?: string;
  category?: string;
  deploymentType?: string;
  inputPrice?: number;
  outputPrice?: number;
  isFree?: boolean;
  contextWindow?: number;
  maxOutputTokens?: number;
  capabilities?: string[];
  description?: string;
  dockerImage?: string;
  hardwareRequirements?: Record<string, string>;
  rateLimit?: Record<string, number>;
  latencyMs?: number;
  qualityScore?: number;
  license?: string;
  releaseDate?: string;
  isDeprecated?: boolean;
  fallbackModelId?: string | null;
  isActive?: boolean;
  isDefault?: boolean;
  config?: Record<string, string>;
  sortOrder?: number;
}

export interface LLMModelForm {
  name: string;
  displayName: string;
  provider: string;
  apiEndpoint: string;
  version: string;
  category: string;
  deploymentType: string;
  inputPrice: number;
  outputPrice: number;
  isFree: boolean;
  contextWindow: number;
  maxOutputTokens: number;
  capabilities: string[];
  description: string;
  dockerImage: string;
  hardwareRequirements: Record<string, string>;
  rateLimit: Record<string, number>;
  latencyMs: number;
  qualityScore: number;
  license: string;
  releaseDate: string;
  isDeprecated: boolean;
  fallbackModelId: string;
  isActive: boolean;
  isDefault: boolean;
  config: Record<string, string>;
  sortOrder: number;
}

// ==================== Admin Retrieval ====================

export interface RetrievalEngine {
  id: string;
  name: string;
  displayName: string;
  type: string;
  description: string;
  config: Record<string, unknown>;
  isActive: boolean;
  isDefault: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface RetrievalEngineType {
  type: string;
  name: string;
  description: string;
}

export interface RetrievalEngineCreate {
  name: string;
  displayName: string;
  type: string;
  description?: string;
  config?: Record<string, unknown>;
  isActive?: boolean;
}

export interface RetrievalTestResult {
  engineId: string;
  query: string;
  results: unknown[];
  latencyMs: number;
}

// ==================== Admin Scheduler ====================

export interface ScheduledJob {
  id: string;
  name: string;
  description: string;
  jobType: string;
  cronExpression: string;
  parameters: Record<string, unknown>;
  isActive: boolean;
  lastRunAt: string;
  nextRunAt: string;
  lastStatus: string;
  createdAt: string;
  updatedAt: string;
}

export interface JobType {
  type: string;
  nameZh: string;
  nameEn: string;
  descriptionZh: string;
  descriptionEn: string;
  parametersSchema: Record<string, unknown>;
}

export interface JobExecution {
  id: string;
  jobId: string;
  startedAt: string;
  finishedAt: string;
  status: string;
  result: Record<string, unknown>;
  errorMessage: string;
  createdAt: string;
}

export interface ScheduledJobCreate {
  name: string;
  description?: string;
  jobType: string;
  cronExpression: string;
  parameters?: Record<string, unknown>;
  isActive?: boolean;
}

// ==================== Admin DataSource ====================

export interface DataSource {
  id: string;
  url: string;
  name: string;
  description: string;
  type: string;
  categoryId: string;
  domainId: string;
  tags: string[];
  status: string;
  githubStars?: number;
  githubForks?: number;
  githubLanguage?: string;
  lastSyncedAt?: string;
  createdAt: string;
  updatedAt: string;
}

export interface DataSourceStats {
  total: number;
  byType: Record<string, number>;
  byStatus: Record<string, number>;
  byCategory: { category: string; count: number }[];
}

export interface DataSourceCategory {
  id: string;
  code: string;
  name: string;
  nameEn: string;
  count: number;
}

export interface DataSourceDomain {
  id: string;
  code: string;
  name: string;
  nameEn: string;
  count: number;
}

export interface DataSourceTypeItem {
  type: string;
  count: number;
}

export interface DataSourceStatusItem {
  status: string;
  count: number;
}

export interface DataSourceLanguageItem {
  language: string;
  count: number;
}

export interface DataSourceListParams {
  page?: number;
  limit?: number;
  search?: string;
  categoryId?: string;
  domainId?: string;
  status?: string;
  type?: string;
  language?: string;
}

export interface DataSourceCreate {
  url: string;
  name?: string;
  description?: string;
  type?: string;
  categoryId?: string;
  domainId?: string;
  tags?: string[];
}

// ==================== Admin List Params ====================

export interface UserListParams {
  page?: number;
  limit?: number;
  search?: string;
  status?: string;
}

export interface RecommendationListParams {
  page?: number;
  limit?: number;
  domainId?: string;
  status?: string;
}

export interface ConversationListParams {
  page?: number;
  limit?: number;
  userId?: string;
  startDate?: string;
  endDate?: string;
}

// ==================== Member Domain ====================

export interface ProductLine {
  id: string;
  code: string;
  name: string;
  nameEn: string;
  description: string;
  descriptionEn: string;
  icon: string;
  color: string;
  sortOrder: number;
}

export interface TopicCategory {
  id: string;
  code: string;
  name: string;
  icon: string;
  color: string;
  topics: Topic[];
}

// ==================== Member Advisor ====================

export interface StreamChunk {
  text: string;
  sources: GroundingSource[];
  error?: string;
}

// ==================== Admin Auth ====================

export type AdminRole = "super_admin" | "admin";

export interface AdminAuthUser {
  id: string;
  username: string;
  email: string;
  name: string;
  role: AdminRole;
  isActive: boolean;
}

export interface AdminAuthState {
  admin: AdminAuthUser | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

export interface AdminAuthContextValue extends AdminAuthState {
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  refreshToken: () => Promise<void>;
}

export interface AdminSettingsState {
  lang: Language;
  themeName: string;
}

export interface AdminSettingsContextValue {
  lang: Language;
  setLang: (lang: Language) => void;
  themeName: string;
  setThemeName: (name: string) => void;
}

// ==================== Member Domain (内部) ====================

export interface DomainConfig {
  id: string;
  code: string;
  name: string;
  nameEn: string;
  description: string;
  descriptionEn: string;
  icon: string;
  color: string;
  prompt: string;
  promptEn: string;
  route: string | null;
  isActive: boolean;
  sortOrder: number;
}

export interface GroupedDomain {
  id: string;
  code: string;
  name: string;
  icon: string;
  color: string;
  domains: DomainConfig[];
}

// ==================== Member Auth (内部) ====================

export interface AuthResponse {
  accessToken: string;
  refreshToken: string;
  user: User;
}

export interface AnonymousSessionResponse {
  sessionToken: string;
  userId: string;
  userType: string;
  expiresAt: string;
}

export interface QuotaStatusResponse {
  userType: string;
  searchCount: number;
  dailyLimit: number;
  remaining: number;
}

// ==================== Member Auth (API Response) ====================

export interface AuthApiResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  user_id: string;
  user_type: string;
}

export interface AnonymousSessionApiResponse {
  session_token: string;
  user_id: string;
  user_type: string;
  search_limit: number;
  search_count: number;
}

export interface QuotaStatusApiResponse {
  user_type: string;
  search_count: number;
  search_limit: number;
  remaining: number;
}

export interface UserApiResponse {
  id: string;
  email: string | null;
  name: string | null;
  user_type: string;
  is_anonymous: boolean;
  search_limit: number;
  search_count: number;
}

// ==================== 重新导出枚举类型 ====================

export type {
  Lang,
  ThemeMode,
  AppView,
  MessageRole,
  ChartType,
  UserType,
  AssignmentStatus,
  ResourceType,
  FileType,
};
