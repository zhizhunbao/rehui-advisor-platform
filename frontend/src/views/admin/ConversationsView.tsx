import { useState, useCallback } from "react";
import { adminLocales, type Language } from "@/common/i18n";
import { useInfiniteScroll } from "@/common/hooks";
import { LoadMoreIndicator } from "@/modules/admin/components/LoadMoreIndicator";
import { getApiBase, getAuthHeaders } from "@/modules/admin/utils/api";
import type { AdminConversation } from "@/modules/admin/types/admin.types";
import { Button } from "@/libs/shadcn/ui/button";
import { Input } from "@/libs/shadcn/ui/input";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/libs/shadcn/ui/table";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/libs/shadcn/ui/dialog";

interface ConversationsViewProps {
  lang: Language;
}

const API_BASE = getApiBase();
const getHeaders = getAuthHeaders;

export default function ConversationsView({ lang }: ConversationsViewProps) {
  const t = adminLocales[lang];
  const [userId, setUserId] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [showDetail, setShowDetail] = useState(false);
  const [selectedConversation, setSelectedConversation] =
    useState<AdminConversation | null>(null);

  const fetchConversations = useCallback(
    async (page: number) => {
      const params = new URLSearchParams();
      params.set("page", page.toString());
      params.set("limit", "20");
      if (userId) params.set("userId", userId);
      if (startDate) params.set("startDate", startDate);
      if (endDate) params.set("endDate", endDate);

      const res = await fetch(`${API_BASE}/admin/conversations?${params}`, {
        headers: getHeaders(),
      });
      const json = await res.json();
      return { data: json.data || [], total: json.meta?.total || 0 };
    },
    [userId, startDate, endDate]
  );

  const {
    data: conversations,
    isLoading,
    hasMore,
    total,
    loadMoreRef,
    refresh,
  } = useInfiniteScroll<AdminConversation>({ fetchFn: fetchConversations });

  const handleFilter = (e: React.FormEvent) => {
    e.preventDefault();
    refresh();
  };

  const handleViewDetail = async (conv: AdminConversation) => {
    const res = await fetch(`${API_BASE}/admin/conversations/${conv.id}`, {
      headers: getHeaders(),
    });
    const json = await res.json();
    if (json.success) {
      setSelectedConversation(json.data);
      setShowDetail(true);
    }
  };

  const handleDelete = async (id: string) => {
    if (window.confirm(t.confirmDelete)) {
      await fetch(`${API_BASE}/admin/conversations/${id}`, {
        method: "DELETE",
        headers: getHeaders(),
      });
      refresh();
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-foreground">{t.conversations}</h1>

      <form onSubmit={handleFilter} className="flex flex-wrap gap-4">
        <Input
          type="text"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          placeholder={t.userId}
          className="w-48"
        />
        <Input
          type="date"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
          className="w-40"
        />
        <Input
          type="date"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
          className="w-40"
        />
        <Button type="submit">{t.filter}</Button>
        <Button
          type="button"
          variant="outline"
          onClick={() => {
            setUserId("");
            setStartDate("");
            setEndDate("");
          }}
        >
          {t.reset}
        </Button>
      </form>

      {isLoading && conversations.length === 0 ? (
        <div className="text-center py-8 text-muted-foreground">
          {t.loading}
        </div>
      ) : conversations.length === 0 ? (
        <div className="text-center py-8 text-muted-foreground">{t.noData}</div>
      ) : (
        <>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>{t.conversationTitle}</TableHead>
                <TableHead>{t.userId}</TableHead>
                <TableHead>{t.messageCount}</TableHead>
                <TableHead>{t.lastMessageAt}</TableHead>
                <TableHead>{t.createdAt}</TableHead>
                <TableHead>{t.actions}</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {conversations.map((conv) => (
                <TableRow key={conv.id}>
                  <TableCell>{conv.title}</TableCell>
                  <TableCell className="font-mono text-xs text-muted-foreground">
                    {conv.userId.slice(0, 8)}...
                  </TableCell>
                  <TableCell>{conv.messageCount}</TableCell>
                  <TableCell className="text-muted-foreground">
                    {new Date(conv.lastMessageAt).toLocaleString()}
                  </TableCell>
                  <TableCell className="text-muted-foreground">
                    {new Date(conv.createdAt).toLocaleDateString()}
                  </TableCell>
                  <TableCell className="space-x-2">
                    <Button
                      variant="link"
                      size="sm"
                      onClick={() => handleViewDetail(conv)}
                    >
                      {t.view}
                    </Button>
                    <Button
                      variant="link"
                      size="sm"
                      className="text-destructive"
                      onClick={() => handleDelete(conv.id)}
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
            count={conversations.length}
            lang={lang}
          />
        </>
      )}

      <Dialog open={showDetail} onOpenChange={setShowDetail}>
        <DialogContent className="max-w-2xl max-h-[80vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>
              {selectedConversation?.title || t.conversations}
            </DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            {selectedConversation?.messages?.map((msg) => (
              <div
                key={msg.id}
                className={`p-3 rounded-lg ${
                  msg.role === "user" ? "bg-primary/10" : "bg-muted"
                }`}
              >
                <div className="text-xs text-muted-foreground mb-1">
                  {msg.role === "user" ? t.user : t.assistant}
                </div>
                <div className="text-sm whitespace-pre-wrap">{msg.content}</div>
              </div>
            ))}
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}
