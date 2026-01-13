// Admin 提示词管理页面
import { useState } from "react";
import { adminLocales } from "@/common/i18n";
import type { Language, AdminPrompt } from "@/common/types";
import { usePrompts } from "../hooks/usePrompts";
import { AdminPromptsHeader } from "../components/AdminPromptsHeader";
import { AdminPromptsStats } from "../components/AdminPromptsStats";
import { AdminPromptsFilter } from "../components/AdminPromptsFilter";
import { AdminPromptsList } from "../components/AdminPromptsList";
import { AdminPromptDetailModal } from "../components/AdminPromptDetailModal";

export default function PromptsView({ lang }: { lang: Language }) {
  const t = adminLocales[lang];
  const {
    prompts,
    stats,
    isLoading,
    hasMore,
    total,
    loadMoreRef,
    search,
    setSearch,
    category,
    setCategory,
    source,
    setSource,
    getCategoryLabel,
    getSourceLabel,
    handleToggle,
    handleSync,
    handleReset,
    isSyncing,
  } = usePrompts(lang);

  const [selectedPrompt, setSelectedPrompt] = useState<AdminPrompt | null>(
    null
  );

  const onSync = async () => {
    const result = await handleSync();
    if (result) {
      alert(t.syncedCount.replace("{count}", String(result.synced)));
    }
  };

  return (
    <div>
      <AdminPromptsHeader lang={lang} isSyncing={isSyncing} onSync={onSync} />

      <AdminPromptsStats lang={lang} stats={stats} />

      <AdminPromptsFilter
        lang={lang}
        stats={stats}
        search={search}
        category={category}
        source={source}
        onSearchChange={setSearch}
        onCategoryChange={setCategory}
        onSourceChange={setSource}
        onReset={handleReset}
        getCategoryLabel={getCategoryLabel}
        getSourceLabel={getSourceLabel}
      />

      <AdminPromptsList
        lang={lang}
        prompts={prompts}
        isLoading={isLoading}
        hasMore={hasMore}
        total={total}
        loadMoreRef={loadMoreRef}
        onPromptClick={setSelectedPrompt}
        onToggle={handleToggle}
        getCategoryLabel={getCategoryLabel}
        getSourceLabel={getSourceLabel}
      />

      {selectedPrompt && (
        <AdminPromptDetailModal
          lang={lang}
          prompt={selectedPrompt}
          onClose={() => setSelectedPrompt(null)}
          onToggle={() => {
            handleToggle(selectedPrompt.id);
            setSelectedPrompt(null);
          }}
          getCategoryLabel={getCategoryLabel}
          getSourceLabel={getSourceLabel}
        />
      )}
    </div>
  );
}
