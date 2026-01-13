// Admin 技能详情弹窗组件
import type { Language, Skill } from "@/common/types";
import { adminLocales } from "@/common/i18n";
import { Badge } from "@/libs/shadcn/ui/badge";
import { Button } from "@/libs/shadcn/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/libs/shadcn/ui/dialog";

interface AdminSkillDetailModalProps {
  lang: Language;
  skill: Skill;
  onClose: () => void;
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

export function AdminSkillDetailModal({
  lang,
  skill,
  onClose,
  onToggle,
  getCategoryLabel,
  getSourceLabel,
}: AdminSkillDetailModalProps) {
  const t = adminLocales[lang];

  const handleExportMd = () => {
    const lines: string[] = [];
    lines.push(`# ${skill.name}`, "");
    lines.push(`- **Category**: ${getCategoryLabel(skill.category)}`);
    lines.push(`- **Source**: ${getSourceLabel(skill.source)}`);
    if (skill.repo) lines.push(`- **Repo**: ${skill.repo}`);
    lines.push("");
    if (skill.description)
      lines.push("## Description", "", skill.description, "");
    if (skill.content) lines.push("## Content", "", skill.content);

    const blob = new Blob([lines.join("\n")], {
      type: "text/markdown;charset=utf-8",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${skill.name}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <Dialog open={true} onOpenChange={(o) => !o && onClose()}>
      <DialogContent className="max-w-2xl max-h-[80vh] overflow-hidden flex flex-col">
        <DialogHeader>
          <DialogTitle className="truncate">{skill.name}</DialogTitle>
          <div className="flex items-center gap-2 mt-2">
            <Badge variant={getSourceVariant(skill.source)}>
              {getSourceLabel(skill.source)}
            </Badge>
            <Badge variant="outline">{getCategoryLabel(skill.category)}</Badge>
          </div>
        </DialogHeader>
        <div className="flex-1 overflow-y-auto space-y-4">
          {skill.description && (
            <div>
              <h3 className="text-sm font-medium text-muted-foreground mb-2">
                {t.skillDescription}
              </h3>
              <p className="text-foreground">{skill.description}</p>
            </div>
          )}
          {skill.repo && (
            <div>
              <h3 className="text-sm font-medium text-muted-foreground mb-2">
                {t.skillRepo}
              </h3>
              <a
                href={skill.repo}
                target="_blank"
                rel="noopener noreferrer"
                className="text-primary hover:underline break-all"
              >
                {skill.repo}
              </a>
            </div>
          )}
          {skill.content && (
            <div>
              <h3 className="text-sm font-medium text-muted-foreground mb-2">
                {t.skillContent}
              </h3>
              <pre className="bg-muted rounded-lg p-4 text-sm text-foreground overflow-x-auto whitespace-pre-wrap">
                {skill.content}
              </pre>
            </div>
          )}
        </div>
        <DialogFooter className="flex justify-between sm:justify-between gap-2">
          <div className="flex gap-2">
            <Button
              variant={skill.isActive ? "outline" : "default"}
              onClick={onToggle}
            >
              {skill.isActive ? t.inactive : t.active}
            </Button>
            <Button variant="outline" onClick={handleExportMd}>
              {t.exportMd || "导出 MD"}
            </Button>
          </div>
          <Button variant="outline" onClick={onClose}>
            {t.close}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
