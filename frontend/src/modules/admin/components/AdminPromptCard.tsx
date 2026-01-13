// Admin 提示词卡片组件
import type { Language, AdminPrompt } from "@/common/types";
import { adminLocales } from "@/common/i18n";
import { Badge } from "@/libs/shadcn/ui/badge";
import { Button } from "@/libs/shadcn/ui/button";
import { Card, CardContent } from "@/libs/shadcn/ui/card";

interface AdminPromptCardProps {
  prompt: AdminPrompt;
  lang: Language;
  onClick: () => void;
  onToggle: () => void;
  getCategoryLabel: (code: string) => string;
  getSourceLabel: (code: string) => string;
}

const getSourceVariant = (
  src: string
): "default" | "secondary" | "destructive" | "outline" => {
  if (src?.includes("system")) return "secondary";
  if (src?.includes("anthropic")) return "default";
  if (src?.includes("claude")) return "default";
  return "outline";
};

export function AdminPromptCard({
  prompt,
  lang,
  onClick,
  onToggle,
  getCategoryLabel,
  getSourceLabel,
}: AdminPromptCardProps) {
  const t = adminLocales[lang];

  return (
    <Card
      className={`cursor-pointer hover:border-primary/50 transition-all ${
        !prompt.isActive ? "opacity-60" : ""
      }`}
      onClick={onClick}
    >
      <CardContent className="p-4">
        <div className="flex items-start justify-between mb-2">
          <h3 className="font-medium truncate flex-1 text-foreground">
            {prompt.name}
          </h3>
          <Badge variant={getSourceVariant(prompt.source)} className="ml-2">
            {getSourceLabel(prompt.source)}
          </Badge>
        </div>
        <p className="text-sm text-muted-foreground line-clamp-2 mb-3">
          {prompt.description}
        </p>
        <div className="flex items-center justify-between">
          <Badge variant="outline">{getCategoryLabel(prompt.category)}</Badge>
          <Button
            variant="ghost"
            size="sm"
            onClick={(e) => {
              e.stopPropagation();
              onToggle();
            }}
          >
            <Badge variant={prompt.isActive ? "default" : "secondary"}>
              {prompt.isActive ? t.active : t.inactive}
            </Badge>
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
