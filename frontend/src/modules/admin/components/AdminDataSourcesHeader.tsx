// Admin 数据源页面头部组件
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import { Button } from "@/libs/shadcn/ui/button";

interface AdminDataSourcesHeaderProps {
  onRefreshAll: () => void;
  onAdd: () => void;
}

export function AdminDataSourcesHeader({
  onRefreshAll,
  onAdd,
}: AdminDataSourcesHeaderProps) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  return (
    <div className="flex justify-between items-center mb-6">
      <h1 className="text-2xl font-bold text-foreground">{t.dataSources}</h1>
      <div className="flex gap-2">
        <Button variant="outline" onClick={onRefreshAll}>
          {t.refreshAll}
        </Button>
        <Button onClick={onAdd}>{t.addSource}</Button>
      </div>
    </div>
  );
}
