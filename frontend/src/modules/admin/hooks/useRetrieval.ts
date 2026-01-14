// Admin 检索引擎管理 Hook
import { useState, useEffect, useCallback } from "react";
import type {
  RetrievalEngine,
  RetrievalEngineType,
  RetrievalEngineCreate,
  RetrievalTestResult,
  RetrievalEngineForm,
} from "@/common/types";
import { retrievalService } from "../services/retrieval.service";

const defaultEngineForm: RetrievalEngineForm = {
  name: "",
  display_name: "",
  type: "structured_query",
  description: "",
  config: {},
  is_active: true,
};

export function useRetrieval(options: { autoFetch?: boolean } = {}) {
  const { autoFetch = true } = options;

  // Data state
  const [engines, setEngines] = useState<RetrievalEngine[]>([]);
  const [engineTypes, setEngineTypes] = useState<RetrievalEngineType[]>([]);
  const [loading, setLoading] = useState(false);
  const [testing, setTesting] = useState(false);
  const [testResult, setTestResult] = useState<RetrievalTestResult | null>(
    null
  );

  // Filter state
  const [filterType, setFilterType] = useState("");
  const [filterStatus, setFilterStatus] = useState("");

  // Engine dialog state
  const [showEngineDialog, setShowEngineDialog] = useState(false);
  const [editingEngine, setEditingEngine] = useState<RetrievalEngine | null>(
    null
  );
  const [engineForm, setEngineForm] =
    useState<RetrievalEngineForm>(defaultEngineForm);
  const [configJson, setConfigJson] = useState("{}");

  // Delete state
  const [deleteTarget, setDeleteTarget] = useState<{
    id: string;
    name: string;
  } | null>(null);

  // Test dialog state
  const [showTestDialog, setShowTestDialog] = useState(false);
  const [testEngineId, setTestEngineId] = useState("");
  const [testQuery, setTestQuery] = useState("");

  // Computed values
  const filteredEngines = engines.filter((e) => {
    if (filterType && e.type !== filterType) return false;
    if (filterStatus === "active" && !e.isActive) return false;
    if (filterStatus === "inactive" && e.isActive) return false;
    return true;
  });

  const activeEngines = engines.filter((e) => e.isActive).length;
  const defaultEngine = engines.find((e) => e.isDefault);

  // API methods
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

  // UI handlers
  const getEngineForm = useCallback(
    (engine?: RetrievalEngine): RetrievalEngineForm => {
      if (!engine) return { ...defaultEngineForm };
      return {
        name: engine.name,
        display_name: engine.displayName,
        type: engine.type,
        description: engine.description,
        config: engine.config,
        is_active: engine.isActive,
      };
    },
    []
  );

  const handleCreateEngine = useCallback(() => {
    setEditingEngine(null);
    setEngineForm(defaultEngineForm);
    setConfigJson("{}");
    setShowEngineDialog(true);
  }, []);

  const handleEditEngine = useCallback((engine: RetrievalEngine) => {
    setEditingEngine(engine);
    setEngineForm({
      name: engine.name,
      display_name: engine.displayName,
      type: engine.type,
      description: engine.description,
      config: engine.config,
      is_active: engine.isActive,
    });
    setConfigJson(JSON.stringify(engine.config, null, 2));
    setShowEngineDialog(true);
  }, []);

  const handleSaveEngine = useCallback(async () => {
    let config: Record<string, unknown> = {};
    try {
      config = JSON.parse(configJson);
    } catch {
      return { success: false, error: "invalid_json" };
    }

    const payload: RetrievalEngineCreate = {
      name: engineForm.name,
      displayName: engineForm.display_name,
      type: engineForm.type,
      description: engineForm.description,
      config,
      isActive: engineForm.is_active,
    };

    if (editingEngine) {
      await update(editingEngine.id, payload);
    } else {
      await create(payload);
    }
    setShowEngineDialog(false);
    return { success: true };
  }, [configJson, engineForm, editingEngine, update, create]);

  const handleDeleteEngine = useCallback(async () => {
    if (!deleteTarget) return;
    await remove(deleteTarget.id);
    setDeleteTarget(null);
  }, [deleteTarget, remove]);

  const handleSetDefault = useCallback(
    async (engineId: string) => {
      await setDefault(engineId);
    },
    [setDefault]
  );

  const handleTest = useCallback(async () => {
    if (!testEngineId || !testQuery) return;
    await test(testEngineId, testQuery);
  }, [testEngineId, testQuery, test]);

  const resetFilters = useCallback(() => {
    setFilterType("");
    setFilterStatus("");
  }, []);

  useEffect(() => {
    if (autoFetch) {
      fetchEngines();
      fetchTypes();
    }
  }, [autoFetch, fetchEngines, fetchTypes]);

  return {
    // Data
    engines,
    engineTypes,
    loading,
    testing,
    testResult,
    filteredEngines,
    activeEngines,
    defaultEngine,

    // Filter state
    filterType,
    setFilterType,
    filterStatus,
    setFilterStatus,

    // Engine dialog state
    showEngineDialog,
    setShowEngineDialog,
    editingEngine,
    engineForm,
    setEngineForm,
    configJson,
    setConfigJson,

    // Delete state
    deleteTarget,
    setDeleteTarget,

    // Test dialog state
    showTestDialog,
    setShowTestDialog,
    testEngineId,
    setTestEngineId,
    testQuery,
    setTestQuery,

    // API methods
    fetchEngines,
    fetchTypes,
    create,
    update,
    remove,
    setDefault,
    test,

    // UI handlers
    getEngineForm,
    handleCreateEngine,
    handleEditEngine,
    handleSaveEngine,
    handleDeleteEngine,
    handleSetDefault,
    handleTest,
    resetFilters,
  };
}
