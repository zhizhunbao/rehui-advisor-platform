import { useEffect, useState } from "react";
import { useSubscriptions } from "@/modules/admin/hooks";
import { adminLocales, type Language } from "@/locales";
import type {
  SubscriptionPlan,
  CreateSubscriptionDto,
  UpdateSubscriptionDto,
} from "@/modules/admin/types/admin.types";
import { Button } from "@/libs/shadcn/ui/button";
import { Input } from "@/libs/shadcn/ui/input";
import { Badge } from "@/libs/shadcn/ui/badge";
import { Card, CardContent } from "@/libs/shadcn/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/libs/shadcn/ui/select";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/libs/shadcn/ui/dialog";

interface SubscriptionsViewProps {
  lang: Language;
}

export default function SubscriptionsView({ lang }: SubscriptionsViewProps) {
  const t = adminLocales[lang];
  const {
    subscriptions,
    isLoading,
    fetchSubscriptions,
    createSubscription,
    updateSubscription,
    deleteSubscription,
  } = useSubscriptions();
  const [showForm, setShowForm] = useState(false);
  const [editingPlan, setEditingPlan] = useState<SubscriptionPlan | null>(null);
  const [formData, setFormData] = useState<CreateSubscriptionDto>({
    name: "",
    nameEn: "",
    description: "",
    descriptionEn: "",
    price: 0,
    currency: "CNY",
    dailyQuota: 10,
    features: [],
    sortOrder: 0,
  });

  useEffect(() => {
    fetchSubscriptions();
  }, [fetchSubscriptions]);

  const handleEdit = (plan: SubscriptionPlan) => {
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
  };

  const handleCreate = () => {
    setEditingPlan(null);
    setFormData({
      name: "",
      nameEn: "",
      description: "",
      descriptionEn: "",
      price: 0,
      currency: "CNY",
      dailyQuota: 10,
      features: [],
      sortOrder: 0,
    });
    setShowForm(true);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (editingPlan) {
      await updateSubscription(
        editingPlan.id,
        formData as UpdateSubscriptionDto
      );
    } else {
      await createSubscription(formData);
    }
    setShowForm(false);
  };

  const handleDelete = async (id: string) => {
    if (window.confirm(t.confirmDelete)) {
      await deleteSubscription(id);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-foreground">
          {t.subscriptions}
        </h1>
        <Button onClick={handleCreate}>{t.addPlan}</Button>
      </div>

      {isLoading ? (
        <div className="text-center py-8 text-muted-foreground">
          {t.loading}
        </div>
      ) : subscriptions.length === 0 ? (
        <div className="text-center py-8 text-muted-foreground">{t.noData}</div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {subscriptions.map((plan) => (
            <Card key={plan.id}>
              <CardContent className="p-4">
                <div className="flex justify-between items-start mb-2">
                  <h3 className="text-lg font-semibold text-foreground">
                    {lang === "zh" ? plan.name : plan.nameEn}
                  </h3>
                  <Badge variant={plan.isActive ? "default" : "secondary"}>
                    {plan.isActive ? t.active : t.inactive}
                  </Badge>
                </div>
                <p className="text-sm text-muted-foreground mb-3">
                  {lang === "zh" ? plan.description : plan.descriptionEn}
                </p>
                <div className="text-2xl font-bold text-foreground mb-2">
                  {plan.currency} {plan.price}
                </div>
                <div className="text-sm text-muted-foreground mb-3">
                  {t.dailyQuota}: {plan.dailyQuota}
                </div>
                {plan.features.length > 0 && (
                  <ul className="text-sm text-muted-foreground mb-4 space-y-1">
                    {plan.features.map((f, i) => (
                      <li key={i}>• {f}</li>
                    ))}
                  </ul>
                )}
                <div className="flex gap-2">
                  <Button
                    variant="link"
                    size="sm"
                    onClick={() => handleEdit(plan)}
                  >
                    {t.edit}
                  </Button>
                  <Button
                    variant="link"
                    size="sm"
                    className="text-destructive"
                    onClick={() => handleDelete(plan.id)}
                  >
                    {t.delete}
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      <Dialog open={showForm} onOpenChange={(o) => !o && setShowForm(false)}>
        <DialogContent className="max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>{editingPlan ? t.editPlan : t.addPlan}</DialogTitle>
          </DialogHeader>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">{t.planName}</label>
                <Input
                  value={formData.name}
                  onChange={(e) =>
                    setFormData({ ...formData, name: e.target.value })
                  }
                  required
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">{t.planNameEn}</label>
                <Input
                  value={formData.nameEn}
                  onChange={(e) =>
                    setFormData({ ...formData, nameEn: e.target.value })
                  }
                  required
                />
              </div>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">{t.planDescription}</label>
              <textarea
                value={formData.description}
                onChange={(e) =>
                  setFormData({ ...formData, description: e.target.value })
                }
                rows={2}
                className="w-full px-3 py-2 border rounded-md bg-background text-foreground border-input focus:outline-none focus:ring-2 focus:ring-ring"
              />
            </div>
            <div className="grid grid-cols-3 gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">{t.planPrice}</label>
                <Input
                  type="number"
                  value={formData.price}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      price: Number(e.target.value),
                    })
                  }
                  min={0}
                  step={0.01}
                />
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">{t.planCurrency}</label>
                <Select
                  value={formData.currency}
                  onValueChange={(v) =>
                    setFormData({ ...formData, currency: v })
                  }
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="CNY">CNY</SelectItem>
                    <SelectItem value="USD">USD</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium">{t.dailyQuota}</label>
                <Input
                  type="number"
                  value={formData.dailyQuota}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      dailyQuota: Number(e.target.value),
                    })
                  }
                  min={0}
                />
              </div>
            </div>
            <DialogFooter>
              <Button
                type="button"
                variant="outline"
                onClick={() => setShowForm(false)}
              >
                {t.cancel}
              </Button>
              <Button type="submit">{t.save}</Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
}
