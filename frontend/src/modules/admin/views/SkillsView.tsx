// Admin 技能管理页面
import type { Language } from "@/common/types";
import { adminLocales } from "@/common/i18n";
import { useSkills } from "../hooks/useSkills";
import { AdminSkillsHeader } from "../components/AdminSkillsHeader";
import { AdminSkillsStats } from "../components/AdminSkillsStats";
import { AdminSkillsFilter } from "../components/AdminSkillsFilter";
import { AdminSkillsList } from "../components/AdminSkillsList";
import { AdminSkillDetailModal } from "../components/AdminSkillDetailModal";

export default function SkillsView({ lang }: { lang: Language }) {
  const t = adminLocales[lang];
  const {
    skills,
    stats,
    isLoading,
    hasMore,
    total,
    loadMoreRef,
    isSyncing,
    selectedSkill,
    setSelectedSkill,
    search,
    setSearch,
    filterCategory,
    setFilterCategory,
    filterSource,
    setFilterSource,
    getCategoryLabel,
    getSourceLabel,
    handleToggle,
    handleSync,
    handleReset,
  } = useSkills(lang);

  const onSync = async () => {
    const result = await handleSync();
    if (result) {
      alert(t.syncedCount.replace("{count}", String(result.synced)));
    }
  };

  return (
    <div>
      <AdminSkillsHeader lang={lang} isSyncing={isSyncing} onSync={onSync} />

      <AdminSkillsStats lang={lang} stats={stats} />

      <AdminSkillsFilter
        lang={lang}
        stats={stats}
        search={search}
        filterCategory={filterCategory}
        filterSource={filterSource}
        onSearchChange={setSearch}
        onCategoryChange={setFilterCategory}
        onSourceChange={setFilterSource}
        onReset={handleReset}
        getCategoryLabel={getCategoryLabel}
        getSourceLabel={getSourceLabel}
      />

      <AdminSkillsList
        lang={lang}
        skills={skills}
        isLoading={isLoading}
        hasMore={hasMore}
        total={total}
        loadMoreRef={loadMoreRef}
        onSkillClick={setSelectedSkill}
        onToggle={handleToggle}
        getCategoryLabel={getCategoryLabel}
        getSourceLabel={getSourceLabel}
      />

      {selectedSkill && (
        <AdminSkillDetailModal
          lang={lang}
          skill={selectedSkill}
          onClose={() => setSelectedSkill(null)}
          onToggle={() => {
            handleToggle(selectedSkill.id);
            setSelectedSkill(null);
          }}
          getCategoryLabel={getCategoryLabel}
          getSourceLabel={getSourceLabel}
        />
      )}
    </div>
  );
}
