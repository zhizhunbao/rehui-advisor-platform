// common/ErrorBoundary.tsx
import { Component, ReactNode, ErrorInfo } from "react";
import { logger } from "./logger";

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
  onError?: (error: Error, errorInfo: ErrorInfo) => void;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    logger.error("[ErrorBoundary] Caught error", {
      error: error.message,
      stack: error.stack,
      componentStack: errorInfo.componentStack || undefined,
    });

    this.props.onError?.(error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        this.props.fallback || (
          <div className="flex flex-col items-center justify-center h-full p-8">
            <h2 className="text-xl font-bold text-red-500 mb-4">出错了</h2>
            <p className="text-gray-500 mb-4">{this.state.error?.message}</p>
            <button
              onClick={() => this.setState({ hasError: false, error: null })}
              className="px-4 py-2 bg-blue-500 text-white rounded"
            >
              重试
            </button>
          </div>
        )
      );
    }

    return this.props.children;
  }
}
