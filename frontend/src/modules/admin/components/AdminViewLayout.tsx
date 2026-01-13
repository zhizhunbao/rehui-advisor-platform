// Admin 通用页面布局组件
interface AdminViewContainerProps {
  children: React.ReactNode;
}

export function AdminViewContainer({ children }: AdminViewContainerProps) {
  return <div className="space-y-6">{children}</div>;
}

interface AdminViewTitleProps {
  title: string;
}

export function AdminViewTitle({ title }: AdminViewTitleProps) {
  return <h1 className="text-2xl font-bold text-foreground">{title}</h1>;
}

interface AdminViewContentProps {
  isLoading: boolean;
  isEmpty: boolean;
  loadingText: string;
  emptyText: string;
  children: React.ReactNode;
}

export function AdminViewContent({
  isLoading,
  isEmpty,
  loadingText,
  emptyText,
  children,
}: AdminViewContentProps) {
  if (isLoading && isEmpty) {
    return (
      <div className="text-center py-8 text-muted-foreground">
        {loadingText}
      </div>
    );
  }

  if (isEmpty) {
    return (
      <div className="text-center py-8 text-muted-foreground">{emptyText}</div>
    );
  }

  return <>{children}</>;
}
