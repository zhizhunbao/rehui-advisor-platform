// Admin 检索引擎管理页面
import { useRetrieval } from "../hooks/useRetrieval";
import { AdminRetrievalStats } from "../components/AdminRetrievalStats";
import { AdminRetrievalHeader } from "../components/AdminRetrievalHeader";
import { AdminRetrievalFilter } from "../components/AdminRetrievalFilter";
import { AdminRetrievalList } from "../components/AdminRetrievalList";
import { AdminRetrievalFormDialog } from "../components/AdminRetrievalFormDialog";
import { AdminRetrievalTestPanel } from "../components/AdminRetrievalTestPanel";
import { AdminRetrievalDeleteDialog } from "../components/AdminRetrievalDeleteDialog";

export default function RetrievalView() {
  const {
    engines,
    engineTypes,
    loading,
    testing,
    testResult,
    filteredEngines,
    activeEngines,
    defaultEngine,
    filterType,
    setFilterType,
    filterStatus,
    setFilterStatus,
    showEngineDialog,
    setShowEngineDialog,
    editingEngine,
    engineForm,
    setEngineForm,
    configJson,
    setConfigJson,
    deleteTarget,
    setDeleteTarget,
    showTestDialog,
    setShowTestDialog,
    testEngineId,
    setTestEngineId,
    testQuery,
    setTestQuery,
    handleCreateEngine,
    handleEditEngine,
    handleSaveEngine,
    handleDeleteEngine,
    handleSetDefault,
    handleTest,
    resetFilters,
  } = useRetrieval();

  return (
    <>
      <AdminRetrievalStats
        engines={engines}
        activeCount={activeEngines}
        defaultEngine={defaultEngine}
      />

      <AdminRetrievalHeader
        onTest={() => setShowTestDialog(true)}
        onCreate={handleCreateEngine}
      />

      <AdminRetrievalFilter
        engines={engines}
        filterType={filterType}
        onFilterTypeChange={setFilterType}
        filterStatus={filterStatus}
        onFilterStatusChange={setFilterStatus}
        onReset={resetFilters}
      />

      <AdminRetrievalList
        engines={filteredEngines}
        isLoading={loading}
        onEdit={handleEditEngine}
        onSetDefault={handleSetDefault}
        onDelete={setDeleteTarget}
      />

      <AdminRetrievalFormDialog
        open={showEngineDialog}
        onOpenChange={setShowEngineDialog}
        editingEngine={editingEngine}
        engineTypes={engineTypes}
        engineForm={engineForm}
        onEngineFormChange={setEngineForm}
        configJson={configJson}
        onConfigJsonChange={setConfigJson}
        onSave={handleSaveEngine}
      />

      <AdminRetrievalTestPanel
        open={showTestDialog}
        onOpenChange={setShowTestDialog}
        engines={engines}
        testEngineId={testEngineId}
        onTestEngineIdChange={setTestEngineId}
        testQuery={testQuery}
        onTestQueryChange={setTestQuery}
        isTesting={testing}
        testResult={testResult}
        onTest={handleTest}
      />

      <AdminRetrievalDeleteDialog
        deleteTarget={deleteTarget}
        onOpenChange={() => setDeleteTarget(null)}
        onConfirm={handleDeleteEngine}
      />
    </>
  );
}
