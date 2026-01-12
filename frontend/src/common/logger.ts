// common/logger.ts - 前端日志
type LogLevel = "debug" | "info" | "warn" | "error";

export interface LogMeta {
  [key: string]: unknown;
}

const LOG_LEVEL = (import.meta.env.VITE_LOG_LEVEL as LogLevel) || "info";
const IS_DEV = import.meta.env.DEV;
const IS_PROD = import.meta.env.PROD;

const LEVELS: LogLevel[] = ["debug", "info", "warn", "error"];

function shouldLog(level: LogLevel): boolean {
  if (IS_PROD && (level === "debug" || level === "info")) {
    return false;
  }
  return LEVELS.indexOf(level) >= LEVELS.indexOf(LOG_LEVEL);
}

function log(level: LogLevel, message: string, meta?: LogMeta) {
  const methods = {
    debug: console.debug,
    info: console.info,
    warn: console.warn,
    error: console.error,
  };
  if (IS_DEV) {
    methods[level](`[${level.toUpperCase()}] ${message}`, meta || "");
  } else {
    methods[level](message, meta || "");
  }
}

export const logger = {
  debug: (message: string, meta?: LogMeta) =>
    shouldLog("debug") && log("debug", message, meta),
  info: (message: string, meta?: LogMeta) =>
    shouldLog("info") && log("info", message, meta),
  warn: (message: string, meta?: LogMeta) =>
    shouldLog("warn") && log("warn", message, meta),
  error: (message: string, meta?: LogMeta) =>
    shouldLog("error") && log("error", message, meta),
};

// ==================== API Error ====================
export type ApiErrorCode =
  | "NETWORK_ERROR"
  | "TIMEOUT"
  | "UNAUTHORIZED"
  | "FORBIDDEN"
  | "NOT_FOUND"
  | "VALIDATION_ERROR"
  | "SERVER_ERROR"
  | "UNKNOWN";

export class ApiError extends Error {
  code: ApiErrorCode;
  statusCode?: number;
  details?: unknown;

  constructor(
    code: ApiErrorCode,
    message: string,
    statusCode?: number,
    details?: unknown
  ) {
    super(message);
    this.name = "ApiError";
    this.code = code;
    this.statusCode = statusCode;
    this.details = details;
  }

  static fromResponse(
    res: Response,
    body?: { error?: { message?: string; details?: unknown } }
  ): ApiError {
    const code = this.mapStatusToCode(res.status);
    const message = body?.error?.message || res.statusText || "Request failed";
    return new ApiError(code, message, res.status, body?.error?.details);
  }

  private static mapStatusToCode(status: number): ApiErrorCode {
    if (status === 401) return "UNAUTHORIZED";
    if (status === 403) return "FORBIDDEN";
    if (status === 404) return "NOT_FOUND";
    if (status === 400) return "VALIDATION_ERROR";
    if (status >= 500) return "SERVER_ERROR";
    return "UNKNOWN";
  }
}

// ==================== Global Error Handler ====================
export function initGlobalErrorHandler() {
  window.addEventListener("unhandledrejection", (event) => {
    const error = event.reason;
    logger.error("Unhandled Promise rejection", {
      error: error instanceof Error ? error.message : String(error),
      stack: error instanceof Error ? error.stack : undefined,
    });
  });

  window.addEventListener("error", (event) => {
    if (event.target !== window) return;
    logger.error("Uncaught error", {
      file: event.filename?.split("/").pop() || "unknown",
      line: event.lineno || 0,
      error: event.message,
    });
  });
}
