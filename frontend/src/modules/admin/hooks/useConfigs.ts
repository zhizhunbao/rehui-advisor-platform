import { useState, useCallback } from "react";
import { configService } from "../services/config.service";
import type {
  SystemConfig,
  CreateConfigDto,
  UpdateConfigDto,
} from "../types/admin.types";

export function useConfigs() {
  const [configs, setConfigs] = useState<SystemConfig[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const fetchConfigs = useCallback(async (category?: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await configService.getAll(category);
      setConfigs(result);
      return result;
    } catch (err) {
      setError(
        err instanceof Error ? err : new Error("Failed to fetch configs")
      );
      return [];
    } finally {
      setIsLoading(false);
    }
  }, []);

  const createConfig = useCallback(async (data: CreateConfigDto) => {
    try {
      const created = await configService.create(data);
      setConfigs((prev) => [...prev, created]);
      return created;
    } catch (err) {
      setError(
        err instanceof Error ? err : new Error("Failed to create config")
      );
      return null;
    }
  }, []);

  const updateConfig = useCallback(
    async (key: string, data: UpdateConfigDto) => {
      try {
        const updated = await configService.update(key, data);
        setConfigs((prev) => prev.map((c) => (c.key === key ? updated : c)));
        return updated;
      } catch (err) {
        setError(
          err instanceof Error ? err : new Error("Failed to update config")
        );
        return null;
      }
    },
    []
  );

  const deleteConfig = useCallback(async (key: string) => {
    try {
      await configService.delete(key);
      setConfigs((prev) => prev.filter((c) => c.key !== key));
      return true;
    } catch (err) {
      setError(
        err instanceof Error ? err : new Error("Failed to delete config")
      );
      return false;
    }
  }, []);

  return {
    configs,
    isLoading,
    error,
    fetchConfigs,
    createConfig,
    updateConfig,
    deleteConfig,
  };
}
