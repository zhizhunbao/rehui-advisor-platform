// Admin 检索引擎表单弹窗组件
import type {
  RetrievalEngine,
  RetrievalEngineType,
  RetrievalEngineForm,
} from "@/common/types";
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import { RetrievalEngineTypeConfig } from "@/common/enum";
import { Button } from "@/libs/shadcn/ui/button";
import { Input } from "@/libs/shadcn/ui/input";
import { Textarea } from "@/libs/shadcn/ui/textarea";
import { Switch } from "@/libs/shadcn/ui/switch";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/libs/shadcn/ui/select";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/libs/shadcn/ui/dialog";

interface AdminRetrievalFormDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  editingEngine: RetrievalEngine | null;
  engineTypes: RetrievalEngineType[];
  engineForm: RetrievalEngineForm;
  onEngineFormChange: (form: RetrievalEngineForm) => void;
  configJson: string;
  onConfigJsonChange: (json: string) => void;
  onSave: () => void;
}

export function AdminRetrievalFormDialog({
  open,
  onOpenChange,
  editingEngine,
  engineTypes,
  engineForm,
  onEngineFormChange,
  configJson,
  onConfigJsonChange,
  onSave,
}: AdminRetrievalFormDialogProps) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>
            {editingEngine ? t.editEngine : t.addEngine}
          </DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">{t.engineName}</label>
              <Input
                value={engineForm.name}
                onChange={(e) =>
                  onEngineFormChange({ ...engineForm, name: e.target.value })
                }
                placeholder="my_engine"
                disabled={!!editingEngine}
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">{t.displayName}</label>
              <Input
                value={engineForm.display_name}
                onChange={(e) =>
                  onEngineFormChange({
                    ...engineForm,
                    display_name: e.target.value,
                  })
                }
                placeholder="My Engine"
              />
            </div>
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium">{t.engineType}</label>
            <Select
              value={engineForm.type}
              onValueChange={(v) =>
                onEngineFormChange({ ...engineForm, type: v })
              }
            >
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {engineTypes.map((type) => (
                  <SelectItem key={type.type} value={type.type}>
                    {RetrievalEngineTypeConfig[type.type]?.icon || "📦"}{" "}
                    {type.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium">{t.description}</label>
            <Textarea
              value={engineForm.description}
              onChange={(e) =>
                onEngineFormChange({
                  ...engineForm,
                  description: e.target.value,
                })
              }
              rows={2}
            />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium">{t.engineConfig}</label>
            <Textarea
              value={configJson}
              onChange={(e) => onConfigJsonChange(e.target.value)}
              rows={6}
              className="font-mono text-sm"
            />
          </div>
          <div className="flex items-center gap-2">
            <Switch
              checked={engineForm.is_active}
              onCheckedChange={(checked) =>
                onEngineFormChange({ ...engineForm, is_active: checked })
              }
            />
            <label className="text-sm">{t.active}</label>
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            {t.cancel}
          </Button>
          <Button onClick={onSave}>{t.save}</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
