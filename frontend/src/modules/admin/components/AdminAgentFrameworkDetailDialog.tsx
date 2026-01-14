// Admin Agent 框架详情弹窗
import { useAdminSettingsStore } from "@/common/stores";
import type { AgentFramework } from "@/common/types";
import { Button } from "@/libs/shadcn/ui/button";
import { Badge } from "@/libs/shadcn/ui/badge";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/libs/shadcn/ui/dialog";

interface Props {
  framework: AgentFramework | null;
  onClose: () => void;
  onRefresh: () => void;
}

export function AdminAgentFrameworkDetailDialog({
  framework,
  onClose,
  onRefresh,
}: Props) {
  const { lang } = useAdminSettingsStore();

  if (!framework) return null;

  return (
    <Dialog open onOpenChange={onClose}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>{framework.name}</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <div>
            <a
              href={framework.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary hover:underline"
            >
              {framework.url}
            </a>
          </div>

          <p className="text-muted-foreground">{framework.description}</p>

          <div className="grid grid-cols-3 gap-4">
            <div className="text-center p-4 bg-muted rounded-lg">
              <div className="text-2xl font-bold">
                {framework.githubStars?.toLocaleString() || "-"}
              </div>
              <div className="text-sm text-muted-foreground">Stars</div>
            </div>
            <div className="text-center p-4 bg-muted rounded-lg">
              <div className="text-2xl font-bold">
                {framework.githubForks?.toLocaleString() || "-"}
              </div>
              <div className="text-sm text-muted-foreground">Forks</div>
            </div>
            <div className="text-center p-4 bg-muted rounded-lg">
              <div className="text-2xl font-bold">
                {framework.githubLanguage || "-"}
              </div>
              <div className="text-sm text-muted-foreground">Language</div>
            </div>
          </div>

          <div>
            <div className="text-sm font-medium mb-2">
              {lang === "zh" ? "标签" : "Tags"}
            </div>
            <div className="flex flex-wrap gap-2">
              {(framework.tags || []).map((tag) => (
                <Badge key={tag} variant="secondary">
                  {tag}
                </Badge>
              ))}
            </div>
          </div>

          <div className="text-sm text-muted-foreground">
            {lang === "zh" ? "最后同步" : "Last synced"}:{" "}
            {framework.lastSyncedAt
              ? new Date(framework.lastSyncedAt).toLocaleString()
              : "-"}
          </div>

          <div className="flex gap-2 justify-end">
            <Button variant="outline" onClick={onRefresh}>
              {lang === "zh" ? "刷新数据" : "Refresh"}
            </Button>
            <Button variant="outline" onClick={onClose}>
              {lang === "zh" ? "关闭" : "Close"}
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
