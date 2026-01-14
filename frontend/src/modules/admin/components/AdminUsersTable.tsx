// Admin 用户列表表格组件
import type { AdminUser } from "@/common/types";
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import { AdminLoadMoreIndicator } from "./AdminLoadMoreIndicator";
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

interface AdminUsersTableProps {
  users: AdminUser[];
  isLoading: boolean;
  hasMore: boolean;
  total: number;
  loadMoreRef: (node: HTMLDivElement | null) => void;
  onToggleStatus: (id: string) => void;
  getUserTypeLabel: (type: string) => string;
  getStatusLabel: (status: string) => string;
  getStatusVariant: (
    status: string
  ) => "default" | "secondary" | "destructive" | "outline";
}

export function AdminUsersTable({
  users,
  isLoading,
  hasMore,
  total,
  loadMoreRef,
  onToggleStatus,
  getUserTypeLabel,
  getStatusLabel,
  getStatusVariant,
}: AdminUsersTableProps) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  if (isLoading && users.length === 0) {
    return (
      <div className="text-center py-8 text-muted-foreground">{t.loading}</div>
    );
  }

  if (users.length === 0) {
    return (
      <div className="text-center py-8 text-muted-foreground">{t.noData}</div>
    );
  }

  return (
    <>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>{t.userEmail}</TableHead>
            <TableHead>{t.userName}</TableHead>
            <TableHead>{t.userType}</TableHead>
            <TableHead>{t.status}</TableHead>
            <TableHead>{t.searchCount}</TableHead>
            <TableHead>{t.createdAt}</TableHead>
            <TableHead>{t.actions}</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {users.map((user) => (
            <TableRow key={user.id}>
              <TableCell>{user.email}</TableCell>
              <TableCell>{user.name}</TableCell>
              <TableCell>{getUserTypeLabel(user.userType)}</TableCell>
              <TableCell>
                <Badge variant={getStatusVariant(user.status)}>
                  {getStatusLabel(user.status)}
                </Badge>
              </TableCell>
              <TableCell>{user.searchCount}</TableCell>
              <TableCell className="text-muted-foreground">
                {new Date(user.createdAt).toLocaleDateString()}
              </TableCell>
              <TableCell>
                <Button
                  variant="link"
                  size="sm"
                  onClick={() => onToggleStatus(user.id)}
                >
                  {t.toggleStatus}
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
        count={users.length}
      />
    </>
  );
}
