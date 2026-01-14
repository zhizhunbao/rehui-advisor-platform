// ========== User ==========
export const UserType = {
  Anonymous: "ANONYMOUS",
  Registered: "REGISTERED",
  Premium: "PREMIUM",
} as const;
export type UserType = (typeof UserType)[keyof typeof UserType];

export const UserStatus = {
  Active: "active",
  Inactive: "inactive",
  Banned: "banned",
} as const;
export type UserStatus = (typeof UserStatus)[keyof typeof UserStatus];

// ========== Common ==========
export const HttpMethod = {
  Get: "GET",
  Post: "POST",
  Put: "PUT",
  Delete: "DELETE",
  Patch: "PATCH",
} as const;
export type HttpMethod = (typeof HttpMethod)[keyof typeof HttpMethod];

export const SortOrder = {
  Asc: "asc",
  Desc: "desc",
} as const;
export type SortOrder = (typeof SortOrder)[keyof typeof SortOrder];

export const ThemeMode = {
  Light: "light",
  Dark: "dark",
  System: "system",
} as const;
export type ThemeMode = (typeof ThemeMode)[keyof typeof ThemeMode];

export const Lang = {
  En: "en",
  Zh: "zh",
} as const;
export type Lang = (typeof Lang)[keyof typeof Lang];

// ========== App ==========
export const AppView = {
  Home: "home",
  Conversation: "conversation",
  Login: "login",
  Register: "register",
} as const;
export type AppView = (typeof AppView)[keyof typeof AppView];

export const MessageRole = {
  User: "user",
  Assistant: "assistant",
} as const;
export type MessageRole = (typeof MessageRole)[keyof typeof MessageRole];

export const ChartType = {
  Bar: "bar",
  Line: "line",
  Pie: "pie",
} as const;
export type ChartType = (typeof ChartType)[keyof typeof ChartType];

// ========== Admin ==========
export const AdminRole = {
  SuperAdmin: "super_admin",
  Admin: "admin",
  Editor: "editor",
  Viewer: "viewer",
} as const;
export type AdminRole = (typeof AdminRole)[keyof typeof AdminRole];

export const EntityStatus = {
  Active: "active",
  Inactive: "inactive",
  Deleted: "deleted",
  Draft: "draft",
} as const;
export type EntityStatus = (typeof EntityStatus)[keyof typeof EntityStatus];

export const TaskStatus = {
  Pending: "pending",
  Running: "running",
  Success: "success",
  Failed: "failed",
  Cancelled: "cancelled",
} as const;
export type TaskStatus = (typeof TaskStatus)[keyof typeof TaskStatus];

// ========== UI Mappings ==========

// Entity Status
export const EntityStatusColor: Record<EntityStatus, string> = {
  [EntityStatus.Active]: "bg-green-500/20 text-green-700 dark:text-green-400",
  [EntityStatus.Inactive]:
    "bg-yellow-500/20 text-yellow-700 dark:text-yellow-400",
  [EntityStatus.Deleted]: "bg-red-500/20 text-red-700 dark:text-red-400",
  [EntityStatus.Draft]: "bg-slate-500/20 text-slate-600 dark:text-slate-400",
};

// Task Status
export const TaskStatusColor: Record<TaskStatus, string> = {
  [TaskStatus.Pending]: "bg-slate-500/20 text-slate-600",
  [TaskStatus.Running]: "bg-blue-500/20 text-blue-600",
  [TaskStatus.Success]: "bg-green-500/20 text-green-600",
  [TaskStatus.Failed]: "bg-red-500/20 text-red-600",
  [TaskStatus.Cancelled]: "bg-yellow-500/20 text-yellow-600",
};

// Data Source Type
export const DataSourceType = {
  Github: "github",
  Api: "api",
  Web: "web",
  File: "file",
} as const;
export type DataSourceType =
  (typeof DataSourceType)[keyof typeof DataSourceType];

export const DataSourceTypeColor: Record<DataSourceType, string> = {
  [DataSourceType.Github]:
    "bg-violet-500/20 text-violet-700 dark:text-violet-400",
  [DataSourceType.Api]: "bg-blue-500/20 text-blue-700 dark:text-blue-400",
  [DataSourceType.Web]:
    "bg-emerald-500/20 text-emerald-700 dark:text-emerald-400",
  [DataSourceType.File]: "bg-amber-500/20 text-amber-700 dark:text-amber-400",
};

export const DataSourceTypeColors: Record<string, string> = {
  github: "bg-violet-500/20 text-violet-700 dark:text-violet-400",
  api: "bg-blue-500/20 text-blue-700 dark:text-blue-400",
  website: "bg-amber-500/20 text-amber-700 dark:text-amber-400",
  rss: "bg-orange-500/20 text-orange-700 dark:text-orange-400",
};

export const DataSourceStatusColors: Record<string, string> = {
  active: "bg-green-500/20 text-green-700 dark:text-green-400",
  archived: "bg-slate-500/20 text-slate-600 dark:text-slate-400",
  invalid: "bg-rose-500/20 text-rose-700 dark:text-rose-400",
  pending: "bg-amber-500/20 text-amber-700 dark:text-amber-400",
};

// Icon Mapping (domain icons)
export const IconMap: Record<string, string> = {
  plane: "Plane",
  building: "Hotel",
  briefcase: "Briefcase",
  car: "Car",
  home: "Home",
  shield: "ShieldCheck",
  "graduation-cap": "GraduationCap",
  "trending-up": "TrendingUp",
};

// Color Mapping (hex to tailwind)
export const ColorMap: Record<string, string> = {
  "#3B82F6": "bg-blue-500",
  "#10B981": "bg-emerald-500",
  "#6366F1": "bg-indigo-500",
  "#F97316": "bg-orange-500",
  "#EF4444": "bg-rose-500",
  "#06B6D4": "bg-cyan-500",
  "#8B5CF6": "bg-purple-500",
  "#F59E0B": "bg-amber-500",
};

// ========== LLM ==========
export const LLMProvider = {
  OpenAI: "openai",
  Anthropic: "anthropic",
  Google: "google",
  MetaLlama: "meta-llama",
  MistralAI: "mistralai",
  DeepSeek: "deepseek",
  Qwen: "qwen",
  Microsoft: "microsoft",
  Cohere: "cohere",
  Groq: "groq",
  XAI: "x-ai",
  Amazon: "amazon",
  Nvidia: "nvidia",
  Perplexity: "perplexity",
  OpenRouter: "openrouter",
  Azure: "azure",
  VertexAI: "vertex_ai",
  Bedrock: "bedrock",
  Ollama: "ollama",
  VLLM: "vllm",
} as const;
export type LLMProvider = (typeof LLMProvider)[keyof typeof LLMProvider];

export const LLMProviderLabel: Record<string, string> = {
  openai: "OpenAI",
  anthropic: "Anthropic",
  google: "Google",
  "meta-llama": "Meta Llama",
  mistralai: "Mistral AI",
  deepseek: "DeepSeek",
  qwen: "Qwen (阿里)",
  microsoft: "Microsoft",
  cohere: "Cohere",
  groq: "Groq",
  "x-ai": "xAI (Grok)",
  amazon: "Amazon",
  nvidia: "NVIDIA",
  perplexity: "Perplexity",
  openrouter: "OpenRouter",
  azure: "Azure",
  vertex_ai: "Vertex AI",
  bedrock: "AWS Bedrock",
  ollama: "Ollama",
  vllm: "vLLM",
};

export const LLMProviderPriority: Record<string, number> = {
  openai: 1,
  anthropic: 2,
  google: 3,
  "meta-llama": 4,
  mistralai: 5,
  deepseek: 6,
  qwen: 7,
  microsoft: 8,
  cohere: 9,
  groq: 10,
  "x-ai": 11,
  amazon: 12,
  nvidia: 13,
  perplexity: 14,
  openrouter: 15,
  azure: 16,
  vertex_ai: 17,
  bedrock: 18,
  ollama: 90,
  vllm: 91,
};

export const LLMCategory = {
  General: "general",
  Chat: "chat",
  Coding: "coding",
  Reasoning: "reasoning",
  Vision: "vision",
  Embedding: "embedding",
} as const;
export type LLMCategory = (typeof LLMCategory)[keyof typeof LLMCategory];

export const LLMCategoryLabel: Record<string, { zh: string; en: string }> = {
  general: { zh: "通用", en: "General" },
  chat: { zh: "对话", en: "Chat" },
  coding: { zh: "编程", en: "Coding" },
  reasoning: { zh: "推理", en: "Reasoning" },
  vision: { zh: "视觉", en: "Vision" },
  embedding: { zh: "嵌入", en: "Embedding" },
};

export const LLMDeploymentType = {
  API: "api",
  Local: "local",
  Hybrid: "hybrid",
} as const;
export type LLMDeploymentType =
  (typeof LLMDeploymentType)[keyof typeof LLMDeploymentType];

export const LLMDeploymentTypeLabel: Record<
  string,
  { zh: string; en: string }
> = {
  api: { zh: "API 调用", en: "API" },
  local: { zh: "本地部署", en: "Local" },
  hybrid: { zh: "混合", en: "Hybrid" },
};

export const LLMCapabilities = [
  "vision",
  "function_calling",
  "json_mode",
  "streaming",
  "code_interpreter",
  "web_search",
] as const;
export type LLMCapability = (typeof LLMCapabilities)[number];

// ========== Retrieval Engine ==========
export const RetrievalEngineTypeCode = {
  KeywordMatch: "keyword_match",
  StructuredQuery: "structured_query",
  RagVector: "rag_vector",
  PageIndex: "page_index",
  AgentTools: "agent_tools",
  RealtimeSearch: "realtime_search",
  Hybrid: "hybrid",
} as const;
export type RetrievalEngineTypeCode =
  (typeof RetrievalEngineTypeCode)[keyof typeof RetrievalEngineTypeCode];

export const RetrievalEngineTypeConfig: Record<
  string,
  { icon: string; color: string }
> = {
  keyword_match: { icon: "🔤", color: "slate" },
  structured_query: { icon: "📊", color: "blue" },
  rag_vector: { icon: "🧠", color: "violet" },
  page_index: { icon: "🌲", color: "emerald" },
  agent_tools: { icon: "🤖", color: "amber" },
  realtime_search: { icon: "🌐", color: "cyan" },
  hybrid: { icon: "🔀", color: "rose" },
};

export const RetrievalEngineTypeColor: Record<string, string> = {
  keyword_match: "bg-slate-500/20 text-slate-600 dark:text-slate-400",
  structured_query: "bg-blue-500/20 text-blue-600 dark:text-blue-400",
  rag_vector: "bg-violet-500/20 text-violet-600 dark:text-violet-400",
  page_index: "bg-emerald-500/20 text-emerald-600 dark:text-emerald-400",
  agent_tools: "bg-amber-500/20 text-amber-600 dark:text-amber-400",
  realtime_search: "bg-cyan-500/20 text-cyan-600 dark:text-cyan-400",
  hybrid: "bg-rose-500/20 text-rose-600 dark:text-rose-400",
};

// ========== Admin Menu ==========
import type { AdminMenuConfig } from "./types";

export const ADMIN_MENU_CONFIG: AdminMenuConfig = [
  { path: "/admin", label: "dashboard", icon: "📊" },
  { path: "/admin/analytics", label: "analytics", icon: "📈" },
  {
    key: "ai",
    label: "aiCore",
    icon: "🤖",
    children: [
      { path: "/admin/llm", label: "llm", icon: "🧠" },
      { path: "/admin/prompts", label: "prompts", icon: "💬" },
      { path: "/admin/skills", label: "skills", icon: "🧩" },
      { path: "/admin/agent-frameworks", label: "agentFrameworks", icon: "🤝" },
    ],
  },
  {
    key: "data",
    label: "dataManagement",
    icon: "📦",
    children: [
      { path: "/admin/domains", label: "domains", icon: "🌐" },
      { path: "/admin/data-sources", label: "dataSources", icon: "🔗" },
      { path: "/admin/crawlers", label: "crawlers", icon: "🕷️" },
      { path: "/admin/retrieval", label: "retrieval", icon: "🔍" },
      { path: "/admin/scheduler", label: "scheduler", icon: "📅" },
    ],
  },
  {
    key: "content",
    label: "contentManagement",
    icon: "📝",
    children: [
      { path: "/admin/questions", label: "questions", icon: "❓" },
      { path: "/admin/recommendations", label: "recommendations", icon: "⭐" },
    ],
  },
  {
    key: "users",
    label: "userManagement",
    icon: "👥",
    children: [
      { path: "/admin/users", label: "users", icon: "👤" },
      { path: "/admin/conversations", label: "conversations", icon: "💭" },
      { path: "/admin/subscriptions", label: "subscriptions", icon: "💳" },
    ],
  },
  {
    path: "/admin/configs",
    label: "configs",
    icon: "⚙️",
    superAdminOnly: true,
  },
];
