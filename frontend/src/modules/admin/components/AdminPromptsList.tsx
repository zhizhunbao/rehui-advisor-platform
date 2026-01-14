// Admin 提示词列表组件
import type { AdminPrompt } from "@/common/types";
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import { AdminPromptCard } from "./AdminPromptCard";
import { AdminLoadMoreIndicator } from "./AdminLoadMoreIndicator";

interface AdminPromptsListProps {
  prompts: AdminPrompt[];
  isLoading: boolean;
  hasMore: boolean;
  total: number;
  loadMoreRef: (node: HTMLDivElement | null) => void;
  onPromptClick: (prompt: AdminPrompt) => void;
  onToggle: (id: string) => void;
  getCategoryLabel: (code: string) => string;
  getSourceLabel: (code: string) => string;
}

export function AdminPromptsList({
  prompts,
  isLoading,
  hasMore,
  total,
  loadMoreRef,
  onPromptClick,
  onToggle,
  getCategoryLabel,
  getSourceLabel,
}: AdminPromptsListProps) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  if (isLoading && prompts.length === 0) {
    return (
      <div className="text-center py-8 text-muted-foreground">{t.loading}</div>
    );
  }

  if (prompts.length === 0) {
    return (
      <div className="text-center py-8 text-muted-foreground">{t.noData}</div>
    );
  }

  return (
    <>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {prompts.map((prompt) => (
          <AdminPromptCard
            key={prompt.id}
            prompt={prompt}
            onClick={() => onPromptClick(prompt)}
            onToggle={() => onToggle(prompt.id)}
            getCategoryLabel={getCategoryLabel}
            getSourceLabel={getSourceLabel}
          />
        ))}
      </div>
      <AdminLoadMoreIndicator
        loadMoreRef={loadMoreRef}
        hasMore={hasMore}
        isLoading={isLoading}
        total={total}
        count={prompts.length}
      />
    </>
  );
}
