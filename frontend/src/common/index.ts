// Common Module - 通用基础设施
export { ErrorBoundary } from "./ErrorBoundary";
export { ToastProvider, useToast, useErrorHandler } from "./toast";
export { useInfiniteScroll, useIsMobile } from "./hooks";
export { http, traceManager } from "./http";
export {
  logger,
  ApiError,
  initGlobalErrorHandler,
  type ApiErrorCode,
  type LogMeta,
} from "./logger";
export {
  themes,
  applyTheme,
  getStoredTheme,
  type ThemeName,
  type Theme,
} from "./themes";
export {
  locales,
  useI18n,
  common,
  adminLocales,
  advisorLocales,
  authLocales,
  type Language,
} from "./i18n";
