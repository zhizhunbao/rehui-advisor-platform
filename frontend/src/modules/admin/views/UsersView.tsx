// Admin 用户管理页面
import type { Language } from "@/common/types";
import { useUsers } from "../hooks/useUsers";
import { AdminUsersHeader } from "../components/AdminUsersHeader";
import { AdminUsersFilter } from "../components/AdminUsersFilter";
import { AdminUsersTable } from "../components/AdminUsersTable";

export default function UsersView({ lang }: { lang: Language }) {
  const {
    users,
    isLoading,
    hasMore,
    total,
    loadMoreRef,
    search,
    setSearch,
    statusFilter,
    setStatusFilter,
    handleToggleStatus,
    handleSearch,
    getUserTypeLabel,
    getStatusLabel,
    getStatusVariant,
  } = useUsers(lang);

  return (
    <div>
      <AdminUsersHeader lang={lang} />

      <AdminUsersFilter
        lang={lang}
        search={search}
        statusFilter={statusFilter}
        onSearchChange={setSearch}
        onStatusChange={setStatusFilter}
        onSearch={handleSearch}
      />

      <AdminUsersTable
        lang={lang}
        users={users}
        isLoading={isLoading}
        hasMore={hasMore}
        total={total}
        loadMoreRef={loadMoreRef}
        onToggleStatus={handleToggleStatus}
        getUserTypeLabel={getUserTypeLabel}
        getStatusLabel={getStatusLabel}
        getStatusVariant={getStatusVariant}
      />
    </div>
  );
}
