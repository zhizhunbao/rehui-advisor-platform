// Admin 会话详情弹窗组件
import type { Language, AdminConversation } from "@/common/types";
import { adminLocales } from "@/common/i18n";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/libs/shadcn/ui/dialog";

interface AdminConversationDetailDialogProps {
  lang: Language;
  conversation: AdminConversation | null;
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function AdminConversationDetailDialog({
  lang,
  conversation,
  open,
  onOpenChange,
}: AdminConversationDetailDialogProps) {
  const t = adminLocales[lang];

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl max-h-[80vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>{conversation?.title || t.conversations}</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          {conversation?.messages?.map((msg) => (
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
  );
}
