import { useState, useCallback } from "react";
import { userService, type UserListParams } from "../services/user.service";
import type { AdminUser, PaginatedResponse } from "../types/admin.types";

export function useUsers() {
  const [data, setData] = useState<PaginatedResponse<AdminUser> | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const fetchUsers = useCallback(async (params?: UserListParams) => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await userService.getAll(params);
      setData(result);
      return result;
    } catch (err) {
      setError(err instanceof Error ? err : new Error("Failed to fetch users"));
      return null;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const toggleUserStatus = useCallback(async (id: string) => {
    try {
      const updated = await userService.toggleStatus(id);
      setData((prev) =>
        prev
          ? {
              ...prev,
              data: prev.data.map((u) => (u.id === id ? updated : u)),
            }
          : null
      );
      return updated;
    } catch (err) {
      setError(
        err instanceof Error ? err : new Error("Failed to toggle status")
      );
      return null;
    }
  }, []);

  const updateUser = useCallback(
    async (id: string, updates: Partial<AdminUser>) => {
      try {
        const updated = await userService.update(id, updates);
        setData((prev) =>
          prev
            ? {
                ...prev,
                data: prev.data.map((u) => (u.id === id ? updated : u)),
              }
            : null
        );
        return updated;
      } catch (err) {
        setError(
          err instanceof Error ? err : new Error("Failed to update user")
        );
        return null;
      }
    },
    []
  );

  return {
    users: data?.data || [],
    total: data?.total || 0,
    page: data?.page || 1,
    limit: data?.limit || 20,
    isLoading,
    error,
    fetchUsers,
    toggleUserStatus,
    updateUser,
  };
}
