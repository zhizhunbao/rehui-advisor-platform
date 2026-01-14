// Admin 路由守卫组件
import { Navigate, useLocation } from "react-router-dom";
import { useAdminAuthStore } from "@/common/stores";

interface AdminRouteProps {
  children: React.ReactNode;
  requireSuperAdmin?: boolean;
}

export default function AdminRoute({
  children,
  requireSuperAdmin = false,
}: AdminRouteProps) {
  const { admin, isAuthenticated, isLoading } = useAdminAuthStore();
  const location = useLocation();

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100 dark:bg-admin-card-dark">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/admin/login" state={{ from: location }} replace />;
  }

  if (requireSuperAdmin && admin?.role !== "super_admin") {
    return <Navigate to="/admin" replace />;
  }

  return <>{children}</>;
}
