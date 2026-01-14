// Admin LLM 模型管理页面
import { useLLM } from "../hooks/useLLM";
import { AdminLLMHeader } from "../components/AdminLLMHeader";
import { AdminLLMStats } from "../components/AdminLLMStats";
import { AdminLLMFilter } from "../components/AdminLLMFilter";
import { AdminLLMTable } from "../components/AdminLLMTable";
import { AdminLLMFormDialog } from "../components/AdminLLMFormDialog";
import { AdminLLMDeleteDialog } from "../components/AdminLLMDeleteDialog";
import { AdminLLMSyncResult } from "../components/AdminLLMSyncResult";

export default function LLMView() {
  const {
    groupedModels,
    sortedGroups,
    syncSources,
    loading,
    syncing,
    syncResult,
    stats,
    filterCounts,
    searchQuery,
    setSearchQuery,
    filterProvider,
    setFilterProvider,
    filterCategory,
    setFilterCategory,
    filterDeployment,
    setFilterDeployment,
    filterInputPrice,
    setFilterInputPrice,
    filterOutputPrice,
    setFilterOutputPrice,
    filterContext,
    setFilterContext,
    collapsedGroups,
    toggleGroup,
    hasFilters,
    handleReset,
    normalizeProvider,
    getProviderLabel,
    getCategoryLabel,
    sync,
    showDialog,
    deleteTarget,
    initialForm,
    editingModel,
    handleCreate,
    handleEdit,
    handleSave,
    handleCloseDialog,
    handleSetDeleteTarget,
    handleClearDeleteTarget,
    handleDelete,
  } = useLLM();

  return (
    <>
      <AdminLLMStats stats={stats} />

      <AdminLLMHeader
        isSyncing={syncing}
        onSync={() => sync()}
        onCreate={handleCreate}
      />

      <AdminLLMFilter
        searchQuery={searchQuery}
        filterProvider={filterProvider}
        filterCategory={filterCategory}
        filterDeployment={filterDeployment}
        filterInputPrice={filterInputPrice}
        filterOutputPrice={filterOutputPrice}
        filterContext={filterContext}
        providerCounts={filterCounts.providerCounts}
        categoryCounts={filterCounts.categoryCounts}
        deploymentCounts={filterCounts.deploymentCounts}
        inputPriceCounts={filterCounts.inputPriceCounts}
        outputPriceCounts={filterCounts.outputPriceCounts}
        contextCounts={filterCounts.contextCounts}
        hasFilters={!!hasFilters}
        onSearchChange={setSearchQuery}
        onProviderChange={setFilterProvider}
        onCategoryChange={setFilterCategory}
        onDeploymentChange={setFilterDeployment}
        onInputPriceChange={setFilterInputPrice}
        onOutputPriceChange={setFilterOutputPrice}
        onContextChange={setFilterContext}
        onReset={handleReset}
      />

      <AdminLLMSyncResult syncResult={syncResult} syncSources={syncSources} />

      <AdminLLMTable
        groupedModels={groupedModels}
        sortedGroups={sortedGroups}
        collapsedGroups={collapsedGroups}
        isLoading={loading}
        onToggleGroup={toggleGroup}
        onEdit={handleEdit}
        onDelete={handleSetDeleteTarget}
        getProviderLabel={getProviderLabel}
        getCategoryLabel={getCategoryLabel}
        normalizeProvider={normalizeProvider}
      />

      <AdminLLMFormDialog
        open={showDialog}
        isEditing={!!editingModel}
        initialForm={initialForm}
        onClose={handleCloseDialog}
        onSave={handleSave}
      />

      <AdminLLMDeleteDialog
        deleteTarget={deleteTarget}
        onOpenChange={handleClearDeleteTarget}
        onConfirm={handleDelete}
      />
    </>
  );
}
