import { Routes, Route, Navigate } from "react-router-dom";
import { AdminAuthProvider } from "./modules/admin/hooks/useAdminAuth";
import {
  AdminSettingsProvider,
  useAdminSettings,
} from "./modules/admin/hooks/useAdminSettings";
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
import { ErrorBoundary } from "./common/ErrorBoundary";
import { ToastProvider } from "./common/toast";

function AdminRoutes() {
  const { lang } = useAdminSettings();

  return (
    <Routes>
      <Route path="login" element={<LoginView lang={lang} />} />
      <Route
        element={
          <AdminRoute>
            <AdminLayout />
          </AdminRoute>
        }
      >
        <Route index element={<DashboardView lang={lang} />} />
        <Route path="domains" element={<DomainsView lang={lang} />} />
        <Route path="prompts" element={<PromptsView lang={lang} />} />
        <Route path="questions" element={<QuestionsView lang={lang} />} />
        <Route path="crawlers" element={<CrawlersView lang={lang} />} />
        <Route path="users" element={<UsersView lang={lang} />} />
        <Route
          path="conversations"
          element={<ConversationsView lang={lang} />}
        />
        <Route
          path="subscriptions"
          element={<SubscriptionsView lang={lang} />}
        />
        <Route
          path="recommendations"
          element={<RecommendationsView lang={lang} />}
        />
        <Route path="skills" element={<SkillsView lang={lang} />} />
        <Route path="data-sources" element={<DataSourcesView lang={lang} />} />
        <Route path="llm" element={<LLMView lang={lang} />} />
        <Route path="retrieval" element={<RetrievalView lang={lang} />} />
        <Route path="scheduler" element={<SchedulerView lang={lang} />} />
        <Route
          path="agent-frameworks"
          element={<AgentFrameworksView lang={lang} />}
        />
        <Route
          path="configs"
          element={
            <AdminRoute requireSuperAdmin>
              <ConfigView lang={lang} />
            </AdminRoute>
          }
        />
        <Route path="analytics" element={<AnalyticsView lang={lang} />} />
      </Route>
      <Route path="*" element={<Navigate to="/admin" replace />} />
    </Routes>
  );
}

export default function AdminApp() {
  return (
    <ErrorBoundary>
      <ToastProvider>
        <AdminSettingsProvider>
          <AdminAuthProvider>
            <AdminRoutes />
          </AdminAuthProvider>
        </AdminSettingsProvider>
      </ToastProvider>
    </ErrorBoundary>
  );
}
