// Admin 领域管理页面
import { useDomains } from "../hooks/useDomains";
import { AdminDomainsHeader } from "../components/AdminDomainsHeader";
import { AdminDomainsStats } from "../components/AdminDomainsStats";
import { AdminDomainsFilter } from "../components/AdminDomainsFilter";
import { AdminDomainsList } from "../components/AdminDomainsList";
import { AdminDomainFormDialog } from "../components/AdminDomainFormDialog";

export default function DomainsView() {
  const {
    categories,
    isLoading,
    search,
    setSearch,
    filterCategoryId,
    setFilterCategoryId,
    editingDomain,
    setEditingDomain,
    isCreating,
    setIsCreating,
    isGroupedMode,
    categoryOptions,
    filteredDomains,
    groupedDomains,
    stats,
    getCategoryName,
    handleToggle,
    handleSave,
    handleReset,
    handleCloseDialog,
  } = useDomains();

  return (
    <>
      <AdminDomainsHeader onCreate={() => setIsCreating(true)} />

      <AdminDomainsStats stats={stats} />

      <AdminDomainsFilter
        search={search}
        onSearchChange={setSearch}
        filterCategoryId={filterCategoryId}
        onFilterCategoryIdChange={setFilterCategoryId}
        categoryOptions={categoryOptions}
        onReset={handleReset}
      />

      <AdminDomainsList
        isGroupedMode={isGroupedMode}
        filteredDomains={filteredDomains}
        groupedDomains={groupedDomains}
        isLoading={isLoading}
        getCategoryName={getCategoryName}
        onSelect={setEditingDomain}
        onToggle={handleToggle}
      />

      <AdminDomainFormDialog
        domain={editingDomain}
        categories={categories}
        open={isCreating || !!editingDomain}
        onSave={handleSave}
        onClose={handleCloseDialog}
      />
    </>
  );
}
