// Admin 推荐管理页面头部组件
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";

export function AdminRecommendationsHeader() {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  return (
    <h1 className="text-2xl font-bold text-foreground mb-6">
      {t.recommendations}
    </h1>
  );
}
