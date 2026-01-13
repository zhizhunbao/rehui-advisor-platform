// Admin 技能卡片组件
import type { Language, Skill } from "@/common/types";
import { adminLocales } from "@/common/i18n";
import { Badge } from "@/libs/shadcn/ui/badge";
import { Button } from "@/libs/shadcn/ui/button";
import { Card, CardContent } from "@/libs/shadcn/ui/card";

interface AdminSkillCardProps {
  skill: Skill;
  lang: Language;
  onClick: () => void;
  onToggle: () => void;
  getCategoryLabel: (code: string) => string;
  getSourceLabel: (code: string) => string;
}

const getSourceVariant = (
  src: string
): "default" | "secondary" | "destructive" | "outline" => {
  switch (src) {
    case "official":
      return "default";
    case "claude-code":
      return "secondary";
    default:
      return "outline";
  }
};

export function AdminSkillCard({
  skill,
  lang,
  onClick,
  onToggle,
  getCategoryLabel,
  getSourceLabel,
}: AdminSkillCardProps) {
  const t = adminLocales[lang];

  return (
    <Card
      className={`cursor-pointer hover:border-primary/50 transition-all ${
        !skill.isActive ? "opacity-60" : ""
      }`}
      onClick={onClick}
    >
      <CardContent className="p-4">
        <div className="flex items-start justify-between mb-2">
          <h3 className="font-medium truncate flex-1 text-foreground">
            {skill.name}
          </h3>
          <Badge variant={getSourceVariant(skill.source)} className="ml-2">
            {getSourceLabel(skill.source)}
          </Badge>
        </div>
        <p className="text-sm text-muted-foreground line-clamp-2 mb-3">
          {skill.description}
        </p>
        <div className="flex items-center justify-between">
          <Badge variant="outline">{getCategoryLabel(skill.category)}</Badge>
          <Button
            variant="ghost"
            size="sm"
            onClick={(e) => {
              e.stopPropagation();
              onToggle();
            }}
          >
            <Badge variant={skill.isActive ? "default" : "secondary"}>
              {skill.isActive ? t.active : t.inactive}
            </Badge>
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
