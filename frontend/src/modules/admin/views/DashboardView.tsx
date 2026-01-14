// Admin 仪表盘页面
import { useDashboard } from "../hooks/useDashboard";
import { AdminDashboardHeader } from "../components/AdminDashboardHeader";
import { AdminDashboardStats } from "../components/AdminDashboardStats";
import { AdminDashboardCharts } from "../components/AdminDashboardCharts";
import {
  AdminViewContainer,
  AdminViewContent,
} from "../components/AdminViewLayout";

export default function DashboardView() {
  const { summary, isLoading } = useDashboard();

  return (
    <AdminViewContainer>
      <AdminDashboardHeader />
      <AdminViewContent isLoading={isLoading} isEmpty={false}>
        <AdminDashboardStats summary={summary} />
        <AdminDashboardCharts summary={summary} />
      </AdminViewContent>
    </AdminViewContainer>
  );
}
