// Admin 数据源列表组件
import type { DataSource } from "@/common/types";
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import { AdminDataSourceCard } from "./AdminDataSourceCard";
import { AdminLoadMoreIndicator } from "./AdminLoadMoreIndicator";

interface AdminDataSourcesListProps {
  sources: DataSource[];
  isLoading: boolean;
  hasMore: boolean;
  total: number;
  loadMoreRef: (node: HTMLDivElement | null) => void;
  onSelect: (source: DataSource) => void;
  onRefresh: (id: string) => void;
  onDelete: (id: string) => void;
}

export function AdminDataSourcesList({
  sources,
  isLoading,
  hasMore,
  total,
  loadMoreRef,
  onSelect,
  onRefresh,
  onDelete,
}: AdminDataSourcesListProps) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  if (isLoading && sources.length === 0) {
    return (
      <div className="flex items-center justify-center h-64 text-muted-foreground">
        {t.loading}
      </div>
    );
  }

  return (
    <>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {sources.map((source) => (
          <AdminDataSourceCard
            key={source.id}
            source={source}
            onClick={() => onSelect(source)}
            onRefresh={() => onRefresh(source.id)}
            onDelete={() => onDelete(source.id)}
          />
        ))}
      </div>
      <AdminLoadMoreIndicator
        loadMoreRef={loadMoreRef}
        hasMore={hasMore}
        isLoading={isLoading}
        total={total}
        count={sources.length}
      />
    </>
  );
}
