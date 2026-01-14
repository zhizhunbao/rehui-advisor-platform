// Admin 提示词管理页面
import { usePrompts } from "../hooks/usePrompts";
import { AdminPromptsHeader } from "../components/AdminPromptsHeader";
import { AdminPromptsStats } from "../components/AdminPromptsStats";
import { AdminPromptsFilter } from "../components/AdminPromptsFilter";
import { AdminPromptsList } from "../components/AdminPromptsList";
import { AdminPromptDetailModal } from "../components/AdminPromptDetailModal";

export default function PromptsView() {
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
    handleToggleSelected,
    handleSync,
    handleReset,
    isSyncing,
    selectedPrompt,
    setSelectedPrompt,
  } = usePrompts();

  return (
    <>
      <AdminPromptsHeader isSyncing={isSyncing} onSync={handleSync} />

      <AdminPromptsStats stats={stats} />

      <AdminPromptsFilter
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
          prompt={selectedPrompt}
          onClose={() => setSelectedPrompt(null)}
          onToggle={handleToggleSelected}
          getCategoryLabel={getCategoryLabel}
          getSourceLabel={getSourceLabel}
        />
      )}
    </>
  );
}
