// Admin Agent 框架页面头部
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import { Button } from "@/libs/shadcn/ui/button";

interface Props {
  onCreate: () => void;
}

export function AdminAgentFrameworksHeader({ onCreate }: Props) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  return (
    <div className="flex justify-between items-center">
      <div>
        <h1 className="text-2xl font-bold text-foreground">
          {t.agentFrameworks}
        </h1>
        <p className="text-muted-foreground mt-1">
          {lang === "zh"
            ? "管理 AI Agent 和多智能体框架资源"
            : "Manage AI Agent and Multi-Agent framework resources"}
        </p>
      </div>
      <Button onClick={onCreate}>
        {lang === "zh" ? "添加框架" : "Add Framework"}
      </Button>
    </div>
  );
}
