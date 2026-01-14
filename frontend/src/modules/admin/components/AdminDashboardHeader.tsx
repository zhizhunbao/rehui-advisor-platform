// Admin 仪表盘页面头部
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";

export function AdminDashboardHeader() {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  return <h1 className="text-2xl font-bold text-foreground">{t.dashboard}</h1>;
}
