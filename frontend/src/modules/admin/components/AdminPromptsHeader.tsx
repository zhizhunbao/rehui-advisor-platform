// Admin 提示词管理页面头部组件
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import { Button } from "@/libs/shadcn/ui/button";

interface AdminPromptsHeaderProps {
  isSyncing: boolean;
  onSync: () => void;
}

export function AdminPromptsHeader({
  isSyncing,
  onSync,
}: AdminPromptsHeaderProps) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  return (
    <div className="flex items-center justify-between mb-6">
      <h1 className="text-2xl font-bold">{t.prompts}</h1>
      <Button onClick={onSync} disabled={isSyncing}>
        {isSyncing ? t.loading : t.syncPrompts}
      </Button>
    </div>
  );
}
