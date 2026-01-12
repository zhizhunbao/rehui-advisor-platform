// common/http.ts
import { ApiError, logger } from "./logger";

// snake_case 转 camelCase
function snakeToCamel(str: string): string {
  return str.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase());
}

// camelCase 转 snake_case
function camelToSnake(str: string): string {
  return str.replace(/[A-Z]/g, (letter) => `_${letter.toLowerCase()}`);
}

// 递归转换对象的 key
function transformKeys(
  obj: unknown,
  transformer: (key: string) => string
): unknown {
  if (obj === null || obj === undefined) return obj;
  if (Array.isArray(obj)) {
    return obj.map((item) => transformKeys(item, transformer));
  }
  if (typeof obj === "object") {
    const result: Record<string, unknown> = {};
    for (const [key, value] of Object.entries(obj as Record<string, unknown>)) {
      result[transformer(key)] = transformKeys(value, transformer);
    }
    return result;
  }
  return obj;
}

interface RequestConfig {
  method?: "GET" | "POST" | "PUT" | "DELETE" | "PATCH";
  headers?: Record<string, string>;
  body?: unknown;
  timeout?: number;
  traceId?: string;
  skipAuth?: boolean;
}

interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: { code: string; message: string; details?: unknown };
}

const API_BASE = import.meta.env.VITE_API_URL || "/api";
const DEFAULT_TIMEOUT = 30000;

function generateUUID(): string {
  return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0;
    const v = c === "x" ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
}

class TraceManager {
  private currentTraceId: string | null = null;

  start(): string {
    this.currentTraceId = generateUUID();
    return this.currentTraceId;
  }

  end(): void {
    this.currentTraceId = null;
  }

  get(): string {
    return this.currentTraceId || generateUUID();
  }

  isActive(): boolean {
    return this.currentTraceId !== null;
  }
}

export const traceManager = new TraceManager();

let isRefreshing = false;
let refreshPromise: Promise<boolean> | null = null;

async function refreshToken(): Promise<boolean> {
  const refreshTokenValue = localStorage.getItem("refreshToken");
  if (!refreshTokenValue) {
    return false;
  }

  try {
    const response = await fetch(`${API_BASE}/auth/refresh`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh_token: refreshTokenValue }),
    });

    if (!response.ok) {
      return false;
    }

    const data = (await response.json()) as ApiResponse<{
      access_token: string;
      refresh_token: string;
    }>;

    if (data.success && data.data) {
      localStorage.setItem("token", data.data.access_token);
      localStorage.setItem("refreshToken", data.data.refresh_token);
      return true;
    }
    return false;
  } catch {
    return false;
  }
}

async function handleTokenRefresh(): Promise<boolean> {
  if (isRefreshing) {
    return refreshPromise || Promise.resolve(false);
  }

  isRefreshing = true;
  refreshPromise = refreshToken().finally(() => {
    isRefreshing = false;
    refreshPromise = null;
  });

  return refreshPromise;
}

function clearAuthState(): void {
  localStorage.removeItem("token");
  localStorage.removeItem("refreshToken");
  sessionStorage.removeItem("sessionToken");
  window.dispatchEvent(new CustomEvent("auth:logout"));
}

class HttpClient {
  private getToken(): string | null {
    return (
      localStorage.getItem("admin_token") ||
      localStorage.getItem("token") ||
      sessionStorage.getItem("sessionToken")
    );
  }

  private getSessionToken(): string | null {
    return sessionStorage.getItem("sessionToken");
  }

  private beforeRequest(
    url: string,
    config: RequestConfig
  ): { config: RequestConfig; traceId: string; requestId: string } {
    const token = this.getToken();
    const sessionToken = this.getSessionToken();
    const traceId = config.traceId || traceManager.get();
    const requestId = generateUUID();
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
      "X-Trace-Id": traceId,
      "X-Request-Id": requestId,
      ...config.headers,
    };

    if (!config.skipAuth) {
      if (token) {
        headers["Authorization"] = `Bearer ${token}`;
      }
      if (sessionToken) {
        headers["X-Session-Token"] = sessionToken;
      }
    }

    logger.debug(`[HTTP] --> ${config.method || "GET"} ${url}`, {
      traceId,
      requestId,
      body: config.body as Record<string, unknown>,
    });

    return { config: { ...config, headers }, traceId, requestId };
  }

  private async afterResponse<T>(
    url: string,
    res: Response,
    startTime: number,
    traceId: string,
    requestId: string
  ): Promise<T> {
    const duration = Date.now() - startTime;
    const body = (await res.json().catch(() => null)) as ApiResponse<T> | null;

    logger.debug(`[HTTP] <-- ${res.status} ${url} ${duration}ms`, {
      traceId,
      requestId,
    });

    if (!res.ok) {
      const error = ApiError.fromResponse(res, body || undefined);
      logger.error(`[HTTP] Error: ${error.message}`, {
        traceId,
        requestId,
        url,
        status: res.status,
        code: error.code,
      });
      throw error;
    }

    if (body && !body.success) {
      const error = new ApiError(
        "SERVER_ERROR",
        body.error?.message || "Request failed",
        res.status,
        body.error?.details
      );
      throw error;
    }

    const data = body?.data ?? body;
    return transformKeys(data, snakeToCamel) as T;
  }

  async request<T>(
    endpoint: string,
    config: RequestConfig = {},
    retryCount = 0
  ): Promise<T> {
    const url = `${API_BASE}${endpoint}`;
    const startTime = Date.now();
    const {
      config: finalConfig,
      traceId,
      requestId,
    } = this.beforeRequest(url, config);

    const controller = new AbortController();
    const timeoutId = setTimeout(
      () => controller.abort(),
      config.timeout || DEFAULT_TIMEOUT
    );

    try {
      const res = await fetch(url, {
        method: finalConfig.method || "GET",
        headers: finalConfig.headers,
        body: finalConfig.body
          ? JSON.stringify(transformKeys(finalConfig.body, camelToSnake))
          : undefined,
        signal: controller.signal,
      });

      clearTimeout(timeoutId);

      if (res.status === 401 && !config.skipAuth && retryCount === 0) {
        const refreshed = await handleTokenRefresh();
        if (refreshed) {
          return this.request<T>(endpoint, config, retryCount + 1);
        } else {
          clearAuthState();
          throw new ApiError(
            "UNAUTHORIZED",
            "Session expired, please login again"
          );
        }
      }

      return await this.afterResponse<T>(
        url,
        res,
        startTime,
        traceId,
        requestId
      );
    } catch (error) {
      clearTimeout(timeoutId);

      if (error instanceof ApiError) {
        throw error;
      }

      if (error instanceof Error && error.name === "AbortError") {
        throw new ApiError("TIMEOUT", "Request timeout");
      }

      logger.error(`[HTTP] Network error: ${url}`, {
        traceId,
        requestId,
        error: error instanceof Error ? error.message : "Unknown",
      });
      throw new ApiError("NETWORK_ERROR", "Network error");
    }
  }

  get<T>(endpoint: string, config?: Omit<RequestConfig, "method" | "body">) {
    return this.request<T>(endpoint, { ...config, method: "GET" });
  }

  post<T>(
    endpoint: string,
    body?: unknown,
    config?: Omit<RequestConfig, "method">
  ) {
    return this.request<T>(endpoint, { ...config, method: "POST", body });
  }

  put<T>(
    endpoint: string,
    body?: unknown,
    config?: Omit<RequestConfig, "method">
  ) {
    return this.request<T>(endpoint, { ...config, method: "PUT", body });
  }

  delete<T>(endpoint: string, config?: Omit<RequestConfig, "method" | "body">) {
    return this.request<T>(endpoint, { ...config, method: "DELETE" });
  }
}

export const http = new HttpClient();
