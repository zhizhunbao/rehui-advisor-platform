// Admin 数据源卡片组件
import type { DataSource } from "@/common/types";
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import { DataSourceStatusColors, DataSourceTypeColors } from "@/common/enum";

interface AdminDataSourceCardProps {
  source: DataSource;
  onClick: () => void;
  onRefresh: () => void;
  onDelete: () => void;
}

export function AdminDataSourceCard({
  source,
  onClick,
  onRefresh,
  onDelete,
}: AdminDataSourceCardProps) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  return (
    <div
      className="bg-white dark:bg-admin-card-dark rounded-xl border border-admin-border-light dark:border-admin-border-dark hover:border-violet-500/50 transition-all cursor-pointer"
      onClick={onClick}
    >
      <div className="p-4">
        <div className="flex items-start justify-between mb-2">
          <h3
            className="font-medium text-lg truncate flex-1 text-slate-900 dark:text-white"
            title={source.name}
          >
            {source.name}
          </h3>
          <span
            className={`text-xs px-2 py-1 rounded-full ml-2 shrink-0 ${
              DataSourceStatusColors[source.status] || "bg-slate-100"
            }`}
          >
            {source.status}
          </span>
        </div>

        <div className="text-xs text-slate-500 dark:text-slate-400 mb-3 truncate">
          {source.type === "github" && source.owner
            ? `${source.owner}/${source.repo}`
            : source.url}
        </div>

        {source.description && (
          <p className="text-sm text-slate-600 dark:text-slate-400 mb-3 line-clamp-2">
            {source.description}
          </p>
        )}

        <div className="flex flex-wrap gap-1 mb-3">
          <span
            className={`text-xs px-2 py-1 rounded-full ${
              DataSourceTypeColors[source.type] || "bg-slate-500/20"
            }`}
          >
            {source.type}
          </span>
          {source.category && (
            <span className="text-xs px-2 py-1 bg-blue-500/20 text-blue-600 dark:text-blue-400 rounded-full">
              {source.category}
            </span>
          )}
          {source.subcategory && (
            <span className="text-xs px-2 py-1 bg-slate-500/20 text-slate-600 dark:text-slate-400 rounded-full">
              {source.subcategory}
            </span>
          )}
          {source.language && (
            <span className="text-xs px-2 py-1 bg-emerald-500/20 text-emerald-600 dark:text-emerald-400 rounded-full">
              {source.language}
            </span>
          )}
        </div>

        <div className="flex items-center justify-between text-sm text-slate-500 dark:text-slate-400 pt-3 border-t border-admin-border-light dark:border-admin-border-dark">
          <div className="flex items-center gap-3">
            {source.type === "github" && source.stars !== null && (
              <span title={t.stars}>⭐ {source.stars?.toLocaleString()}</span>
            )}
            {source.type === "github" && source.forks !== null && (
              <span title={t.forks}>🍴 {source.forks?.toLocaleString()}</span>
            )}
          </div>
          <div className="flex gap-2" onClick={(e) => e.stopPropagation()}>
            <a
              href={source.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-500 hover:text-blue-400"
              title={t.openLink}
            >
              🔗
            </a>
            {source.type === "github" && (
              <button
                onClick={onRefresh}
                className="text-slate-500 hover:text-slate-300"
                title={t.refreshLink}
              >
                🔄
              </button>
            )}
            <button
              onClick={onDelete}
              className="text-rose-500 hover:text-rose-400"
              title={t.delete}
            >
              🗑️
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
