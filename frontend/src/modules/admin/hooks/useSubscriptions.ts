// Admin 订阅计划管理 Hook
import { useState, useCallback, useEffect } from "react";
import type {
  SubscriptionPlan,
  CreateSubscriptionDto,
  UpdateSubscriptionDto,
} from "@/common/types";
import { subscriptionService } from "../services/subscription.service";

export function useSubscriptions() {
  const [subscriptions, setSubscriptions] = useState<SubscriptionPlan[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [editingPlan, setEditingPlan] = useState<SubscriptionPlan | null>(null);
  const [formData, setFormData] = useState<CreateSubscriptionDto>(
    getDefaultForm()
  );

  const fetchSubscriptions = useCallback(async () => {
    setIsLoading(true);
    try {
      const result = await subscriptionService.getAll();
      setSubscriptions(result);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchSubscriptions();
  }, [fetchSubscriptions]);

  const handleCreate = useCallback(() => {
    setEditingPlan(null);
    setFormData(getDefaultForm());
    setShowForm(true);
  }, []);

  const handleEdit = useCallback((plan: SubscriptionPlan) => {
    setEditingPlan(plan);
    setFormData({
      name: plan.name,
      nameEn: plan.nameEn,
      description: plan.description,
      descriptionEn: plan.descriptionEn,
      price: plan.price,
      currency: plan.currency,
      dailyQuota: plan.dailyQuota,
      features: plan.features,
      sortOrder: plan.sortOrder,
    });
    setShowForm(true);
  }, []);

  const handleSubmit = useCallback(async () => {
    if (editingPlan) {
      const updated = await subscriptionService.update(editingPlan.id, {
        ...formData,
        isActive: editingPlan.isActive,
      } as UpdateSubscriptionDto);
      setSubscriptions((prev) =>
        prev.map((s) => (s.id === editingPlan.id ? updated : s))
      );
    } else {
      const created = await subscriptionService.create(formData);
      setSubscriptions((prev) => [...prev, created]);
    }
    setShowForm(false);
  }, [editingPlan, formData]);

  const handleDelete = useCallback(async (id: string) => {
    await subscriptionService.delete(id);
    setSubscriptions((prev) => prev.filter((s) => s.id !== id));
  }, []);

  const handleCloseForm = useCallback(() => {
    setShowForm(false);
  }, []);

  return {
    subscriptions,
    isLoading,
    showForm,
    editingPlan,
    formData,
    setFormData,
    handleCreate,
    handleEdit,
    handleSubmit,
    handleDelete,
    handleCloseForm,
  };
}

function getDefaultForm(): CreateSubscriptionDto {
  return {
    name: "",
    nameEn: "",
    description: "",
    descriptionEn: "",
    price: 0,
    currency: "CNY",
    dailyQuota: 10,
    features: [],
    sortOrder: 0,
  };
}
