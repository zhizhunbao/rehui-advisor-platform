// Admin 用户管理 Hook
import { useState, useCallback } from "react";
import type { AdminUser, UserListParams, Language } from "@/common/types";
import { adminLocales } from "@/common/i18n";
import { useInfiniteScroll } from "@/common/hooks";
import { userService } from "../services/user.service";

export function useUsers(lang: Language, autoFetch = true) {
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");

  const fetchUsers = useCallback(
    async (page: number) => {
      const params: UserListParams = {
        page,
        limit: 20,
        search: search || undefined,
        status: statusFilter !== "all" ? statusFilter : undefined,
      };
      const res = await userService.getAll(params);
      return { data: res.data || [], total: res.total || 0 };
    },
    [search, statusFilter]
  );

  const {
    data: users,
    isLoading,
    hasMore,
    total,
    loadMoreRef,
    refresh,
  } = useInfiniteScroll<AdminUser>({ fetchFn: fetchUsers, enabled: autoFetch });

  const handleToggleStatus = useCallback(
    async (id: string) => {
      await userService.toggleStatus(id);
      refresh();
    },
    [refresh]
  );

  const handleSearch = useCallback(() => {
    refresh();
  }, [refresh]);

  const handleReset = useCallback(() => {
    setSearch("");
    setStatusFilter("all");
  }, []);

  const getUserTypeLabel = useCallback(
    (type: string) => {
      const t = adminLocales[lang];
      switch (type) {
        case "ANONYMOUS":
          return t.anonymous;
        case "REGISTERED":
          return t.registered;
        case "PREMIUM":
          return t.premium;
        default:
          return type;
      }
    },
    [lang]
  );

  const getStatusLabel = useCallback(
    (status: string) => {
      const t = adminLocales[lang];
      switch (status) {
        case "ACTIVE":
          return t.active;
        case "INACTIVE":
          return t.inactive;
        case "BANNED":
          return t.banned;
        default:
          return status;
      }
    },
    [lang]
  );

  const getStatusVariant = useCallback(
    (status: string): "default" | "secondary" | "destructive" | "outline" => {
      switch (status) {
        case "ACTIVE":
          return "default";
        case "INACTIVE":
          return "secondary";
        case "BANNED":
          return "destructive";
        default:
          return "outline";
      }
    },
    []
  );

  return {
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
    handleReset,
    getUserTypeLabel,
    getStatusLabel,
    getStatusVariant,
    refresh,
  };
}
