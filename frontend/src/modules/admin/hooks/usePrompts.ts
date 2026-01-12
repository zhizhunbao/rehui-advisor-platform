import { useState, useEffect, useCallback } from "react";
import { promptService } from "../services/admin.service";
import type {
  PromptTemplate,
  CreatePromptDto,
  UpdatePromptDto,
} from "../types/admin.types";

interface UsePromptsOptions {
  autoFetch?: boolean;
}

export function usePrompts(options: UsePromptsOptions = {}) {
  const { autoFetch = true } = options;
  const [prompts, setPrompts] = useState<PromptTemplate[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const fetchPrompts = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await promptService.getAll();
      setPrompts(data);
    } catch (err) {
      setError(
        err instanceof Error ? err : new Error("Failed to fetch prompts")
      );
    } finally {
      setIsLoading(false);
    }
  }, []);

  const createPrompt = useCallback(async (data: CreatePromptDto) => {
    setIsLoading(true);
    try {
      const newPrompt = await promptService.create(data);
      setPrompts((prev) => [...prev, newPrompt]);
      return newPrompt;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const updatePrompt = useCallback(
    async (id: string, data: UpdatePromptDto) => {
      setIsLoading(true);
      try {
        const updated = await promptService.update(id, data);
        setPrompts((prev) => prev.map((p) => (p.id === id ? updated : p)));
        return updated;
      } finally {
        setIsLoading(false);
      }
    },
    []
  );

  const deletePrompt = useCallback(async (id: string) => {
    setIsLoading(true);
    try {
      await promptService.delete(id);
      setPrompts((prev) => prev.filter((p) => p.id !== id));
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    if (autoFetch) {
      fetchPrompts();
    }
  }, [autoFetch, fetchPrompts]);

  return {
    prompts,
    isLoading,
    error,
    fetchPrompts,
    createPrompt,
    updatePrompt,
    deletePrompt,
  };
}
