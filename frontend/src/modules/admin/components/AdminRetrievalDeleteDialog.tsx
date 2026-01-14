// Admin 检索引擎删除确认弹窗组件
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/libs/shadcn/ui/alert-dialog";

interface AdminRetrievalDeleteDialogProps {
  deleteTarget: { id: string; name: string } | null;
  onOpenChange: (open: boolean) => void;
  onConfirm: () => void;
}

export function AdminRetrievalDeleteDialog({
  deleteTarget,
  onOpenChange,
  onConfirm,
}: AdminRetrievalDeleteDialogProps) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  return (
    <AlertDialog open={!!deleteTarget} onOpenChange={() => onOpenChange(false)}>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>{t.confirmDelete}</AlertDialogTitle>
          <AlertDialogDescription>
            {lang === "zh"
              ? `确定要删除引擎 "${deleteTarget?.name}" 吗？`
              : `Delete engine "${deleteTarget?.name}"?`}
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel>{t.cancel}</AlertDialogCancel>
          <AlertDialogAction onClick={onConfirm}>{t.delete}</AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
}
