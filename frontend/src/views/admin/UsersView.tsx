import { useState, useCallback } from "react";
import { adminLocales, type Language } from "@/common/i18n";
import { useInfiniteScroll } from "@/common/hooks";
import { LoadMoreIndicator } from "@/modules/admin/components/LoadMoreIndicator";
import { getApiBase, getAuthHeaders } from "@/modules/admin/utils/api";
import type { AdminUser } from "@/modules/admin/types/admin.types";
import { Button } from "@/libs/shadcn/ui/button";
import { Input } from "@/libs/shadcn/ui/input";
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
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/libs/shadcn/ui/select";

interface UsersViewProps {
  lang: Language;
}

const API_BASE = getApiBase();
const getHeaders = getAuthHeaders;

export default function UsersView({ lang }: UsersViewProps) {
  const t = adminLocales[lang];
  const [search, setSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");

  const fetchUsers = useCallback(
    async (page: number) => {
      const params = new URLSearchParams();
      params.set("page", page.toString());
      params.set("limit", "20");
      if (search) params.set("search", search);
      if (statusFilter && statusFilter !== "all")
        params.set("status", statusFilter);

      const res = await fetch(`${API_BASE}/admin/users?${params}`, {
        headers: getHeaders(),
      });
      const json = await res.json();
      return { data: json.data || [], total: json.meta?.total || 0 };
    },
    [search, statusFilter]
  );

  const {
    data: users,
    isLoading,
    hasMore,
    total,
    loadMoreRef,
    refresh,
  } = useInfiniteScroll<AdminUser>({ fetchFn: fetchUsers });

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    refresh();
  };

  const handleToggleStatus = async (id: string) => {
    await fetch(`${API_BASE}/admin/users/${id}/toggle-status`, {
      method: "POST",
      headers: getHeaders(),
    });
    refresh();
  };

  const getUserTypeLabel = (type: string) => {
    switch (type) {
      case "ANONYMOUS":
        return t.anonymous;
      case "REGISTERED":
        return t.registered;
      case "PREMIUM":
        return t.premium;
      default:
        return type;
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status) {
      case "ACTIVE":
        return t.active;
      case "INACTIVE":
        return t.inactive;
      case "BANNED":
        return t.banned;
      default:
        return status;
    }
  };

  const getStatusVariant = (
    status: string
  ): "default" | "secondary" | "destructive" | "outline" => {
    switch (status) {
      case "ACTIVE":
        return "default";
      case "INACTIVE":
        return "secondary";
      case "BANNED":
        return "destructive";
      default:
        return "outline";
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-foreground">{t.users}</h1>

      <form onSubmit={handleSearch} className="flex gap-4">
        <Input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder={t.search}
          className="flex-1"
        />
        <Select value={statusFilter} onValueChange={setStatusFilter}>
          <SelectTrigger className="w-40">
            <SelectValue placeholder={t.status} />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">{t.allStatus}</SelectItem>
            <SelectItem value="ACTIVE">{t.active}</SelectItem>
            <SelectItem value="INACTIVE">{t.inactive}</SelectItem>
            <SelectItem value="BANNED">{t.banned}</SelectItem>
          </SelectContent>
        </Select>
        <Button type="submit">{t.search}</Button>
      </form>

      {isLoading && users.length === 0 ? (
        <div className="text-center py-8 text-muted-foreground">
          {t.loading}
        </div>
      ) : users.length === 0 ? (
        <div className="text-center py-8 text-muted-foreground">{t.noData}</div>
      ) : (
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
                      onClick={() => handleToggleStatus(user.id)}
                    >
                      {t.toggleStatus}
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
          <LoadMoreIndicator
            loadMoreRef={loadMoreRef}
            hasMore={hasMore}
            isLoading={isLoading}
            total={total}
            count={users.length}
            lang={lang}
          />
        </>
      )}
    </div>
  );
}
