// Admin 提示词详情弹窗组件
import type { AdminPrompt } from "@/common/types";
import { useAdminSettingsStore } from "@/common/stores";
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

interface AdminPromptDetailModalProps {
  prompt: AdminPrompt;
  onClose: () => void;
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

export function AdminPromptDetailModal({
  prompt,
  onClose,
  onToggle,
  getCategoryLabel,
  getSourceLabel,
}: AdminPromptDetailModalProps) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  const handleCopyTemplate = () => {
    if (prompt.template) {
      navigator.clipboard.writeText(prompt.template);
      alert(t.copied);
    }
  };

  return (
    <Dialog open={true} onOpenChange={(o) => !o && onClose()}>
      <DialogContent className="max-w-2xl max-h-[80vh] overflow-hidden flex flex-col">
        <DialogHeader>
          <DialogTitle className="truncate">{prompt.name}</DialogTitle>
          <div className="flex items-center gap-2 mt-2">
            <Badge variant={getSourceVariant(prompt.source)}>
              {getSourceLabel(prompt.source)}
            </Badge>
            <Badge variant="outline">{getCategoryLabel(prompt.category)}</Badge>
          </div>
        </DialogHeader>

        <div className="flex-1 overflow-y-auto space-y-4">
          {prompt.description && (
            <div>
              <h3 className="text-sm font-medium text-muted-foreground mb-2">
                {t.description}
              </h3>
              <p className="text-foreground">{prompt.description}</p>
            </div>
          )}

          {prompt.repo && (
            <div>
              <h3 className="text-sm font-medium text-muted-foreground mb-2">
                {t.repo}
              </h3>
              <a
                href={prompt.repo}
                target="_blank"
                rel="noopener noreferrer"
                className="text-primary hover:underline break-all"
              >
                {prompt.repo}
              </a>
            </div>
          )}

          {prompt.template && (
            <div>
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-medium text-muted-foreground">
                  {t.template}
                </h3>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleCopyTemplate}
                >
                  {t.copy}
                </Button>
              </div>
              <pre className="bg-muted rounded-lg p-4 text-sm text-foreground overflow-x-auto whitespace-pre-wrap">
                {prompt.template}
              </pre>
            </div>
          )}
        </div>

        <DialogFooter className="flex justify-between sm:justify-between">
          <Button
            variant={prompt.isActive ? "outline" : "default"}
            onClick={onToggle}
          >
            {prompt.isActive ? t.inactive : t.active}
          </Button>
          <Button variant="outline" onClick={onClose}>
            {t.close}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
