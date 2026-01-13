// Admin LLM 表格组件
import type { Language, LLMModel } from "@/common/types";
import { adminLocales } from "@/common/i18n";
import { Button } from "@/libs/shadcn/ui/button";
import { Badge } from "@/libs/shadcn/ui/badge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/libs/shadcn/ui/table";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/libs/shadcn/ui/collapsible";
import { ChevronDown, ChevronRight } from "lucide-react";

interface AdminLLMTableProps {
  lang: Language;
  groupedModels: Record<string, LLMModel[]>;
  sortedGroups: string[];
  collapsedGroups: Set<string>;
  isLoading: boolean;
  onToggleGroup: (group: string) => void;
  onEdit: (model: LLMModel) => void;
  onDelete: (model: LLMModel) => void;
  getProviderLabel: (key: string) => string;
  getCategoryLabel: (key: string) => string;
  normalizeProvider: (provider: string) => string;
}

export function AdminLLMTable({
  lang,
  groupedModels,
  sortedGroups,
  collapsedGroups,
  isLoading,
  onToggleGroup,
  onEdit,
  onDelete,
  getProviderLabel,
  getCategoryLabel,
  normalizeProvider,
}: AdminLLMTableProps) {
  const t = adminLocales[lang];

  if (isLoading) {
    return (
      <div className="text-center py-8 text-muted-foreground">{t.loading}</div>
    );
  }

  return (
    <div className="space-y-4">
      {sortedGroups.map((groupKey) => {
        const groupModels = groupedModels[groupKey];
        const isCollapsed = collapsedGroups.has(groupKey);
        const groupLabel = getProviderLabel(groupKey);

        return (
          <Collapsible
            key={groupKey}
            open={!isCollapsed}
            onOpenChange={() => onToggleGroup(groupKey)}
          >
            <div className="border rounded-lg overflow-hidden">
              <CollapsibleTrigger className="w-full">
                <div className="flex items-center justify-between px-4 py-3 bg-muted/50 hover:bg-muted transition-colors">
                  <div className="flex items-center gap-3">
                    {isCollapsed ? (
                      <ChevronRight className="h-4 w-4" />
                    ) : (
                      <ChevronDown className="h-4 w-4" />
                    )}
                    <span className="font-medium">{groupLabel}</span>
                    <Badge variant="secondary">{groupModels.length}</Badge>
                  </div>
                  <div className="flex gap-2 text-xs text-muted-foreground">
                    <span>
                      {t.active}: {groupModels.filter((m) => m.isActive).length}
                    </span>
                    <span>
                      {t.free}: {groupModels.filter((m) => m.isFree).length}
                    </span>
                  </div>
                </div>
              </CollapsibleTrigger>
              <CollapsibleContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>{t.model}</TableHead>
                      <TableHead>{t.company}</TableHead>
                      <TableHead>{t.releaseDate}</TableHead>
                      <TableHead>{t.category}</TableHead>
                      <TableHead>{t.price}</TableHead>
                      <TableHead>{t.context}</TableHead>
                      <TableHead>{t.status}</TableHead>
                      <TableHead>{t.actions}</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {groupModels.map((model) => (
                      <TableRow key={model.id}>
                        <TableCell>
                          <div>
                            <div className="font-medium">
                              {model.displayName}
                            </div>
                            <code className="text-xs text-muted-foreground">
                              {model.name}
                            </code>
                          </div>
                        </TableCell>
                        <TableCell>
                          <Badge variant="outline">
                            {normalizeProvider(model.provider)}
                          </Badge>
                        </TableCell>
                        <TableCell>
                          <span className="text-xs text-muted-foreground">
                            {model.releaseDate
                              ? new Date(model.releaseDate)
                                  .toISOString()
                                  .split("T")[0]
                              : "-"}
                          </span>
                        </TableCell>
                        <TableCell>
                          {getCategoryLabel(model.category)}
                        </TableCell>
                        <TableCell>
                          {model.isFree ? (
                            <Badge variant="secondary">{t.free}</Badge>
                          ) : (
                            <span className="text-xs font-mono">
                              ${model.inputPrice} / ${model.outputPrice}
                            </span>
                          )}
                        </TableCell>
                        <TableCell>
                          <span className="text-xs">
                            {model.contextWindow
                              ? `${(model.contextWindow / 1000).toFixed(0)}K`
                              : "-"}
                          </span>
                        </TableCell>
                        <TableCell>
                          <div className="flex gap-1">
                            {model.isDefault && <Badge>{t.default}</Badge>}
                            {model.isDeprecated && (
                              <Badge variant="destructive">
                                {t.deprecated}
                              </Badge>
                            )}
                            {!model.isActive && (
                              <Badge variant="outline">{t.disabled}</Badge>
                            )}
                            {model.isActive && !model.isDeprecated && (
                              <Badge variant="secondary">{t.active}</Badge>
                            )}
                          </div>
                        </TableCell>
                        <TableCell>
                          <div className="flex gap-2">
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => onEdit(model)}
                            >
                              {t.edit}
                            </Button>
                            <Button
                              variant="destructive"
                              size="sm"
                              onClick={() => onDelete(model)}
                            >
                              {t.delete}
                            </Button>
                          </div>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </CollapsibleContent>
            </div>
          </Collapsible>
        );
      })}
    </div>
  );
}
