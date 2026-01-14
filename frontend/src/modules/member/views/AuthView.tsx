// Member 认证页面
import { useAuth } from "../hooks/useAuth";
import { MemberAuthFormContainer } from "../components/MemberAuthForm";

interface AuthViewProps {
  type: "login" | "register";
}

export default function AuthView({ type }: AuthViewProps) {
  const hook = useAuth(type);

  return <MemberAuthFormContainer {...hook} />;
}
