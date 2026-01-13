import { useState, useEffect, useCallback } from "react";
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

interface UseDomainsOptions {
  autoFetch?: boolean;
}

export function useDomains(options: UseDomainsOptions = {}) {
  const { autoFetch = true } = options;
  const [domains, setDomains] = useState<Domain[]>([]);
  const [categories, setCategories] = useState<DomainCategory[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const fetchDomains = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await domainService.getAll();
      setDomains(data);
    } catch (err) {
      setError(
        err instanceof Error ? err : new Error("Failed to fetch domains")
      );
    } finally {
      setIsLoading(false);
    }
  }, []);

  const fetchCategories = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await domainCategoryService.getAll();
      setCategories(data);
    } catch (err) {
      setError(
        err instanceof Error ? err : new Error("Failed to fetch categories")
      );
    } finally {
      setIsLoading(false);
    }
  }, []);

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
    return newDomain;
  }, []);

  const updateDomain = useCallback(
    async (id: string, data: UpdateDomainDto) => {
      const updated = await domainService.update(id, data);
      setDomains((prev) => prev.map((d) => (d.id === id ? updated : d)));
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
    fetchDomains,
    fetchCategories,
    fetchAll,
    createDomain,
    updateDomain,
    deleteDomain,
    createCategory,
    updateCategory,
    deleteCategory,
  };
}
