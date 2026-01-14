// Admin 配置页面头部
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import { Button } from "@/libs/shadcn/ui/button";

interface Props {
  onCreate: () => void;
}

export function AdminConfigsHeader({ onCreate }: Props) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  return (
    <div className="flex justify-between items-center">
      <h1 className="text-2xl font-bold text-foreground">{t.configs}</h1>
      <Button onClick={onCreate}>{t.addConfig}</Button>
    </div>
  );
}
