// Admin 订阅计划表单弹窗组件
import type { SubscriptionPlan, CreateSubscriptionDto } from "@/common/types";
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import { Button } from "@/libs/shadcn/ui/button";
import { Input } from "@/libs/shadcn/ui/input";
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

interface AdminSubscriptionFormDialogProps {
  open: boolean;
  editingPlan: SubscriptionPlan | null;
  formData: CreateSubscriptionDto;
  onFormDataChange: (data: CreateSubscriptionDto) => void;
  onSubmit: () => void;
  onClose: () => void;
}

export function AdminSubscriptionFormDialog({
  open,
  editingPlan,
  formData,
  onFormDataChange,
  onSubmit,
  onClose,
}: AdminSubscriptionFormDialogProps) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit();
  };

  return (
    <Dialog open={open} onOpenChange={(o) => !o && onClose()}>
      <DialogContent className="max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>{editingPlan ? t.editPlan : t.addPlan}</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">{t.planName}</label>
              <Input
                value={formData.name}
                onChange={(e) =>
                  onFormDataChange({ ...formData, name: e.target.value })
                }
                required
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">{t.planNameEn}</label>
              <Input
                value={formData.nameEn}
                onChange={(e) =>
                  onFormDataChange({ ...formData, nameEn: e.target.value })
                }
                required
              />
            </div>
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium">{t.planDescription}</label>
            <Textarea
              value={formData.description}
              onChange={(e) =>
                onFormDataChange({ ...formData, description: e.target.value })
              }
              rows={2}
            />
          </div>
          <div className="grid grid-cols-3 gap-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">{t.planPrice}</label>
              <Input
                type="number"
                value={formData.price}
                onChange={(e) =>
                  onFormDataChange({
                    ...formData,
                    price: Number(e.target.value),
                  })
                }
                min={0}
                step={0.01}
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">{t.planCurrency}</label>
              <Select
                value={formData.currency}
                onValueChange={(v) =>
                  onFormDataChange({ ...formData, currency: v })
                }
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="CNY">CNY</SelectItem>
                  <SelectItem value="USD">USD</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">{t.dailyQuota}</label>
              <Input
                type="number"
                value={formData.dailyQuota}
                onChange={(e) =>
                  onFormDataChange({
                    ...formData,
                    dailyQuota: Number(e.target.value),
                  })
                }
                min={0}
              />
            </div>
          </div>
          <DialogFooter>
            <Button type="button" variant="outline" onClick={onClose}>
              {t.cancel}
            </Button>
            <Button type="submit">{t.save}</Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
