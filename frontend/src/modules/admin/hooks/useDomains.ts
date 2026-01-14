// Admin 领域管理 Hook
import { useState, useEffect, useCallback } from "react";
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import {
  domainService,
  domainCategoryService,
} from "../services/domain.service";
import type {
  Domain,
  DomainCategory,
  CreateDomainDto,
  UpdateDomainDto,
  CreateDomainCategoryDto,
  UpdateDomainCategoryDto,
} from "@/common/types";

export function useDomains(autoFetch = true) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  const [domains, setDomains] = useState<Domain[]>([]);
  const [categories, setCategories] = useState<DomainCategory[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const [search, setSearch] = useState("");
  const [filterCategoryId, setFilterCategoryId] = useState("__all__");
  const [editingDomain, setEditingDomain] = useState<Domain | null>(null);
  const [isCreating, setIsCreating] = useState(false);

  const isGroupedMode = !search && filterCategoryId === "__all__";

  const getCategoryName = useCallback(
    (categoryId: string) => {
      const category = categories.find((c) => c.id === categoryId);
      if (!category) return t.uncategorized;
      return lang === "zh" ? category.name : category.nameEn;
    },
    [categories, lang, t.uncategorized]
  );

  const categoryOptions = categories.map((cat) => ({
    value: cat.id,
    label: lang === "zh" ? cat.name : cat.nameEn,
    count: domains.filter((d) => d.categoryId === cat.id).length,
  }));

  const filteredDomains = domains.filter((d) => {
    const matchCategory =
      filterCategoryId === "__all__" || d.categoryId === filterCategoryId;
    const matchSearch =
      !search ||
      d.name.toLowerCase().includes(search.toLowerCase()) ||
      d.nameEn.toLowerCase().includes(search.toLowerCase()) ||
      d.code.toLowerCase().includes(search.toLowerCase());
    return matchCategory && matchSearch;
  });

  const groupedDomains = categories
    .filter((cat) => domains.some((d) => d.categoryId === cat.id))
    .map((cat) => ({
      category: cat,
      domains: domains.filter((d) => d.categoryId === cat.id),
    }));

  const stats = {
    total: domains.length,
    active: domains.filter((d) => d.isActive).length,
    inactive: domains.filter((d) => !d.isActive).length,
    categories: categories.length,
  };

  const fetchAll = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const [domainsData, categoriesData] = await Promise.all([
        domainService.getAll(),
        domainCategoryService.getAll(),
      ]);
      setDomains(domainsData);
      setCategories(categoriesData);
    } catch (err) {
      setError(err instanceof Error ? err : new Error("Failed to fetch data"));
    } finally {
      setIsLoading(false);
    }
  }, []);

  const createDomain = useCallback(async (data: CreateDomainDto) => {
    const newDomain = await domainService.create(data);
    setDomains((prev) => [...prev, newDomain]);
    setIsCreating(false);
    return newDomain;
  }, []);

  const updateDomain = useCallback(
    async (id: string, data: UpdateDomainDto) => {
      const updated = await domainService.update(id, data);
      setDomains((prev) => prev.map((d) => (d.id === id ? updated : d)));
      setEditingDomain(null);
      return updated;
    },
    []
  );

  const deleteDomain = useCallback(async (id: string) => {
    await domainService.delete(id);
    setDomains((prev) => prev.filter((d) => d.id !== id));
  }, []);

  const createCategory = useCallback(async (data: CreateDomainCategoryDto) => {
    const newCategory = await domainCategoryService.create(data);
    setCategories((prev) => [...prev, newCategory]);
    return newCategory;
  }, []);

  const updateCategory = useCallback(
    async (id: string, data: UpdateDomainCategoryDto) => {
      const updated = await domainCategoryService.update(id, data);
      setCategories((prev) => prev.map((c) => (c.id === id ? updated : c)));
      return updated;
    },
    []
  );

  const deleteCategory = useCallback(async (id: string) => {
    await domainCategoryService.delete(id);
    setCategories((prev) => prev.filter((c) => c.id !== id));
  }, []);

  const handleToggle = useCallback(
    async (domain: Domain) => {
      await updateDomain(domain.id, {
        name: domain.name,
        nameEn: domain.nameEn,
        description: domain.description,
        descriptionEn: domain.descriptionEn,
        icon: domain.icon,
        color: domain.color,
        promptTemplateId: domain.promptTemplateId,
        categoryId: domain.categoryId,
        isActive: !domain.isActive,
        sortOrder: domain.sortOrder,
        discoveryKeywords: domain.discoveryKeywords || [],
      });
    },
    [updateDomain]
  );

  const handleSave = useCallback(
    async (data: CreateDomainDto | UpdateDomainDto) => {
      if (editingDomain) {
        await updateDomain(editingDomain.id, data as UpdateDomainDto);
      } else {
        await createDomain(data as CreateDomainDto);
      }
    },
    [editingDomain, updateDomain, createDomain]
  );

  const handleReset = useCallback(() => {
    setSearch("");
    setFilterCategoryId("__all__");
  }, []);

  const handleCloseDialog = useCallback(() => {
    setIsCreating(false);
    setEditingDomain(null);
  }, []);

  useEffect(() => {
    if (autoFetch) {
      fetchAll();
    }
  }, [autoFetch, fetchAll]);

  return {
    domains,
    categories,
    isLoading,
    error,
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
    fetchAll,
    createDomain,
    updateDomain,
    deleteDomain,
    createCategory,
    updateCategory,
    deleteCategory,
    handleToggle,
    handleSave,
    handleReset,
    handleCloseDialog,
  };
}
