// Admin 登录 Hook
import { useState, useCallback, type FormEvent } from "react";
import { useNavigate } from "react-router-dom";
import { useAdminSettingsStore, useAdminAuthStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import { adminAppService } from "../services/app.service";

const ADMIN_TOKEN_KEY = "admin_token";
const ADMIN_REFRESH_TOKEN_KEY = "admin_refresh_token";

export function useLogin() {
  const { lang } = useAdminSettingsStore();
  const { login } = useAdminAuthStore();
  const t = adminLocales[lang];
  const navigate = useNavigate();

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = useCallback(
    async (e: FormEvent) => {
      e.preventDefault();
      setError(null);
      setIsLoading(true);

      try {
        const response = await adminAppService.login(username, password);
        localStorage.setItem(ADMIN_TOKEN_KEY, response.accessToken);
        localStorage.setItem(ADMIN_REFRESH_TOKEN_KEY, response.refreshToken);
        login(response.admin);
        navigate("/admin");
      } catch (err) {
        setError(err instanceof Error ? err.message : t.loginFailed);
      } finally {
        setIsLoading(false);
      }
    },
    [username, password, login, navigate, t.loginFailed]
  );

  return {
    username,
    setUsername,
    password,
    setPassword,
    error,
    isLoading,
    handleSubmit,
  };
}
