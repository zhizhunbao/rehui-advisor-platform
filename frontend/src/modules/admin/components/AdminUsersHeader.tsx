// Admin 用户管理头部组件
import type { Language } from "@/common/types";
import { adminLocales } from "@/common/i18n";

interface AdminUsersHeaderProps {
  lang: Language;
}

export function AdminUsersHeader({ lang }: AdminUsersHeaderProps) {
  const t = adminLocales[lang];

  return <h1 className="text-2xl font-bold text-foreground">{t.users}</h1>;
}
