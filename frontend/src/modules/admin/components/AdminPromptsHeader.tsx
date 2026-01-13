// Admin 提示词管理页面头部组件
import type { Language } from "@/common/types";
import { adminLocales } from "@/common/i18n";
import { Button } from "@/libs/shadcn/ui/button";

interface AdminPromptsHeaderProps {
  lang: Language;
  isSyncing: boolean;
  onSync: () => void;
}

export function AdminPromptsHeader({
  lang,
  isSyncing,
  onSync,
}: AdminPromptsHeaderProps) {
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
