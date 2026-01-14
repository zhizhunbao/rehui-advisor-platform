// Admin 通用页面布局组件
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";

interface AdminViewContainerProps {
  children: React.ReactNode;
}

export function AdminViewContainer({ children }: AdminViewContainerProps) {
  return <div className="space-y-6">{children}</div>;
}

interface AdminViewTitleProps {
  title?: string;
}

export function AdminViewTitle({ title }: AdminViewTitleProps) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];
  const displayTitle = title || t.dashboard;

  return <h1 className="text-2xl font-bold text-foreground">{displayTitle}</h1>;
}

interface AdminViewContentProps {
  isLoading: boolean;
  isEmpty: boolean;
  loadingText?: string;
  emptyText?: string;
  children: React.ReactNode;
}

export function AdminViewContent({
  isLoading,
  isEmpty,
  loadingText,
  emptyText,
  children,
}: AdminViewContentProps) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];
  const loading = loadingText || t.loading;
  const empty = emptyText || t.noData;

  if (isLoading && isEmpty) {
    return (
      <div className="text-center py-8 text-muted-foreground">{loading}</div>
    );
  }

  if (isEmpty) {
    return (
      <div className="text-center py-8 text-muted-foreground">{empty}</div>
    );
  }

  return <>{children}</>;
}
