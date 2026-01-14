// Admin 推荐管理页面
import { useRecommendations } from "../hooks/useRecommendations";
import { AdminRecommendationsHeader } from "../components/AdminRecommendationsHeader";
import { AdminRecommendationsFilter } from "../components/AdminRecommendationsFilter";
import { AdminRecommendationsTable } from "../components/AdminRecommendationsTable";

export default function RecommendationsView() {
  const {
    recommendations,
    isLoading,
    hasMore,
    total,
    loadMoreRef,
    statusFilter,
    setStatusFilter,
    handleStatusChange,
    handleDelete,
    getStatusLabel,
    getStatusVariant,
  } = useRecommendations();

  return (
    <>
      <AdminRecommendationsHeader />

      <AdminRecommendationsFilter
        statusFilter={statusFilter}
        onStatusFilterChange={setStatusFilter}
      />

      <AdminRecommendationsTable
        recommendations={recommendations}
        isLoading={isLoading}
        hasMore={hasMore}
        total={total}
        loadMoreRef={loadMoreRef}
        onStatusChange={handleStatusChange}
        onDelete={handleDelete}
        getStatusLabel={getStatusLabel}
        getStatusVariant={getStatusVariant}
      />
    </>
  );
}
