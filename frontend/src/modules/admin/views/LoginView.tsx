// Admin 登录页面
import { useLogin } from "../hooks/useLogin";
import { AdminLoginForm } from "../components/AdminLoginForm";

export default function LoginView() {
  const {
    username,
    setUsername,
    password,
    setPassword,
    error,
    isLoading,
    handleSubmit,
  } = useLogin();

  return (
    <AdminLoginForm
      username={username}
      password={password}
      error={error}
      isLoading={isLoading}
      onUsernameChange={setUsername}
      onPasswordChange={setPassword}
      onSubmit={handleSubmit}
    />
  );
}
