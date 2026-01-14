// Admin 调度任务管理页面
import { useScheduler } from "../hooks/useScheduler";
import { AdminSchedulerHeader } from "../components/AdminSchedulerHeader";
import { AdminSchedulerFilter } from "../components/AdminSchedulerFilter";
import { AdminSchedulerList } from "../components/AdminSchedulerList";
import { AdminSchedulerFormDialog } from "../components/AdminSchedulerFormDialog";

export default function SchedulerView() {
  const {
    jobs,
    jobTypes,
    isLoading,
    executionsMap,
    isLoadingHistory,
    showJobModal,
    isSubmitting,
    selectedJob,
    expandedJobId,
    filterType,
    setFilterType,
    collapsedGroups,
    formData,
    setFormData,
    handleCreate,
    handleEdit,
    handleSave,
    handleDelete,
    handleToggle,
    handleTrigger,
    handleViewHistory,
    toggleGroup,
    handleCloseModal,
  } = useScheduler();

  return (
    <>
      <AdminSchedulerHeader onCreate={handleCreate} />

      <AdminSchedulerFilter
        jobs={jobs}
        jobTypes={jobTypes}
        filterType={filterType}
        onFilterTypeChange={setFilterType}
      />

      <AdminSchedulerList
        jobs={jobs}
        jobTypes={jobTypes}
        isLoading={isLoading}
        expandedJobId={expandedJobId}
        executionsMap={executionsMap}
        isLoadingHistory={isLoadingHistory}
        collapsedGroups={collapsedGroups}
        onViewHistory={handleViewHistory}
        onToggle={handleToggle}
        onTrigger={handleTrigger}
        onEdit={handleEdit}
        onDelete={handleDelete}
        onToggleGroup={toggleGroup}
      />

      <AdminSchedulerFormDialog
        open={showJobModal}
        selectedJob={selectedJob}
        jobTypes={jobTypes}
        formData={formData}
        isSubmitting={isSubmitting}
        onFormDataChange={setFormData}
        onSave={handleSave}
        onClose={handleCloseModal}
      />
    </>
  );
}
