// Admin 加载更多指示器组件 - Props: loadMoreRef, hasMore, isLoading, total, count, lang
import { adminLocales } from "@/common/i18n";
import type { Language } from "@/common/types";

interface AdminLoadMoreIndicatorProps {
  loadMoreRef: (node: HTMLDivElement | null) => void;
  hasMore: boolean;
  isLoading: boolean;
  total: number;
  count: number;
  lang: Language;
}

export function AdminLoadMoreIndicator({
  loadMoreRef,
  hasMore,
  isLoading,
  total,
  count,
  lang,
}: AdminLoadMoreIndicatorProps) {
  const t = adminLocales[lang];

  if (!hasMore && count > 0) {
    return (
      <div className="text-center text-muted-foreground py-6">
        {t.totalCount.replace("{count}", String(total))}
      </div>
    );
  }

  if (!hasMore) return null;

  return (
    <div ref={loadMoreRef} className="flex items-center justify-center py-8">
      <span className="text-muted-foreground">
        {isLoading ? t.loading : t.scrollToLoadMore}
      </span>
    </div>
  );
}
