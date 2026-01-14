// Member 应用入口
import { ErrorBoundary } from "./common/ErrorBoundary";
import { ToastProvider } from "./common/toast";
import { useApp } from "./modules/member/hooks/useApp";
import MemberLayout from "./modules/member/components/MemberLayout";
import HomeView from "./modules/member/views/HomeView";
import ConversationView from "./modules/member/views/ConversationView";
import AuthView from "./modules/member/views/AuthView";

function MemberApp() {
  const { view, isInitialized } = useApp();

  if (!isInitialized) return null;

  const renderContent = () => {
    switch (view) {
      case "home":
        return <HomeView />;
      case "conversation":
        return <ConversationView />;
      case "login":
        return <AuthView type="login" />;
      case "register":
        return <AuthView type="register" />;
      default:
        return <HomeView />;
    }
  };

  return <MemberLayout>{renderContent()}</MemberLayout>;
}

export default function App() {
  return (
    <ErrorBoundary>
      <ToastProvider>
        <MemberApp />
      </ToastProvider>
    </ErrorBoundary>
  );
}
