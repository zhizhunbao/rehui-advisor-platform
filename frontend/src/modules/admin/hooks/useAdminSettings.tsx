// Admin 设置 Hook（基于 zustand store）
import { useAdminSettingsStore } from "@/common/stores";
import { themes, type ThemeName } from "@/common/themes";

export function useAdminSettings() {
  return useAdminSettingsStore();
}

export { themes, type ThemeName };
