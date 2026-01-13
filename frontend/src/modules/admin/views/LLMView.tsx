// Admin LLM 模型管理页面
import { useState, useMemo } from "react";
import type { Language, LLMModel, LLMModelCreate } from "@/common/types";
import { adminLocales } from "@/common/i18n";
import { useLLM } from "../hooks/useLLM";
import { AdminLLMHeader } from "../components/AdminLLMHeader";
import { AdminLLMStats } from "../components/AdminLLMStats";
import { AdminLLMFilter } from "../components/AdminLLMFilter";
import { AdminLLMTable } from "../components/AdminLLMTable";
import { AdminLLMFormDialog } from "../components/AdminLLMFormDialog";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/libs/shadcn/ui/alert-dialog";

export default function LLMView({ lang }: { lang: Language }) {
  const t = adminLocales[lang];
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
    getModelForm,
    create,
    update,
    remove,
    sync,
  } = useLLM(lang);

  const [showDialog, setShowDialog] = useState(false);
  const [editingModel, setEditingModel] = useState<LLMModel | null>(null);
  const [deleteTarget, setDeleteTarget] = useState<{
    id: string;
    name: string;
  } | null>(null);

  const initialForm = useMemo(
    () => getModelForm(editingModel),
    [editingModel, getModelForm]
  );

  const handleCreate = () => {
    setEditingModel(null);
    setShowDialog(true);
  };

  const handleEdit = (model: LLMModel) => {
    setEditingModel(model);
    setShowDialog(true);
  };

  const handleSave = async (data: LLMModelCreate) => {
    if (editingModel) {
      await update(editingModel.id, data);
    } else {
      await create(data);
    }
  };

  const handleDelete = async () => {
    if (!deleteTarget) return;
    await remove(deleteTarget.id);
    setDeleteTarget(null);
  };

  return (
    <div>
      <AdminLLMStats lang={lang} stats={stats} />

      <AdminLLMHeader
        lang={lang}
        isSyncing={syncing}
        onSync={() => sync()}
        onCreate={handleCreate}
      />

      <AdminLLMFilter
        lang={lang}
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

      {syncResult && (
        <div
          className={`p-4 rounded-lg ${
            syncResult.errors.length > 0
              ? "bg-amber-50 dark:bg-amber-950"
              : "bg-green-50 dark:bg-green-950"
          }`}
        >
          <div className="font-medium">
            {t.syncComplete}: {syncResult.synced}
          </div>
          {syncResult.errors.length > 0 && (
            <div className="text-sm text-muted-foreground mt-1">
              {t.error}: {syncResult.errors.map((e) => e.error).join(", ")}
            </div>
          )}
        </div>
      )}

      {syncSources.length > 0 && (
        <div className="text-sm text-muted-foreground">
          {t.syncSources}: {syncSources.map((s) => s.name).join(", ")}
        </div>
      )}

      <AdminLLMTable
        lang={lang}
        groupedModels={groupedModels}
        sortedGroups={sortedGroups}
        collapsedGroups={collapsedGroups}
        isLoading={loading}
        onToggleGroup={toggleGroup}
        onEdit={handleEdit}
        onDelete={(model) =>
          setDeleteTarget({ id: model.id, name: model.displayName })
        }
        getProviderLabel={getProviderLabel}
        getCategoryLabel={getCategoryLabel}
        normalizeProvider={normalizeProvider}
      />

      <AdminLLMFormDialog
        lang={lang}
        open={showDialog}
        isEditing={!!editingModel}
        initialForm={initialForm}
        onClose={() => setShowDialog(false)}
        onSave={handleSave}
      />

      <AlertDialog
        open={!!deleteTarget}
        onOpenChange={() => setDeleteTarget(null)}
      >
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>{t.confirmDelete}</AlertDialogTitle>
            <AlertDialogDescription>
              {t.deleteWarning} ({deleteTarget?.name})
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>{t.cancel}</AlertDialogCancel>
            <AlertDialogAction onClick={handleDelete}>
              {t.delete}
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
}
