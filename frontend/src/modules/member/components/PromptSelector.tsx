import { useState, useEffect, useCallback } from "react";
import type { Language } from "../types";

interface Prompt {
  id: string;
  name: string;
  description: string | null;
  template: string | null;
  category: string | null;
}

interface PromptSelectorProps {
  lang: Language;
  onSelect: (prompt: Prompt) => void;
  onClose: () => void;
}

const CATEGORY_LABELS: Record<string, { zh: string; en: string }> = {
  roleplay: { zh: "角色扮演", en: "Roleplay" },
  writing: { zh: "写作创作", en: "Writing" },
  coding: { zh: "编程开发", en: "Coding" },
  business: { zh: "商业营销", en: "Business" },
  education: { zh: "教育学习", en: "Education" },
  creative: { zh: "创意设计", en: "Creative" },
  analysis: { zh: "分析研究", en: "Analysis" },
  system: { zh: "系统提示", en: "System" },
  general: { zh: "通用", en: "General" },
};

const t = {
  zh: {
    title: "选择 Prompt",
    search: "搜索...",
    allCategories: "全部分类",
    noResults: "没有找到匹配的 Prompt",
    use: "使用",
    cancel: "取消",
  },
  en: {
    title: "Select Prompt",
    search: "Search...",
    allCategories: "All Categories",
    noResults: "No matching prompts found",
    use: "Use",
    cancel: "Cancel",
  },
};

export default function PromptSelector({
  lang,
  onSelect,
  onClose,
}: PromptSelectorProps) {
  const labels = t[lang];
  const [prompts, setPrompts] = useState<Prompt[]>([]);
  const [categories, setCategories] = useState<
    { category: string; count: number }[]
  >([]);
  const [isLoading, setIsLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("");
  const [selectedPrompt, setSelectedPrompt] = useState<Prompt | null>(null);

  const API_BASE = import.meta.env.VITE_API_URL || "/api";

  const fetchPrompts = useCallback(async () => {
    setIsLoading(true);
    try {
      const params = new URLSearchParams({ limit: "50" });
      if (search) params.set("search", search);
      if (category) params.set("category", category);

      const res = await fetch(`${API_BASE}/prompts?${params}`);
      const json = await res.json();
      if (json.success) {
        setPrompts(json.data?.filter((p: Prompt) => p.template) || []);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  }, [search, category, API_BASE]);

  const fetchCategories = useCallback(async () => {
    try {
      const res = await fetch(`${API_BASE}/prompts/categories`);
      const json = await res.json();
      if (json.success) setCategories(json.data || []);
    } catch (err) {
      console.error(err);
    }
  }, [API_BASE]);

  useEffect(() => {
    fetchPrompts();
  }, [fetchPrompts]);
  useEffect(() => {
    fetchCategories();
  }, [fetchCategories]);

  const handleUse = () => {
    if (selectedPrompt) {
      onSelect(selectedPrompt);
      onClose();
    }
  };

  return (
    <div
      className="fixed inset-0 bg-black/50 flex items-center justify-center z-50"
      onClick={onClose}
    >
      <div
        className="bg-white dark:bg-gray-800 rounded-lg w-full max-w-2xl max-h-[80vh] overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="p-4 border-b dark:border-gray-700 flex items-center justify-between">
          <h2 className="text-lg font-bold">{labels.title}</h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 text-xl"
          >
            ×
          </button>
        </div>

        <div className="p-4 border-b dark:border-gray-700 flex gap-3">
          <input
            type="text"
            placeholder={labels.search}
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="flex-1 px-3 py-2 border rounded dark:bg-gray-700 dark:border-gray-600"
          />
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="px-3 py-2 border rounded dark:bg-gray-700 dark:border-gray-600"
          >
            <option value="">{labels.allCategories}</option>
            {categories.map((c) => (
              <option key={c.category} value={c.category}>
                {CATEGORY_LABELS[c.category]?.[lang] || c.category} ({c.count})
              </option>
            ))}
          </select>
        </div>

        <div className="overflow-y-auto max-h-[50vh] p-4">
          {isLoading ? (
            <div className="text-center py-8 text-gray-500">Loading...</div>
          ) : prompts.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              {labels.noResults}
            </div>
          ) : (
            <div className="space-y-2">
              {prompts.map((prompt) => (
                <div
                  key={prompt.id}
                  onClick={() => setSelectedPrompt(prompt)}
                  className={`p-3 rounded-lg cursor-pointer transition-colors ${
                    selectedPrompt?.id === prompt.id
                      ? "bg-blue-100 dark:bg-blue-900 border-2 border-blue-500"
                      : "bg-gray-50 dark:bg-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600"
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="font-medium">{prompt.name}</span>
                    <span className="text-xs px-2 py-0.5 bg-gray-200 dark:bg-gray-600 rounded">
                      {CATEGORY_LABELS[prompt.category || "general"]?.[lang] ||
                        prompt.category}
                    </span>
                  </div>
                  {prompt.description && (
                    <p className="text-sm text-gray-500 mt-1 line-clamp-1">
                      {prompt.description}
                    </p>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="p-4 border-t dark:border-gray-700 flex justify-end gap-3">
          <button
            onClick={onClose}
            className="px-4 py-2 border rounded hover:bg-gray-100 dark:hover:bg-gray-700"
          >
            {labels.cancel}
          </button>
          <button
            onClick={handleUse}
            disabled={!selectedPrompt}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
          >
            {labels.use}
          </button>
        </div>
      </div>
    </div>
  );
}
