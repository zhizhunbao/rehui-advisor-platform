// Admin 推荐管理表格组件
import type { AdminRecommendation } from "@/common/types";
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import { formatDate } from "@/common/helper";
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
import { AdminLoadMoreIndicator } from "./AdminLoadMoreIndicator";

interface AdminRecommendationsTableProps {
  recommendations: AdminRecommendation[];
  isLoading: boolean;
  hasMore: boolean;
  total: number;
  loadMoreRef: (node: HTMLDivElement | null) => void;
  onStatusChange: (id: string, status: "APPROVED" | "REJECTED") => void;
  onDelete: (id: string) => void;
  getStatusLabel: (status: string) => string;
  getStatusVariant: (
    status: string
  ) => "default" | "secondary" | "destructive" | "outline";
}

export function AdminRecommendationsTable({
  recommendations,
  isLoading,
  hasMore,
  total,
  loadMoreRef,
  onStatusChange,
  onDelete,
  getStatusLabel,
  getStatusVariant,
}: AdminRecommendationsTableProps) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  if (isLoading && recommendations.length === 0) {
    return (
      <div className="text-center py-8 text-muted-foreground">{t.loading}</div>
    );
  }

  if (recommendations.length === 0) {
    return (
      <div className="text-center py-8 text-muted-foreground">{t.noData}</div>
    );
  }

  return (
    <>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>{t.recommendationTitle}</TableHead>
            <TableHead>{t.userId}</TableHead>
            <TableHead>{t.domainId}</TableHead>
            <TableHead>{t.status}</TableHead>
            <TableHead>{t.createdAt}</TableHead>
            <TableHead>{t.actions}</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {recommendations.map((rec) => (
            <TableRow key={rec.id}>
              <TableCell className="max-w-xs truncate">{rec.title}</TableCell>
              <TableCell className="font-mono text-xs">
                {rec.userId.slice(0, 8)}...
              </TableCell>
              <TableCell>{rec.domainId}</TableCell>
              <TableCell>
                <Badge variant={getStatusVariant(rec.status)}>
                  {getStatusLabel(rec.status)}
                </Badge>
              </TableCell>
              <TableCell className="text-muted-foreground">
                {formatDate(rec.createdAt)}
              </TableCell>
              <TableCell className="space-x-2">
                {rec.status === "PENDING" && (
                  <>
                    <Button
                      variant="link"
                      size="sm"
                      className="text-green-600"
                      onClick={() => onStatusChange(rec.id, "APPROVED")}
                    >
                      {t.approve}
                    </Button>
                    <Button
                      variant="link"
                      size="sm"
                      className="text-destructive"
                      onClick={() => onStatusChange(rec.id, "REJECTED")}
                    >
                      {t.reject}
                    </Button>
                  </>
                )}
                <Button
                  variant="link"
                  size="sm"
                  onClick={() => onDelete(rec.id)}
                >
                  {t.delete}
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <AdminLoadMoreIndicator
        loadMoreRef={loadMoreRef}
        hasMore={hasMore}
        isLoading={isLoading}
        total={total}
        count={recommendations.length}
      />
    </>
  );
}
