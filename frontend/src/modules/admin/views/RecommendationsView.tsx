import { useState, useCallback } from "react";
import { adminLocales } from "@/common/i18n";
import type { Language } from "@/common/types";
import { useInfiniteScroll } from "@/common/hooks";
import { AdminLoadMoreIndicator } from "../components/AdminLoadMoreIndicator";
import { getApiBase, getAuthHeaders } from "@/common/helper";
import type { AdminRecommendation } from "@/common/types";
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
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/libs/shadcn/ui/select";

interface RecommendationsViewProps {
  lang: Language;
}

const API_BASE = getApiBase();
const getHeaders = getAuthHeaders;

export default function RecommendationsView({
  lang,
}: RecommendationsViewProps) {
  const t = adminLocales[lang];
  const [statusFilter, setStatusFilter] = useState("__all__");

  const fetchRecommendations = useCallback(
    async (page: number) => {
      const params = new URLSearchParams();
      params.set("page", page.toString());
      params.set("limit", "20");
      if (statusFilter && statusFilter !== "__all__")
        params.set("status", statusFilter);

      const res = await fetch(`${API_BASE}/admin/recommendations?${params}`, {
        headers: getHeaders(),
      });
      const json = await res.json();
      return { data: json.data || [], total: json.meta?.total || 0 };
    },
    [statusFilter]
  );

  const {
    data: recommendations,
    isLoading,
    hasMore,
    total,
    loadMoreRef,
    refresh,
  } = useInfiniteScroll<AdminRecommendation>({ fetchFn: fetchRecommendations });

  const handleStatusChange = async (
    id: string,
    status: "APPROVED" | "REJECTED"
  ) => {
    await fetch(`${API_BASE}/admin/recommendations/${id}`, {
      method: "PUT",
      headers: getHeaders(),
      body: JSON.stringify({ status }),
    });
    refresh();
  };

  const handleDelete = async (id: string) => {
    if (window.confirm(t.confirmDelete)) {
      await fetch(`${API_BASE}/admin/recommendations/${id}`, {
        method: "DELETE",
        headers: getHeaders(),
      });
      refresh();
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status) {
      case "PENDING":
        return t.pending;
      case "APPROVED":
        return t.approved;
      case "REJECTED":
        return t.rejected;
      default:
        return status;
    }
  };

  const getStatusVariant = (
    status: string
  ): "default" | "secondary" | "destructive" | "outline" => {
    switch (status) {
      case "PENDING":
        return "outline";
      case "APPROVED":
        return "default";
      case "REJECTED":
        return "destructive";
      default:
        return "secondary";
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-foreground">
        {t.recommendations}
      </h1>

      <div className="flex gap-4">
        <Select value={statusFilter} onValueChange={setStatusFilter}>
          <SelectTrigger className="w-48">
            <SelectValue placeholder={t.status} />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="__all__">{t.status}</SelectItem>
            <SelectItem value="PENDING">{t.pending}</SelectItem>
            <SelectItem value="APPROVED">{t.approved}</SelectItem>
            <SelectItem value="REJECTED">{t.rejected}</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {isLoading && recommendations.length === 0 ? (
        <div className="text-center py-8 text-muted-foreground">
          {t.loading}
        </div>
      ) : recommendations.length === 0 ? (
        <div className="text-center py-8 text-muted-foreground">{t.noData}</div>
      ) : (
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
                  <TableCell className="max-w-xs truncate">
                    {rec.title}
                  </TableCell>
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
                    {new Date(rec.createdAt).toLocaleDateString()}
                  </TableCell>
                  <TableCell className="space-x-2">
                    {rec.status === "PENDING" && (
                      <>
                        <Button
                          variant="link"
                          size="sm"
                          className="text-green-600"
                          onClick={() => handleStatusChange(rec.id, "APPROVED")}
                        >
                          {t.approve}
                        </Button>
                        <Button
                          variant="link"
                          size="sm"
                          className="text-destructive"
                          onClick={() => handleStatusChange(rec.id, "REJECTED")}
                        >
                          {t.reject}
                        </Button>
                      </>
                    )}
                    <Button
                      variant="link"
                      size="sm"
                      onClick={() => handleDelete(rec.id)}
                    >
                      {t.delete}
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
            count={recommendations.length}
            lang={lang}
          />
        </>
      )}
    </div>
  );
}
