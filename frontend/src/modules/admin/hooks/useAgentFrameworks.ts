// Admin Agent 框架管理 Hook
import { useState, useEffect, useCallback } from "react";
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import type { AgentFramework, CreateAgentFrameworkDto } from "@/common/types";
import { agentFrameworkService } from "../services/agentFramework.service";

export function useAgentFrameworks(autoFetch = true) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  const [frameworks, setFrameworks] = useState<AgentFramework[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [selectedFramework, setSelectedFramework] =
    useState<AgentFramework | null>(null);
  const [showAddModal, setShowAddModal] = useState(false);

  const fetchFrameworks = useCallback(async () => {
    setIsLoading(true);
    try {
      const data = await agentFrameworkService.getList();
      setFrameworks(data);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const handleRefresh = useCallback(
    async (id: string) => {
      await agentFrameworkService.refresh(id);
      fetchFrameworks();
    },
    [fetchFrameworks]
  );

  const handleDelete = useCallback(
    async (id: string) => {
      if (!confirm(t.confirmDelete)) return;
      await agentFrameworkService.delete(id);
      fetchFrameworks();
    },
    [fetchFrameworks, t.confirmDelete]
  );

  const handleCreate = useCallback(
    async (data: CreateAgentFrameworkDto) => {
      await agentFrameworkService.create(data);
      setShowAddModal(false);
      fetchFrameworks();
    },
    [fetchFrameworks]
  );

  const handleRefreshSelected = useCallback(async () => {
    if (selectedFramework) {
      await handleRefresh(selectedFramework.id);
      setSelectedFramework(null);
    }
  }, [selectedFramework, handleRefresh]);

  const filteredFrameworks = frameworks.filter(
    (f) =>
      f.name.toLowerCase().includes(search.toLowerCase()) ||
      f.description.toLowerCase().includes(search.toLowerCase())
  );

  const stats = {
    total: frameworks.length,
    totalStars: frameworks.reduce((sum, f) => sum + (f.githubStars || 0), 0),
    active: frameworks.filter((f) => f.status === "active").length,
    tags: new Set(frameworks.flatMap((f) => f.tags || [])).size,
  };

  useEffect(() => {
    if (autoFetch) {
      fetchFrameworks();
    }
  }, [autoFetch, fetchFrameworks]);

  return {
    frameworks,
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
  };
}
