// Admin 检索引擎页面头部组件
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import { Button } from "@/libs/shadcn/ui/button";

interface AdminRetrievalHeaderProps {
  onTest: () => void;
  onCreate: () => void;
}

export function AdminRetrievalHeader({
  onTest,
  onCreate,
}: AdminRetrievalHeaderProps) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  return (
    <div className="flex justify-end gap-2">
      <Button variant="outline" onClick={onTest}>
        🧪 {t.testEngine}
      </Button>
      <Button onClick={onCreate}>+ {t.addEngine}</Button>
    </div>
  );
}
