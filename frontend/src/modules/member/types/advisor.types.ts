import type { User, QuotaStatus } from "./auth.types";

export type AppView = "home" | "conversation" | "login" | "register";

export type Language = "zh" | "en";
export type Theme = "light" | "dark";

// 重新导出 auth 类型
export type { User, QuotaStatus };

export interface GroundingSource {
  title: string;
  uri: string;
}

export interface ChartData {
  type: "bar" | "line" | "pie";
  title: string;
  labels: string[];
  values: number[];
  unit?: string;
}

export interface Message {
  id: string;
  role: "user" | "assistant";
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
}
