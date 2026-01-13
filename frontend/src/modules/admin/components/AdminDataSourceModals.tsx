// Admin 数据源弹窗组件 - Props: lang, source/categories, onClose, onRefresh/onSubmit
import { useState } from "react";
import type { Language } from "@/common/i18n";
import type { DataSource } from "./AdminDataSourceCard";
import { adminLocales } from "@/common/i18n";

const STATUS_COLORS: Record<string, string> = {
  active: "bg-green-500/20 text-green-700 dark:text-green-400",
  archived: "bg-slate-500/20 text-slate-600 dark:text-slate-400",
  invalid: "bg-rose-500/20 text-rose-700 dark:text-rose-400",
  pending: "bg-amber-500/20 text-amber-700 dark:text-amber-400",
};

const TYPE_COLORS: Record<string, string> = {
  github: "bg-violet-500/20 text-violet-700 dark:text-violet-400",
  api: "bg-blue-500/20 text-blue-700 dark:text-blue-400",
  website: "bg-amber-500/20 text-amber-700 dark:text-amber-400",
  rss: "bg-orange-500/20 text-orange-700 dark:text-orange-400",
};

export interface Category {
  id: string;
  code: string;
  name: string;
  nameEn: string;
  count: number;
}

interface SourceDetailModalProps {
  lang: Language;
  source: DataSource;
  onClose: () => void;
  onRefresh: () => void;
}

export function AdminSourceDetailModal({
  lang,
  source,
  onClose,
  onRefresh,
}: SourceDetailModalProps) {
  const t = adminLocales[lang];

  return (
    <div
      className="fixed inset-0 bg-black/60 flex items-center justify-center z-50"
      onClick={onClose}
    >
      <div
        className="bg-white dark:bg-[#1e1e1e] rounded-xl w-full max-w-2xl max-h-[90vh] overflow-hidden border border-admin-border-light dark:border-admin-border-dark"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="p-6 border-b border-admin-border-light dark:border-admin-border-dark">
          <div className="flex items-start justify-between">
            <div>
              <h2 className="text-xl font-bold text-slate-900 dark:text-white">
                {source.name}
              </h2>
              <a
                href={source.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-violet-600 dark:text-violet-400 hover:underline"
              >
                {source.url}
              </a>
            </div>
            <button
              onClick={onClose}
              className="text-slate-400 hover:text-slate-600 dark:hover:text-white text-2xl transition-colors"
            >
              ×
            </button>
          </div>
        </div>

        <div className="p-6 overflow-y-auto max-h-[60vh]">
          <div className="grid grid-cols-2 gap-4 mb-4">
            <div>
              <label className="text-sm text-slate-500 dark:text-slate-400">
                {t.type}
              </label>
              <div>
                <span
                  className={`text-xs px-2 py-1 rounded-full ${
                    TYPE_COLORS[source.type] || "bg-slate-500/20"
                  }`}
                >
                  {source.type}
                </span>
              </div>
            </div>
            <div>
              <label className="text-sm text-slate-500 dark:text-slate-400">
                {t.status}
              </label>
              <div>
                <span
                  className={`text-xs px-2 py-1 rounded-full ${
                    STATUS_COLORS[source.status] || "bg-slate-100"
                  }`}
                >
                  {source.status}
                </span>
              </div>
            </div>
            {source.type === "github" && (
              <>
                <div>
                  <label className="text-sm text-slate-500 dark:text-slate-400">
                    {t.owner}
                  </label>
                  <div className="text-slate-900 dark:text-white">
                    {source.owner}
                  </div>
                </div>
                <div>
                  <label className="text-sm text-slate-500 dark:text-slate-400">
                    {t.repo}
                  </label>
                  <div className="text-slate-900 dark:text-white">
                    {source.repo}
                  </div>
                </div>
                <div>
                  <label className="text-sm text-slate-500 dark:text-slate-400">
                    {t.stars}
                  </label>
                  <div className="text-slate-900 dark:text-white">
                    ⭐ {source.stars?.toLocaleString()}
                  </div>
                </div>
                <div>
                  <label className="text-sm text-slate-500 dark:text-slate-400">
                    {t.forks}
                  </label>
                  <div className="text-slate-900 dark:text-white">
                    🍴 {source.forks?.toLocaleString()}
                  </div>
                </div>
              </>
            )}
            <div>
              <label className="text-sm text-slate-500 dark:text-slate-400">
                {t.category}
              </label>
              <div className="text-slate-900 dark:text-white">
                {source.category || "-"}
              </div>
            </div>
            {source.subcategory && (
              <div>
                <label className="text-sm text-slate-500 dark:text-slate-400">
                  Subcategory
                </label>
                <div className="text-slate-900 dark:text-white">
                  {source.subcategory}
                </div>
              </div>
            )}
            {source.language && (
              <div>
                <label className="text-sm text-slate-500 dark:text-slate-400">
                  {t.language}
                </label>
                <div className="text-slate-900 dark:text-white">
                  {source.language}
                </div>
              </div>
            )}
          </div>

          {source.description && (
            <div className="mb-4">
              <label className="text-sm text-slate-500 dark:text-slate-400">
                {t.description}
              </label>
              <p className="text-slate-900 dark:text-white">
                {source.description}
              </p>
            </div>
          )}

          <div className="text-xs text-slate-400 dark:text-slate-500">
            {t.lastChecked}: {source.lastCheckedAt || "-"}
          </div>
        </div>

        <div className="p-6 border-t border-admin-border-light dark:border-admin-border-dark flex justify-between">
          {source.type === "github" && (
            <button
              onClick={onRefresh}
              className="px-4 py-2 border rounded-lg hover:bg-slate-100 dark:border-admin-border-dark dark:hover:bg-admin-hover-dark dark:text-white transition-colors"
            >
              🔄 {t.refreshLink}
            </button>
          )}
          <button
            onClick={onClose}
            className="px-4 py-2 bg-violet-600 text-white rounded-lg hover:bg-violet-700 transition-colors ml-auto"
          >
            {t.close}
          </button>
        </div>
      </div>
    </div>
  );
}

interface AddSourceModalProps {
  lang: Language;
  categories: Category[];
  isLoading: boolean;
  onClose: () => void;
  onSubmit: (data: { urls: string[]; type: string; category: string }) => void;
}

export function AdminAddSourceModal({
  lang,
  categories,
  isLoading,
  onClose,
  onSubmit,
}: AddSourceModalProps) {
  const t = adminLocales[lang];
  const [urls, setUrls] = useState("");
  const [type, setType] = useState("github");
  const [category, setCategory] = useState("");

  const handleSubmit = () => {
    const urlList = urls
      .split("\n")
      .map((u) => u.trim())
      .filter((u) => u);
    if (!urlList.length) return;
    onSubmit({ urls: urlList, type, category: category || "" });
  };

  return (
    <div
      className="fixed inset-0 bg-black/60 flex items-center justify-center z-50"
      onClick={onClose}
    >
      <div
        className="bg-white dark:bg-[#1e1e1e] rounded-xl w-full max-w-lg p-6 border border-admin-border-light dark:border-admin-border-dark"
        onClick={(e) => e.stopPropagation()}
      >
        <h2 className="text-xl font-bold mb-4 text-slate-900 dark:text-white">
          {t.addSource}
        </h2>

        <div className="mb-4">
          <label className="block text-sm font-medium mb-1 text-slate-700 dark:text-slate-300">
            {t.type}
          </label>
          <select
            value={type}
            onChange={(e) => setType(e.target.value)}
            className="w-full px-3 py-2 border rounded-lg bg-white dark:bg-admin-card-dark border-admin-border-light dark:border-admin-border-dark dark:text-white"
          >
            <option value="github">GitHub</option>
            <option value="api">API</option>
            <option value="website">Website</option>
            <option value="rss">RSS</option>
          </select>
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium mb-1 text-slate-700 dark:text-slate-300">
            URLs
          </label>
          <textarea
            value={urls}
            onChange={(e) => setUrls(e.target.value)}
            rows={6}
            placeholder={
              type === "github"
                ? "https://github.com/owner/repo"
                : "https://api.example.com/v1"
            }
            className="w-full px-3 py-2 border rounded-lg bg-white dark:bg-admin-card-dark border-admin-border-light dark:border-admin-border-dark dark:text-white dark:placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-violet-500/50"
          />
        </div>

        <div className="mb-4">
          <label className="block text-sm font-medium mb-1 text-slate-700 dark:text-slate-300">
            {t.category}
          </label>
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="w-full px-3 py-2 border rounded-lg bg-white dark:bg-admin-card-dark border-admin-border-light dark:border-admin-border-dark dark:text-white"
          >
            <option value="">{t.selectCategory}</option>
            {categories.map((cat) => (
              <option key={cat.id} value={cat.id}>
                {lang === "zh" ? cat.name : cat.nameEn || cat.name}
              </option>
            ))}
          </select>
        </div>

        <div className="flex justify-end gap-3">
          <button
            onClick={onClose}
            className="px-4 py-2 border rounded-lg hover:bg-slate-100 dark:border-admin-border-dark dark:hover:bg-admin-hover-dark dark:text-white transition-colors"
          >
            {t.cancel}
          </button>
          <button
            onClick={handleSubmit}
            disabled={isLoading || !urls.trim()}
            className="px-4 py-2 bg-violet-600 text-white rounded-lg hover:bg-violet-700 disabled:opacity-50 transition-colors"
          >
            {isLoading ? t.adding : t.add}
          </button>
        </div>
      </div>
    </div>
  );
}
