// Admin 应用入口
import { Routes, Route, Navigate } from "react-router-dom";
import { ErrorBoundary } from "./common/ErrorBoundary";
import { ToastProvider } from "./common/toast";
import { useAdminApp } from "./modules/admin/hooks/useAdminApp";
import AdminRoute from "./modules/admin/components/AdminRoute";
import AdminLayout from "./modules/admin/components/AdminLayout";
import DashboardView from "./modules/admin/views/DashboardView";
import DomainsView from "./modules/admin/views/DomainsView";
import PromptsView from "./modules/admin/views/PromptsView";
import QuestionsView from "./modules/admin/views/QuestionsView";
import CrawlersView from "./modules/admin/views/CrawlersView";
import AnalyticsView from "./modules/admin/views/AnalyticsView";
import LoginView from "./modules/admin/views/LoginView";
import UsersView from "./modules/admin/views/UsersView";
import ConversationsView from "./modules/admin/views/ConversationsView";
import SubscriptionsView from "./modules/admin/views/SubscriptionsView";
import RecommendationsView from "./modules/admin/views/RecommendationsView";
import ConfigView from "./modules/admin/views/ConfigView";
import SkillsView from "./modules/admin/views/SkillsView";
import DataSourcesView from "./modules/admin/views/DataSourcesView";
import LLMView from "./modules/admin/views/LLMView";
import RetrievalView from "./modules/admin/views/RetrievalView";
import SchedulerView from "./modules/admin/views/SchedulerView";
import AgentFrameworksView from "./modules/admin/views/AgentFrameworksView";

function AdminRoutes() {
  useAdminApp();

  return (
    <Routes>
      <Route path="login" element={<LoginView />} />
      <Route
        element={
          <AdminRoute>
            <AdminLayout />
          </AdminRoute>
        }
      >
        <Route index element={<DashboardView />} />
        <Route path="domains" element={<DomainsView />} />
        <Route path="prompts" element={<PromptsView />} />
        <Route path="questions" element={<QuestionsView />} />
        <Route path="crawlers" element={<CrawlersView />} />
        <Route path="users" element={<UsersView />} />
        <Route path="conversations" element={<ConversationsView />} />
        <Route path="subscriptions" element={<SubscriptionsView />} />
        <Route path="recommendations" element={<RecommendationsView />} />
        <Route path="skills" element={<SkillsView />} />
        <Route path="data-sources" element={<DataSourcesView />} />
        <Route path="llm" element={<LLMView />} />
        <Route path="retrieval" element={<RetrievalView />} />
        <Route path="scheduler" element={<SchedulerView />} />
        <Route path="agent-frameworks" element={<AgentFrameworksView />} />
        <Route
          path="configs"
          element={
            <AdminRoute requireSuperAdmin>
              <ConfigView />
            </AdminRoute>
          }
        />
        <Route path="analytics" element={<AnalyticsView />} />
      </Route>
      <Route path="*" element={<Navigate to="/admin" replace />} />
    </Routes>
  );
}

export default function AdminApp() {
  return (
    <ErrorBoundary>
      <ToastProvider>
        <AdminRoutes />
      </ToastProvider>
    </ErrorBoundary>
  );
}
