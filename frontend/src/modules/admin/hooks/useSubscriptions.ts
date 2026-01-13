import { useState, useCallback } from "react";
import { subscriptionService } from "../services/subscription.service";
import type {
  SubscriptionPlan,
  CreateSubscriptionDto,
  UpdateSubscriptionDto,
} from "@/common/types";

export function useSubscriptions() {
  const [subscriptions, setSubscriptions] = useState<SubscriptionPlan[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const fetchSubscriptions = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await subscriptionService.getAll();
      setSubscriptions(result);
      return result;
    } catch (err) {
      setError(
        err instanceof Error ? err : new Error("Failed to fetch subscriptions")
      );
      return [];
    } finally {
      setIsLoading(false);
    }
  }, []);

  const createSubscription = useCallback(
    async (data: CreateSubscriptionDto) => {
      try {
        const created = await subscriptionService.create(data);
        setSubscriptions((prev) => [...prev, created]);
        return created;
      } catch (err) {
        setError(
          err instanceof Error
            ? err
            : new Error("Failed to create subscription")
        );
        return null;
      }
    },
    []
  );

  const updateSubscription = useCallback(
    async (id: string, data: UpdateSubscriptionDto) => {
      try {
        const updated = await subscriptionService.update(id, data);
        setSubscriptions((prev) =>
          prev.map((s) => (s.id === id ? updated : s))
        );
        return updated;
      } catch (err) {
        setError(
          err instanceof Error
            ? err
            : new Error("Failed to update subscription")
        );
        return null;
      }
    },
    []
  );

  const deleteSubscription = useCallback(async (id: string) => {
    try {
      await subscriptionService.delete(id);
      setSubscriptions((prev) => prev.filter((s) => s.id !== id));
      return true;
    } catch (err) {
      setError(
        err instanceof Error ? err : new Error("Failed to delete subscription")
      );
      return false;
    }
  }, []);

  return {
    subscriptions,
    isLoading,
    error,
    fetchSubscriptions,
    createSubscription,
    updateSubscription,
    deleteSubscription,
  };
}
