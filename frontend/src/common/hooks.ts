// common/hooks.ts - 通用 Hooks
import { useState, useEffect, useRef, useCallback } from "react";

// ==================== useInfiniteScroll ====================
interface UseInfiniteScrollOptions<T> {
  fetchFn: (page: number) => Promise<{ data: T[]; total: number }>;
  limit?: number;
  enabled?: boolean;
}

interface UseInfiniteScrollReturn<T> {
  data: T[];
  isLoading: boolean;
  hasMore: boolean;
  total: number;
  loadMoreRef: (node: HTMLDivElement | null) => void;
  reset: () => void;
  refresh: () => void;
}

export function useInfiniteScroll<T>({
  fetchFn,
  limit = 20,
  enabled = true,
}: UseInfiniteScrollOptions<T>): UseInfiniteScrollReturn<T> {
  const [data, setData] = useState<T[]>([]);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [hasMore, setHasMore] = useState(true);
  const observerRef = useRef<IntersectionObserver | null>(null);
  const isLoadingRef = useRef(false);
  const nodeRef = useRef<HTMLDivElement | null>(null);

  const loadPage = useCallback(
    async (pageNum: number, append: boolean = false) => {
      if (isLoadingRef.current) return;
      isLoadingRef.current = true;
      setIsLoading(true);

      try {
        const result = await fetchFn(pageNum);
        const newData = result.data;
        const totalCount = result.total;

        setData((prev) => (append ? [...prev, ...newData] : newData));
        setTotal(totalCount);
        setPage(pageNum);
        setHasMore(pageNum * limit < totalCount);
      } catch (err) {
        console.error("Failed to fetch:", err);
      } finally {
        setIsLoading(false);
        isLoadingRef.current = false;
      }
    },
    [fetchFn, limit]
  );

  useEffect(() => {
    if (enabled) {
      setData([]);
      setPage(1);
      setHasMore(true);
      loadPage(1, false);
    }
  }, [enabled, loadPage]);

  const loadMoreRef = useCallback(
    (node: HTMLDivElement | null) => {
      if (!enabled) return;

      if (observerRef.current) {
        observerRef.current.disconnect();
      }

      nodeRef.current = node;

      if (!node) return;

      observerRef.current = new IntersectionObserver(
        (entries) => {
          if (entries[0].isIntersecting && hasMore && !isLoadingRef.current) {
            loadPage(page + 1, true);
          }
        },
        { rootMargin: "200px" }
      );

      observerRef.current.observe(node);
    },
    [enabled, hasMore, page, loadPage]
  );

  useEffect(() => {
    return () => {
      observerRef.current?.disconnect();
    };
  }, []);

  const reset = useCallback(() => {
    setData([]);
    setPage(1);
    setHasMore(true);
  }, []);

  const refresh = useCallback(() => {
    reset();
    loadPage(1, false);
  }, [reset, loadPage]);

  return { data, isLoading, hasMore, total, loadMoreRef, reset, refresh };
}

// ==================== useIsMobile ====================
const MOBILE_BREAKPOINT = 768;

export function useIsMobile() {
  const [isMobile, setIsMobile] = useState<boolean | undefined>(undefined);

  useEffect(() => {
    const mql = window.matchMedia(`(max-width: ${MOBILE_BREAKPOINT - 1}px)`);
    const onChange = () => {
      setIsMobile(window.innerWidth < MOBILE_BREAKPOINT);
    };
    mql.addEventListener("change", onChange);
    setIsMobile(window.innerWidth < MOBILE_BREAKPOINT);
    return () => mql.removeEventListener("change", onChange);
  }, []);

  return !!isMobile;
}
