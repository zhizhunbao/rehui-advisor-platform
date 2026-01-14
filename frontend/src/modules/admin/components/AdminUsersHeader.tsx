// Admin 用户管理头部组件
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";

export function AdminUsersHeader() {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  return <h1 className="text-2xl font-bold text-foreground">{t.users}</h1>;
}
