// Admin 技能管理页面头部组件
import type { Language } from "@/common/types";
import { adminLocales } from "@/common/i18n";
import { Button } from "@/libs/shadcn/ui/button";

interface AdminSkillsHeaderProps {
  lang: Language;
  isSyncing: boolean;
  onSync: () => void;
}

export function AdminSkillsHeader({
  lang,
  isSyncing,
  onSync,
}: AdminSkillsHeaderProps) {
  const t = adminLocales[lang];

  return (
    <div className="flex items-center justify-between mb-6">
      <h1 className="text-2xl font-bold">{t.skills}</h1>
      <Button onClick={onSync} disabled={isSyncing}>
        {isSyncing ? t.loading : t.syncSkills}
      </Button>
    </div>
  );
}
