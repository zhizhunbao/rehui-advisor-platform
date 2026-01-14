// Admin 系统配置管理 Hook
import { useState, useEffect, useCallback } from "react";
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import { configService } from "../services/config.service";
import type {
  SystemConfig,
  CreateConfigDto,
  UpdateConfigDto,
} from "@/common/types";

export function useConfigs(autoFetch = true) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  const [configs, setConfigs] = useState<SystemConfig[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [categoryFilter, setCategoryFilter] = useState("__all__");
  const [showForm, setShowForm] = useState(false);
  const [editingConfig, setEditingConfig] = useState<SystemConfig | null>(null);
  const [formData, setFormData] = useState<CreateConfigDto>({
    key: "",
    value: "",
    category: "general",
    description: "",
    isSensitive: false,
  });

  const fetchConfigs = useCallback(async (category?: string) => {
    setIsLoading(true);
    try {
      const result = await configService.getAll(category);
      setConfigs(result);
      return result;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const createConfig = useCallback(async (data: CreateConfigDto) => {
    const created = await configService.create(data);
    setConfigs((prev) => [...prev, created]);
    return created;
  }, []);

  const updateConfig = useCallback(
    async (key: string, data: UpdateConfigDto) => {
      const updated = await configService.update(key, data);
      setConfigs((prev) => prev.map((c) => (c.key === key ? updated : c)));
      return updated;
    },
    []
  );

  const deleteConfig = useCallback(async (key: string) => {
    await configService.delete(key);
    setConfigs((prev) => prev.filter((c) => c.key !== key));
  }, []);

  const handleEdit = useCallback((config: SystemConfig) => {
    setEditingConfig(config);
    setFormData({
      key: config.key,
      value: config.value,
      category: config.category,
      description: config.description,
      isSensitive: config.isSensitive,
    });
    setShowForm(true);
  }, []);

  const handleCreate = useCallback(() => {
    setEditingConfig(null);
    setFormData({
      key: "",
      value: "",
      category: "general",
      description: "",
      isSensitive: false,
    });
    setShowForm(true);
  }, []);

  const handleSubmit = useCallback(
    async (e: React.FormEvent) => {
      e.preventDefault();
      if (editingConfig) {
        await updateConfig(editingConfig.key, {
          value: formData.value,
          category: formData.category,
          description: formData.description,
          isSensitive: formData.isSensitive,
        });
      } else {
        await createConfig(formData);
      }
      setShowForm(false);
    },
    [editingConfig, formData, updateConfig, createConfig]
  );

  const handleDelete = useCallback(
    async (key: string) => {
      if (window.confirm(t.confirmDelete)) {
        await deleteConfig(key);
      }
    },
    [deleteConfig, t.confirmDelete]
  );

  const handleCloseForm = useCallback(() => {
    setShowForm(false);
  }, []);

  const getCategoryLabel = useCallback(
    (cat: string) => {
      const labels: Record<string, string> = {
        general: t.general,
        security: t.security,
        notification: t.notification,
        payment: t.payment,
      };
      return labels[cat] || cat;
    },
    [t]
  );

  useEffect(() => {
    if (autoFetch) {
      const category =
        categoryFilter !== "__all__" ? categoryFilter : undefined;
      fetchConfigs(category);
    }
  }, [autoFetch, categoryFilter, fetchConfigs]);

  return {
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
  };
}
