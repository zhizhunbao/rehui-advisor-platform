// Admin 调度任务页面头部组件
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import { Button } from "@/libs/shadcn/ui/button";

interface AdminSchedulerHeaderProps {
  onCreate: () => void;
}

export function AdminSchedulerHeader({ onCreate }: AdminSchedulerHeaderProps) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  return (
    <div className="flex items-center justify-between mb-6">
      <h2 className="text-2xl font-bold">{t.scheduler}</h2>
      <Button onClick={onCreate}>{t.addJob}</Button>
    </div>
  );
}
