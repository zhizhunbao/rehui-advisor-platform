// Admin 配置表格
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import type { SystemConfig } from "@/common/types";
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

interface Props {
  configs: SystemConfig[];
  isLoading: boolean;
  onEdit: (config: SystemConfig) => void;
  onDelete: (key: string) => void;
  getCategoryLabel: (cat: string) => string;
}

export function AdminConfigsTable({
  configs,
  isLoading,
  onEdit,
  onDelete,
  getCategoryLabel,
}: Props) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  if (isLoading) {
    return (
      <div className="text-center py-8 text-muted-foreground">{t.loading}</div>
    );
  }

  if (configs.length === 0) {
    return (
      <div className="text-center py-8 text-muted-foreground">{t.noData}</div>
    );
  }

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>{t.configKey}</TableHead>
          <TableHead>{t.configValue}</TableHead>
          <TableHead>{t.configCategory}</TableHead>
          <TableHead>{t.configDescription}</TableHead>
          <TableHead>{t.isSensitive}</TableHead>
          <TableHead>{t.actions}</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {configs.map((config) => (
          <TableRow key={config.key}>
            <TableCell className="font-mono">{config.key}</TableCell>
            <TableCell className="max-w-xs truncate">
              {config.isSensitive ? "•••••••" : config.value}
            </TableCell>
            <TableCell>{getCategoryLabel(config.category)}</TableCell>
            <TableCell className="max-w-xs truncate text-muted-foreground">
              {config.description}
            </TableCell>
            <TableCell>
              {config.isSensitive && (
                <Badge variant="destructive">{t.isSensitive}</Badge>
              )}
            </TableCell>
            <TableCell className="space-x-2">
              <Button variant="link" size="sm" onClick={() => onEdit(config)}>
                {t.edit}
              </Button>
              <Button
                variant="link"
                size="sm"
                className="text-destructive"
                onClick={() => onDelete(config.key)}
              >
                {t.delete}
              </Button>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
}
