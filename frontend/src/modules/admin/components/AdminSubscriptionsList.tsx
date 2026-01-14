// Admin 订阅计划列表组件
import type { SubscriptionPlan } from "@/common/types";
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import { Button } from "@/libs/shadcn/ui/button";
import { Badge } from "@/libs/shadcn/ui/badge";
import { Card, CardContent } from "@/libs/shadcn/ui/card";

interface AdminSubscriptionsListProps {
  subscriptions: SubscriptionPlan[];
  isLoading: boolean;
  onEdit: (plan: SubscriptionPlan) => void;
  onDelete: (id: string) => void;
}

export function AdminSubscriptionsList({
  subscriptions,
  isLoading,
  onEdit,
  onDelete,
}: AdminSubscriptionsListProps) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  if (isLoading) {
    return (
      <div className="text-center py-8 text-muted-foreground">{t.loading}</div>
    );
  }

  if (subscriptions.length === 0) {
    return (
      <div className="text-center py-8 text-muted-foreground">{t.noData}</div>
    );
  }

  return (
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
                {plan.features.map((feature, idx) => (
                  <li key={idx}>✓ {feature}</li>
                ))}
              </ul>
            )}
            <div className="flex gap-2">
              <Button variant="link" size="sm" onClick={() => onEdit(plan)}>
                {t.edit}
              </Button>
              <Button
                variant="link"
                size="sm"
                className="text-destructive"
                onClick={() => onDelete(plan.id)}
              >
                {t.delete}
              </Button>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
