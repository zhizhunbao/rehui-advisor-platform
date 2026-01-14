// Admin LLM 头部组件
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import { Button } from "@/libs/shadcn/ui/button";

interface AdminLLMHeaderProps {
  isSyncing: boolean;
  onSync: () => void;
  onCreate: () => void;
}

export function AdminLLMHeader({
  isSyncing,
  onSync,
  onCreate,
}: AdminLLMHeaderProps) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  return (
    <div className="flex flex-wrap gap-4 items-center justify-end">
      <Button variant="outline" onClick={onSync} disabled={isSyncing}>
        {isSyncing ? t.syncing : t.syncModels}
      </Button>
      <Button onClick={onCreate}>{t.addModel}</Button>
    </div>
  );
}
