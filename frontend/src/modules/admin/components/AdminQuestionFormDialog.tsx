// Admin 问题表单弹窗组件
import { useState } from "react";
import type { Domain, CreateQuestionDto } from "@/common/types";
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import { Button } from "@/libs/shadcn/ui/button";
import { Textarea } from "@/libs/shadcn/ui/textarea";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/libs/shadcn/ui/dialog";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/libs/shadcn/ui/select";

interface AdminQuestionFormDialogProps {
  open: boolean;
  domains: Domain[];
  onSave: (data: CreateQuestionDto) => Promise<unknown>;
  onClose: () => void;
}

export function AdminQuestionFormDialog({
  open,
  domains,
  onSave,
  onClose,
}: AdminQuestionFormDialogProps) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];
  const [formData, setFormData] = useState<CreateQuestionDto>({
    domainId: domains[0]?.id ?? "",
    text: "",
    textEn: "",
    type: "single",
    options: [],
    sortOrder: 0,
  });
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      await onSave(formData);
      setFormData({
        domainId: domains[0]?.id ?? "",
        text: "",
        textEn: "",
        type: "single",
        options: [],
        sortOrder: 0,
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={(o) => !o && onClose()}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{t.addQuestion}</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <label className="text-sm font-medium">{t.domains}</label>
            <Select
              value={formData.domainId}
              onValueChange={(value) =>
                setFormData({ ...formData, domainId: value })
              }
            >
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {domains.map((d) => (
                  <SelectItem key={d.id} value={d.id}>
                    {lang === "zh" ? d.name : d.nameEn}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium">{t.questionTextZh}</label>
            <Textarea
              value={formData.text}
              onChange={(e) =>
                setFormData({ ...formData, text: e.target.value })
              }
              className="h-20"
              required
            />
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium">{t.questionTextEn}</label>
            <Textarea
              value={formData.textEn}
              onChange={(e) =>
                setFormData({ ...formData, textEn: e.target.value })
              }
              className="h-20"
              required
            />
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium">{t.questionType}</label>
            <Select
              value={formData.type}
              onValueChange={(value) =>
                setFormData({
                  ...formData,
                  type: value as "single" | "multiple" | "text",
                })
              }
            >
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="single">{t.typeSingle}</SelectItem>
                <SelectItem value="multiple">{t.typeMultiple}</SelectItem>
                <SelectItem value="text">{t.typeText}</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <DialogFooter>
            <Button type="button" variant="outline" onClick={onClose}>
              {t.cancel}
            </Button>
            <Button type="submit" disabled={isLoading}>
              {isLoading ? t.loading : t.save}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
