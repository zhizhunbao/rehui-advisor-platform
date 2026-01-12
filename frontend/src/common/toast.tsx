// common/toast.tsx - Toast 通知相关
import {
  createContext,
  useContext,
  useState,
  useCallback,
  type ReactNode,
} from "react";
import { ApiError, logger } from "./logger";

// ==================== Toast Context ====================
type ToastType = "success" | "error" | "warning" | "info";

interface Toast {
  id: string;
  type: ToastType;
  message: string;
}

interface ToastContextValue {
  toasts: Toast[];
  showToast: (type: ToastType, message: string) => void;
  hideToast: (id: string) => void;
}

const ToastContext = createContext<ToastContextValue | null>(null);

export function ToastProvider({ children }: { children: ReactNode }) {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const showToast = useCallback((type: ToastType, message: string) => {
    const id = Date.now().toString();
    setToasts((prev) => [...prev, { id, type, message }]);

    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, 3000);
  }, []);

  const hideToast = useCallback((id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  return (
    <ToastContext.Provider value={{ toasts, showToast, hideToast }}>
      {children}
      <div className="fixed top-4 right-4 z-50 space-y-2">
        {toasts.map((toast) => (
          <div
            key={toast.id}
            className={`px-4 py-3 rounded-lg shadow-lg text-white ${
              toast.type === "success"
                ? "bg-green-500"
                : toast.type === "error"
                ? "bg-red-500"
                : toast.type === "warning"
                ? "bg-yellow-500"
                : "bg-blue-500"
            }`}
          >
            {toast.message}
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
}

export function useToast() {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error("useToast must be used within ToastProvider");
  }
  return context;
}

// ==================== Error Handler Hook ====================
export function useErrorHandler() {
  const { showToast } = useToast();

  const handleError = useCallback(
    (error: unknown, context?: string) => {
      const prefix = context ? `[${context}] ` : "";

      if (error instanceof ApiError) {
        logger.warn(`${prefix}API Error: ${error.code}`, {
          message: error.message,
          status: error.statusCode,
        });

        if (error.code === "UNAUTHORIZED") {
          localStorage.removeItem("token");
          window.location.href = "/login";
          return;
        }

        showToast("error", error.message);
        return;
      }

      if (error instanceof Error) {
        logger.error(`${prefix}Error: ${error.message}`, {
          stack: error.stack,
        });
        showToast("error", error.message);
        return;
      }

      logger.error(`${prefix}Unknown error`, { error: String(error) });
      showToast("error", "发生未知错误");
    },
    [showToast]
  );

  return { handleError };
}
