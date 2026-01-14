// Admin Agent 框架管理页面
import { useAgentFrameworks } from "../hooks/useAgentFrameworks";
import { AdminAgentFrameworksHeader } from "../components/AdminAgentFrameworksHeader";
import { AdminAgentFrameworksStats } from "../components/AdminAgentFrameworksStats";
import { AdminAgentFrameworksFilter } from "../components/AdminAgentFrameworksFilter";
import { AdminAgentFrameworksList } from "../components/AdminAgentFrameworksList";
import { AdminAgentFrameworkDetailDialog } from "../components/AdminAgentFrameworkDetailDialog";
import { AdminAgentFrameworkAddDialog } from "../components/AdminAgentFrameworkAddDialog";

export default function AgentFrameworksView() {
  const {
    filteredFrameworks,
    isLoading,
    search,
    setSearch,
    selectedFramework,
    setSelectedFramework,
    showAddModal,
    setShowAddModal,
    stats,
    handleRefresh,
    handleDelete,
    handleCreate,
    handleRefreshSelected,
  } = useAgentFrameworks();

  return (
    <>
      <AdminAgentFrameworksHeader onCreate={() => setShowAddModal(true)} />

      <AdminAgentFrameworksStats stats={stats} />

      <AdminAgentFrameworksFilter search={search} onSearchChange={setSearch} />

      <AdminAgentFrameworksList
        frameworks={filteredFrameworks}
        isLoading={isLoading}
        onSelect={setSelectedFramework}
        onRefresh={handleRefresh}
        onDelete={handleDelete}
      />

      <AdminAgentFrameworkDetailDialog
        framework={selectedFramework}
        onClose={() => setSelectedFramework(null)}
        onRefresh={handleRefreshSelected}
      />

      <AdminAgentFrameworkAddDialog
        open={showAddModal}
        onClose={() => setShowAddModal(false)}
        onSubmit={handleCreate}
      />
    </>
  );
}
