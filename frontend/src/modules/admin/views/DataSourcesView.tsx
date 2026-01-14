// Admin 数据源管理页面
import { useDataSources } from "../hooks/useDataSources";
import { AdminDataSourcesHeader } from "../components/AdminDataSourcesHeader";
import { AdminDataSourcesStats } from "../components/AdminDataSourcesStats";
import { AdminDataSourcesFilter } from "../components/AdminDataSourcesFilter";
import { AdminDataSourcesList } from "../components/AdminDataSourcesList";
import {
  AdminSourceDetailModal,
  AdminAddSourceModal,
} from "../components/AdminDataSourceModals";

export default function DataSourcesView() {
  const {
    sources,
    stats,
    categories,
    domains,
    types,
    statuses,
    languages,
    isLoading,
    hasMore,
    total,
    loadMoreRef,
    search,
    setSearch,
    categoryId,
    setCategoryId,
    domainId,
    setDomainId,
    status,
    setStatus,
    type,
    setType,
    language,
    setLanguage,
    refresh,
    handleRefresh,
    handleDelete,
    handleRefreshAll,
    handleReset,
    fetchDomainsByCategory,
    selectedSource,
    setSelectedSource,
    showAddModal,
    setShowAddModal,
  } = useDataSources();

  const onCategoryChange = (val: string) => {
    setCategoryId(val);
    fetchDomainsByCategory(val);
  };

  return (
    <>
      <AdminDataSourcesHeader
        onRefreshAll={handleRefreshAll}
        onAdd={() => setShowAddModal(true)}
      />

      <AdminDataSourcesStats stats={stats} />

      <AdminDataSourcesFilter
        search={search}
        onSearchChange={setSearch}
        type={type}
        onTypeChange={setType}
        categoryId={categoryId}
        onCategoryChange={onCategoryChange}
        domainId={domainId}
        onDomainChange={setDomainId}
        status={status}
        onStatusChange={setStatus}
        language={language}
        onLanguageChange={setLanguage}
        types={types}
        categories={categories}
        domains={domains}
        statuses={statuses}
        languages={languages}
        onReset={handleReset}
      />

      <AdminDataSourcesList
        sources={sources}
        isLoading={isLoading}
        hasMore={hasMore}
        total={total}
        loadMoreRef={loadMoreRef}
        onSelect={setSelectedSource}
        onRefresh={handleRefresh}
        onDelete={handleDelete}
      />

      {selectedSource && (
        <AdminSourceDetailModal
          source={selectedSource}
          onClose={() => setSelectedSource(null)}
          onRefresh={() => {
            handleRefresh(selectedSource.id);
            setSelectedSource(null);
          }}
        />
      )}

      {showAddModal && (
        <AdminAddSourceModal
          categories={categories}
          isLoading={false}
          onClose={() => setShowAddModal(false)}
          onSubmit={async () => {
            setShowAddModal(false);
            refresh();
          }}
        />
      )}
    </>
  );
}
