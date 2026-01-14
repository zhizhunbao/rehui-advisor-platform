// Admin 技能管理页面
import { useSkills } from "../hooks/useSkills";
import { AdminSkillsHeader } from "../components/AdminSkillsHeader";
import { AdminSkillsStats } from "../components/AdminSkillsStats";
import { AdminSkillsFilter } from "../components/AdminSkillsFilter";
import { AdminSkillsList } from "../components/AdminSkillsList";
import { AdminSkillDetailModal } from "../components/AdminSkillDetailModal";

export default function SkillsView() {
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
  } = useSkills();

  return (
    <>
      <AdminSkillsHeader isSyncing={isSyncing} onSync={handleSync} />

      <AdminSkillsStats stats={stats} />

      <AdminSkillsFilter
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
    </>
  );
}
