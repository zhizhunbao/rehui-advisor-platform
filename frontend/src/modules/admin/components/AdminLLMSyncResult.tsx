// Admin LLM 同步结果显示组件
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import type { LLMSyncResult, LLMSyncSource } from "@/common/types";

interface Props {
  syncResult: LLMSyncResult | null;
  syncSources: LLMSyncSource[];
}

export function AdminLLMSyncResult({ syncResult, syncSources }: Props) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  return (
    <>
      {syncResult && (
        <div
          className={`p-4 rounded-lg ${
            syncResult.errors.length > 0
              ? "bg-amber-50 dark:bg-amber-950"
              : "bg-green-50 dark:bg-green-950"
          }`}
        >
          <div className="font-medium">
            {t.syncComplete}: {syncResult.synced}
          </div>
          {syncResult.errors.length > 0 && (
            <div className="text-sm text-muted-foreground mt-1">
              {t.error}: {syncResult.errors.map((e) => e.error).join(", ")}
            </div>
          )}
        </div>
      )}

      {syncSources.length > 0 && (
        <div className="text-sm text-muted-foreground">
          {t.syncSources}: {syncSources.map((s) => s.name).join(", ")}
        </div>
      )}
    </>
  );
}
