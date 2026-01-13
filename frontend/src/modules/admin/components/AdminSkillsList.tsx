// Admin 技能列表组件
import type { Language, Skill } from "@/common/types";
import { adminLocales } from "@/common/i18n";
import { AdminSkillCard } from "./AdminSkillCard";
import { AdminLoadMoreIndicator } from "./AdminLoadMoreIndicator";

interface AdminSkillsListProps {
  lang: Language;
  skills: Skill[];
  isLoading: boolean;
  hasMore: boolean;
  total: number;
  loadMoreRef: (node: HTMLDivElement | null) => void;
  onSkillClick: (skill: Skill) => void;
  onToggle: (id: string) => void;
  getCategoryLabel: (code: string) => string;
  getSourceLabel: (code: string) => string;
}

export function AdminSkillsList({
  lang,
  skills,
  isLoading,
  hasMore,
  total,
  loadMoreRef,
  onSkillClick,
  onToggle,
  getCategoryLabel,
  getSourceLabel,
}: AdminSkillsListProps) {
  const t = adminLocales[lang];

  if (isLoading && skills.length === 0) {
    return (
      <div className="text-center py-8 text-muted-foreground">{t.loading}</div>
    );
  }

  if (skills.length === 0) {
    return (
      <div className="text-center py-8 text-muted-foreground">{t.noData}</div>
    );
  }

  return (
    <>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {skills.map((skill) => (
          <AdminSkillCard
            key={skill.id}
            skill={skill}
            lang={lang}
            onClick={() => onSkillClick(skill)}
            onToggle={() => onToggle(skill.id)}
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
        count={skills.length}
        lang={lang}
      />
    </>
  );
}
