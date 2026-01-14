// Admin 订阅计划页面头部组件
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import { Button } from "@/libs/shadcn/ui/button";

interface AdminSubscriptionsHeaderProps {
  onCreate: () => void;
}

export function AdminSubscriptionsHeader({
  onCreate,
}: AdminSubscriptionsHeaderProps) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  return (
    <div className="flex justify-between items-center mb-6">
      <h1 className="text-2xl font-bold text-foreground">{t.subscriptions}</h1>
      <Button onClick={onCreate}>{t.addPlan}</Button>
    </div>
  );
}
