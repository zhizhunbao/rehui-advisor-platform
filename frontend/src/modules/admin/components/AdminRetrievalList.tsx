// Admin 检索引擎列表组件
import type { RetrievalEngine } from "@/common/types";
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import {
  RetrievalEngineTypeConfig,
  RetrievalEngineTypeColor,
} from "@/common/enum";

interface AdminRetrievalListProps {
  engines: RetrievalEngine[];
  isLoading: boolean;
  onEdit: (engine: RetrievalEngine) => void;
  onSetDefault: (engineId: string) => void;
  onDelete: (engine: { id: string; name: string }) => void;
}

export function AdminRetrievalList({
  engines,
  isLoading,
  onEdit,
  onSetDefault,
  onDelete,
}: AdminRetrievalListProps) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  if (isLoading) {
    return <div className="text-center py-8 text-slate-500">{t.loading}</div>;
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {engines.map((engine) => {
        const typeConfig = RetrievalEngineTypeConfig[engine.type] || {
          icon: "📦",
          color: "slate",
        };
        return (
          <div
            key={engine.id}
            className={`bg-white dark:bg-admin-card-dark rounded-xl border border-admin-border-light dark:border-admin-border-dark hover:border-violet-500/50 transition-all ${
              !engine.isActive ? "opacity-60" : ""
            }`}
          >
            <div className="p-4">
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-center gap-2">
                  <span className="text-2xl">{typeConfig.icon}</span>
                  <div>
                    <h3 className="font-medium text-lg text-slate-900 dark:text-white flex items-center gap-2">
                      {engine.displayName}
                      {engine.isDefault && (
                        <span className="text-xs px-2 py-0.5 bg-violet-500/20 text-violet-600 dark:text-violet-400 rounded-full">
                          {t.default}
                        </span>
                      )}
                    </h3>
                    <div className="text-xs text-slate-500 dark:text-slate-400 font-mono">
                      {engine.name}
                    </div>
                  </div>
                </div>
                <span
                  className={`text-xs px-2 py-1 rounded-full ${
                    engine.isActive
                      ? "bg-green-500/20 text-green-600 dark:text-green-400"
                      : "bg-slate-500/20 text-slate-600 dark:text-slate-400"
                  }`}
                >
                  {engine.isActive ? t.active : t.inactive}
                </span>
              </div>

              {engine.description && (
                <p className="text-sm text-slate-600 dark:text-slate-400 mb-3 line-clamp-2">
                  {engine.description}
                </p>
              )}

              <div className="flex flex-wrap gap-1 mb-3">
                <span
                  className={`text-xs px-2 py-1 rounded-full ${
                    RetrievalEngineTypeColor[engine.type] || "bg-slate-500/20"
                  }`}
                >
                  {engine.type}
                </span>
              </div>

              <div className="flex items-center justify-end gap-2 pt-3 border-t border-admin-border-light dark:border-admin-border-dark">
                <button
                  onClick={() => onEdit(engine)}
                  className="text-slate-500 hover:text-slate-700 dark:hover:text-slate-300"
                  title={t.edit}
                >
                  ✏️
                </button>
                {!engine.isDefault && engine.isActive && (
                  <button
                    onClick={() => onSetDefault(engine.id)}
                    className="text-slate-500 hover:text-violet-500"
                    title={t.setDefaultEngine}
                  >
                    ⭐
                  </button>
                )}
                {!engine.isDefault && (
                  <button
                    onClick={() =>
                      onDelete({
                        id: engine.id,
                        name: engine.displayName,
                      })
                    }
                    className="text-rose-500 hover:text-rose-400"
                    title={t.delete}
                  >
                    🗑️
                  </button>
                )}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
