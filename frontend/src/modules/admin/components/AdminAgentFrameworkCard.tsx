// Admin Agent 框架卡片
import type { AgentFramework } from "@/common/types";
import { Button } from "@/libs/shadcn/ui/button";
import { Badge } from "@/libs/shadcn/ui/badge";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/libs/shadcn/ui/card";

interface Props {
  framework: AgentFramework;
  onClick: () => void;
  onRefresh: () => void;
  onDelete: () => void;
}

export function AdminAgentFrameworkCard({
  framework,
  onClick,
  onRefresh,
  onDelete,
}: Props) {
  const repoName = framework.url.split("/").slice(-2).join("/");

  return (
    <Card
      className="cursor-pointer hover:shadow-lg transition-shadow"
      onClick={onClick}
    >
      <CardHeader className="pb-2">
        <div className="flex items-start justify-between">
          <CardTitle className="text-lg">{framework.name}</CardTitle>
          <Badge
            variant={framework.status === "active" ? "default" : "secondary"}
          >
            {framework.status}
          </Badge>
        </div>
        <a
          href={framework.url}
          target="_blank"
          rel="noopener noreferrer"
          className="text-sm text-muted-foreground hover:text-primary"
          onClick={(e) => e.stopPropagation()}
        >
          {repoName}
        </a>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-muted-foreground line-clamp-2 mb-3">
          {framework.description}
        </p>

        <div className="flex items-center gap-4 text-sm mb-3">
          {framework.githubStars !== undefined && (
            <span className="flex items-center gap-1">
              ⭐ {framework.githubStars.toLocaleString()}
            </span>
          )}
          {framework.githubForks !== undefined && (
            <span className="flex items-center gap-1">
              🍴 {framework.githubForks.toLocaleString()}
            </span>
          )}
          {framework.githubLanguage && (
            <span className="text-muted-foreground">
              {framework.githubLanguage}
            </span>
          )}
        </div>

        <div className="flex flex-wrap gap-1 mb-3">
          {(framework.tags || []).slice(0, 4).map((tag) => (
            <Badge key={tag} variant="outline" className="text-xs">
              {tag}
            </Badge>
          ))}
          {(framework.tags || []).length > 4 && (
            <Badge variant="outline" className="text-xs">
              +{framework.tags.length - 4}
            </Badge>
          )}
        </div>

        <div className="flex gap-2" onClick={(e) => e.stopPropagation()}>
          <Button size="sm" variant="outline" onClick={onRefresh}>
            🔄
          </Button>
          <Button size="sm" variant="destructive" onClick={onDelete}>
            🗑️
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
