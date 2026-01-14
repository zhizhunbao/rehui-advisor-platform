// Admin 系统配置管理页面
import { useConfigs } from "../hooks/useConfigs";
import { AdminConfigsHeader } from "../components/AdminConfigsHeader";
import { AdminConfigsFilter } from "../components/AdminConfigsFilter";
import { AdminConfigsTable } from "../components/AdminConfigsTable";
import { AdminConfigFormDialog } from "../components/AdminConfigFormDialog";
import { AdminViewContainer } from "../components/AdminViewLayout";

export default function ConfigView() {
  const {
    configs,
    isLoading,
    categoryFilter,
    setCategoryFilter,
    showForm,
    editingConfig,
    formData,
    setFormData,
    handleEdit,
    handleCreate,
    handleSubmit,
    handleDelete,
    handleCloseForm,
    getCategoryLabel,
  } = useConfigs();

  return (
    <AdminViewContainer>
      <AdminConfigsHeader onCreate={handleCreate} />

      <AdminConfigsFilter
        categoryFilter={categoryFilter}
        onCategoryFilterChange={setCategoryFilter}
        getCategoryLabel={getCategoryLabel}
      />

      <AdminConfigsTable
        configs={configs}
        isLoading={isLoading}
        onEdit={handleEdit}
        onDelete={handleDelete}
        getCategoryLabel={getCategoryLabel}
      />

      <AdminConfigFormDialog
        open={showForm}
        editingConfig={editingConfig}
        formData={formData}
        onFormDataChange={setFormData}
        onSubmit={handleSubmit}
        onClose={handleCloseForm}
        getCategoryLabel={getCategoryLabel}
      />
    </AdminViewContainer>
  );
}
