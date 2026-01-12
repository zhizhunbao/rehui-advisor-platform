import { useState, useEffect, useCallback } from "react";
import { domainService } from "../services/admin.service";
import type {
  Domain,
  CreateDomainDto,
  UpdateDomainDto,
} from "../types/admin.types";

interface UseDomainsOptions {
  autoFetch?: boolean;
}

export function useDomains(options: UseDomainsOptions = {}) {
  const { autoFetch = true } = options;
  const [domains, setDomains] = useState<Domain[]>([]);
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

  const createDomain = useCallback(async (data: CreateDomainDto) => {
    setIsLoading(true);
    try {
      const newDomain = await domainService.create(data);
      setDomains((prev) => [...prev, newDomain]);
      return newDomain;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const updateDomain = useCallback(
    async (id: string, data: UpdateDomainDto) => {
      setIsLoading(true);
      try {
        const updated = await domainService.update(id, data);
        setDomains((prev) => prev.map((d) => (d.id === id ? updated : d)));
        return updated;
      } finally {
        setIsLoading(false);
      }
    },
    []
  );

  const deleteDomain = useCallback(async (id: string) => {
    setIsLoading(true);
    try {
      await domainService.delete(id);
      setDomains((prev) => prev.filter((d) => d.id !== id));
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    if (autoFetch) {
      fetchDomains();
    }
  }, [autoFetch, fetchDomains]);

  return {
    domains,
    isLoading,
    error,
    fetchDomains,
    createDomain,
    updateDomain,
    deleteDomain,
  };
}
