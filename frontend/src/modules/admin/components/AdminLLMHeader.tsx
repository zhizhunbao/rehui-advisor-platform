// Admin LLM 头部组件
import type { Language } from "@/common/types";
import { adminLocales } from "@/common/i18n";
import { Button } from "@/libs/shadcn/ui/button";

interface AdminLLMHeaderProps {
  lang: Language;
  isSyncing: boolean;
  onSync: () => void;
  onCreate: () => void;
}

export function AdminLLMHeader({
  lang,
  isSyncing,
  onSync,
  onCreate,
}: AdminLLMHeaderProps) {
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
