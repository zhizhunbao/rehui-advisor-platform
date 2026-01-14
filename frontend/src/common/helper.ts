import {
  Plane,
  Hotel,
  Briefcase,
  Car,
  Home,
  ShieldCheck,
  GraduationCap,
  TrendingUp,
  Circle,
  Package,
  FileText,
  Receipt,
  Languages,
  Compass,
  BookOpen,
  PlayCircle,
  FlaskConical,
  Bot,
} from "lucide-react";
import { createElement } from "react";

// ========== Icons ==========
const ICON_MAP = {
  Plane,
  Hotel,
  Briefcase,
  Car,
  Home,
  ShieldCheck,
  GraduationCap,
  TrendingUp,
  Circle,
  Package,
  FileText,
  Receipt,
  Languages,
  Compass,
  BookOpen,
  PlayCircle,
  FlaskConical,
  Bot,
} as const;

type IconName = keyof typeof ICON_MAP;

export function getIcon(name: string, className?: string) {
  const Icon = ICON_MAP[name as IconName] || Circle;
  return createElement(Icon, { className });
}

// ========== API ==========
export function getApiBase() {
  return import.meta.env.VITE_API_URL || "/api";
}

export function getAuthHeaders() {
  return {
    "Content-Type": "application/json",
    Authorization: `Bearer ${localStorage.getItem("admin_token") || ""}`,
  };
}

// ========== Format ==========
export function formatDate(date: string | Date | null | undefined): string {
  if (!date) return "";
  return new Date(date).toLocaleDateString();
}

export function formatDateTime(date: string | Date | null | undefined): string {
  if (!date) return "";
  return new Date(date).toLocaleString();
}

export function formatFileSize(bytes: number): string {
  if (bytes === 0) return "0 B";
  const k = 1024;
  const sizes = ["B", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(1))} ${sizes[i]}`;
}

// ========== String ==========
export function truncate(str: string, length: number): string {
  if (str.length <= length) return str;
  return str.slice(0, length) + "...";
}

export function capitalize(str: string): string {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

// ========== Misc ==========
export function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export function generateId(): string {
  return Math.random().toString(36).substring(2, 9);
}

// ========== Case Conversion ==========
export function snakeToCamel(str: string): string {
  return str.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase());
}

export function camelToSnake(str: string): string {
  return str.replace(/[A-Z]/g, (letter) => `_${letter.toLowerCase()}`);
}

export function keysToCamel<T>(obj: unknown): T {
  if (Array.isArray(obj)) {
    return obj.map((item) => keysToCamel(item)) as T;
  }
  if (obj !== null && typeof obj === "object") {
    return Object.fromEntries(
      Object.entries(obj).map(([key, value]) => [
        snakeToCamel(key),
        keysToCamel(value),
      ])
    ) as T;
  }
  return obj as T;
}

// ========== Admin Menu ==========
import type { AdminMenuItem, AdminMenuGroup, AdminMenuConfig } from "./types";

export function isAdminMenuGroup(
  item: AdminMenuItem | AdminMenuGroup
): item is AdminMenuGroup {
  return "children" in item;
}

export function getAllAdminMenuItems(config: AdminMenuConfig): AdminMenuItem[] {
  const items: AdminMenuItem[] = [];
  for (const item of config) {
    if (isAdminMenuGroup(item)) {
      items.push(...item.children);
    } else {
      items.push(item);
    }
  }
  return items;
}
