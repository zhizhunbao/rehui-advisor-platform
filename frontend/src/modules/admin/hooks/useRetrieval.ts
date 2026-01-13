// Admin 检索引擎管理 Hook
import { useState, useEffect, useCallback } from "react";
import type {
  RetrievalEngine,
  RetrievalEngineType,
  RetrievalEngineCreate,
  RetrievalTestResult,
} from "@/common/types";
import { retrievalService } from "../services/retrieval.service";

interface UseRetrievalOptions {
  autoFetch?: boolean;
}

export function useRetrieval(options: UseRetrievalOptions = {}) {
  const { autoFetch = true } = options;
  const [engines, setEngines] = useState<RetrievalEngine[]>([]);
  const [engineTypes, setEngineTypes] = useState<RetrievalEngineType[]>([]);
  const [loading, setLoading] = useState(false);
  const [testing, setTesting] = useState(false);
  const [testResult, setTestResult] = useState<RetrievalTestResult | null>(
    null
  );

  const fetchEngines = useCallback(async () => {
    setLoading(true);
    try {
      const data = await retrievalService.getList();
      setEngines(data);
      return data;
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchTypes = useCallback(async () => {
    const data = await retrievalService.getTypes();
    setEngineTypes(data);
    return data;
  }, []);

  const create = useCallback(async (data: RetrievalEngineCreate) => {
    const engine = await retrievalService.create(data);
    setEngines((prev) => [...prev, engine]);
    return engine;
  }, []);

  const update = useCallback(
    async (id: string, data: RetrievalEngineCreate) => {
      const engine = await retrievalService.update(id, data);
      setEngines((prev) => prev.map((e) => (e.id === id ? engine : e)));
      return engine;
    },
    []
  );

  const remove = useCallback(async (id: string) => {
    await retrievalService.delete(id);
    setEngines((prev) => prev.filter((e) => e.id !== id));
  }, []);

  const setDefault = useCallback(
    async (engineId: string) => {
      await retrievalService.setDefault(engineId);
      await fetchEngines();
    },
    [fetchEngines]
  );

  const test = useCallback(async (engineId: string, query: string) => {
    setTesting(true);
    setTestResult(null);
    try {
      const result = await retrievalService.test(engineId, query);
      setTestResult(result);
      return result;
    } finally {
      setTesting(false);
    }
  }, []);

  useEffect(() => {
    if (autoFetch) {
      fetchEngines();
      fetchTypes();
    }
  }, [autoFetch, fetchEngines, fetchTypes]);

  return {
    engines,
    engineTypes,
    loading,
    testing,
    testResult,
    fetchEngines,
    fetchTypes,
    create,
    update,
    remove,
    setDefault,
    test,
  };
}
