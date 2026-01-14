// Admin Agent 框架列表
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import type { AgentFramework } from "@/common/types";
import { AdminAgentFrameworkCard } from "./AdminAgentFrameworkCard";

interface Props {
  frameworks: AgentFramework[];
  isLoading: boolean;
  onSelect: (framework: AgentFramework) => void;
  onRefresh: (id: string) => void;
  onDelete: (id: string) => void;
}

export function AdminAgentFrameworksList({
  frameworks,
  isLoading,
  onSelect,
  onRefresh,
  onDelete,
}: Props) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64 text-muted-foreground">
        {t.loading}
      </div>
    );
  }

  if (frameworks.length === 0) {
    return (
      <div className="text-center text-muted-foreground py-12">{t.noData}</div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {frameworks.map((framework) => (
        <AdminAgentFrameworkCard
          key={framework.id}
          framework={framework}
          onClick={() => onSelect(framework)}
          onRefresh={() => onRefresh(framework.id)}
          onDelete={() => onDelete(framework.id)}
        />
      ))}
    </div>
  );
}
