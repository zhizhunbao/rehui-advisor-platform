// Admin 配置表单弹窗
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import type { SystemConfig, CreateConfigDto } from "@/common/types";
import { Button } from "@/libs/shadcn/ui/button";
import { Input } from "@/libs/shadcn/ui/input";
import { Textarea } from "@/libs/shadcn/ui/textarea";
import { Checkbox } from "@/libs/shadcn/ui/checkbox";
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

interface Props {
  open: boolean;
  editingConfig: SystemConfig | null;
  formData: CreateConfigDto;
  onFormDataChange: (data: CreateConfigDto) => void;
  onSubmit: (e: React.FormEvent) => void;
  onClose: () => void;
  getCategoryLabel: (cat: string) => string;
}

export function AdminConfigFormDialog({
  open,
  editingConfig,
  formData,
  onFormDataChange,
  onSubmit,
  onClose,
  getCategoryLabel,
}: Props) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];
  const categories = ["general", "security", "notification", "payment"];

  return (
    <Dialog open={open} onOpenChange={(o) => !o && onClose()}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>
            {editingConfig ? t.editConfig : t.addConfig}
          </DialogTitle>
        </DialogHeader>
        <form onSubmit={onSubmit} className="space-y-4">
          <div className="space-y-2">
            <label className="text-sm font-medium">{t.configKey}</label>
            <Input
              value={formData.key}
              onChange={(e) =>
                onFormDataChange({ ...formData, key: e.target.value })
              }
              required
              disabled={!!editingConfig}
            />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium">{t.configValue}</label>
            <Textarea
              value={formData.value}
              onChange={(e) =>
                onFormDataChange({ ...formData, value: e.target.value })
              }
              required
              rows={3}
            />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium">{t.configCategory}</label>
            <Select
              value={formData.category}
              onValueChange={(v) =>
                onFormDataChange({ ...formData, category: v })
              }
            >
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {categories.map((cat) => (
                  <SelectItem key={cat} value={cat}>
                    {getCategoryLabel(cat)}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium">{t.configDescription}</label>
            <Input
              value={formData.description}
              onChange={(e) =>
                onFormDataChange({ ...formData, description: e.target.value })
              }
            />
          </div>
          <div className="flex items-center gap-2">
            <Checkbox
              id="isSensitive"
              checked={formData.isSensitive}
              onCheckedChange={(checked) =>
                onFormDataChange({ ...formData, isSensitive: checked === true })
              }
            />
            <label htmlFor="isSensitive" className="text-sm">
              {t.isSensitive}
            </label>
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
