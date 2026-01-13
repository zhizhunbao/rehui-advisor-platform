// Admin 会话列表表格组件
import type { Language, AdminConversation } from "@/common/types";
import { adminLocales } from "@/common/i18n";
import { Button } from "@/libs/shadcn/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/libs/shadcn/ui/table";

interface AdminConversationTableProps {
  lang: Language;
  conversations: AdminConversation[];
  onViewDetail: (conversation: AdminConversation) => void;
  onDelete: (id: string) => void;
}

export function AdminConversationTable({
  lang,
  conversations,
  onViewDetail,
  onDelete,
}: AdminConversationTableProps) {
  const t = adminLocales[lang];

  const handleDelete = (id: string) => {
    if (window.confirm(t.confirmDelete)) {
      onDelete(id);
    }
  };

  return (
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
        {conversations.map((conversation) => (
          <TableRow key={conversation.id}>
            <TableCell>{conversation.title}</TableCell>
            <TableCell className="font-mono text-xs text-muted-foreground">
              {conversation.userId.slice(0, 8)}...
            </TableCell>
            <TableCell>{conversation.messageCount}</TableCell>
            <TableCell className="text-muted-foreground">
              {new Date(conversation.lastMessageAt).toLocaleString()}
            </TableCell>
            <TableCell className="text-muted-foreground">
              {new Date(conversation.createdAt).toLocaleDateString()}
            </TableCell>
            <TableCell className="space-x-2">
              <Button
                variant="link"
                size="sm"
                onClick={() => onViewDetail(conversation)}
              >
                {t.view}
              </Button>
              <Button
                variant="link"
                size="sm"
                className="text-destructive"
                onClick={() => handleDelete(conversation.id)}
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
