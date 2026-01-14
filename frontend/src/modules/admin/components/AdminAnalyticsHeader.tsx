// Admin 数据分析页面头部
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";

export function AdminAnalyticsHeader() {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  return <h1 className="text-2xl font-bold text-foreground">{t.analytics}</h1>;
}
