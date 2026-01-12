import { Routes, Route, Navigate } from "react-router-dom";
import { AdminAuthProvider } from "./modules/admin/context/AdminAuthContext";
import {
  AdminSettingsProvider,
  useAdminSettings,
} from "./modules/admin/context/AdminSettingsContext";
import AdminRoute from "./modules/admin/components/AdminRoute";
import AdminLayout from "./modules/admin/components/AdminLayout";
import {
  DashboardView,
  DomainsView,
  PromptsView,
  QuestionsView,
  CrawlersView,
  AnalyticsView,
  LoginView,
  UsersView,
  ConversationsView,
  SubscriptionsView,
  RecommendationsView,
  ConfigView,
  SkillsView,
  DataSourcesView,
  LLMView,
  RetrievalView,
  SchedulerView,
  AgentFrameworksView,
} from "./views/admin";
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
