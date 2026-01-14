// Admin 订阅计划管理页面
import { useSubscriptions } from "../hooks/useSubscriptions";
import { AdminSubscriptionsHeader } from "../components/AdminSubscriptionsHeader";
import { AdminSubscriptionsList } from "../components/AdminSubscriptionsList";
import { AdminSubscriptionFormDialog } from "../components/AdminSubscriptionFormDialog";

export default function SubscriptionsView() {
  const {
    subscriptions,
    isLoading,
    showForm,
    editingPlan,
    formData,
    setFormData,
    handleCreate,
    handleEdit,
    handleSubmit,
    handleDelete,
    handleCloseForm,
  } = useSubscriptions();

  return (
    <>
      <AdminSubscriptionsHeader onCreate={handleCreate} />

      <AdminSubscriptionsList
        subscriptions={subscriptions}
        isLoading={isLoading}
        onEdit={handleEdit}
        onDelete={handleDelete}
      />

      <AdminSubscriptionFormDialog
        open={showForm}
        editingPlan={editingPlan}
        formData={formData}
        onFormDataChange={setFormData}
        onSubmit={handleSubmit}
        onClose={handleCloseForm}
      />
    </>
  );
}
