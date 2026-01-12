import { useState, useEffect, useCallback } from "react";
import { domainCategoryService } from "../services/admin.service";
import type {
  DomainCategory,
  CreateDomainCategoryDto,
  UpdateDomainCategoryDto,
} from "../types/admin.types";

interface UseDomainCategoriesOptions {
  autoFetch?: boolean;
}

export function useDomainCategories(options: UseDomainCategoriesOptions = {}) {
  const { autoFetch = true } = options;
  const [categories, setCategories] = useState<DomainCategory[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const fetchCategories = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await domainCategoryService.getAll();
      setCategories(data);
    } catch (err) {
      setError(
        err instanceof Error
          ? err
          : new Error("Failed to fetch domain categories")
      );
    } finally {
      setIsLoading(false);
    }
  }, []);

  const createCategory = useCallback(async (data: CreateDomainCategoryDto) => {
    setIsLoading(true);
    try {
      const newCategory = await domainCategoryService.create(data);
      setCategories((prev) => [...prev, newCategory]);
      return newCategory;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const updateCategory = useCallback(
    async (id: string, data: UpdateDomainCategoryDto) => {
      setIsLoading(true);
      try {
        const updated = await domainCategoryService.update(id, data);
        setCategories((prev) => prev.map((c) => (c.id === id ? updated : c)));
        return updated;
      } finally {
        setIsLoading(false);
      }
    },
    []
  );

  const deleteCategory = useCallback(async (id: string) => {
    setIsLoading(true);
    try {
      await domainCategoryService.delete(id);
      setCategories((prev) => prev.filter((c) => c.id !== id));
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    if (autoFetch) {
      fetchCategories();
    }
  }, [autoFetch, fetchCategories]);

  return {
    categories,
    isLoading,
    error,
    fetchCategories,
    createCategory,
    updateCategory,
    deleteCategory,
  };
}
