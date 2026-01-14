// Admin 调度任务表单弹窗组件
import type { ScheduledJob, JobType, ScheduledJobCreate } from "@/common/types";
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import { Button } from "@/libs/shadcn/ui/button";
import { Input } from "@/libs/shadcn/ui/input";
import { Textarea } from "@/libs/shadcn/ui/textarea";
import { Switch } from "@/libs/shadcn/ui/switch";
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

interface AdminSchedulerFormDialogProps {
  open: boolean;
  selectedJob: ScheduledJob | null;
  jobTypes: JobType[];
  formData: ScheduledJobCreate;
  isSubmitting: boolean;
  onFormDataChange: (data: ScheduledJobCreate) => void;
  onSave: () => void;
  onClose: () => void;
}

export function AdminSchedulerFormDialog({
  open,
  selectedJob,
  jobTypes,
  formData,
  isSubmitting,
  onFormDataChange,
  onSave,
  onClose,
}: AdminSchedulerFormDialogProps) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  const parametersStr = JSON.stringify(formData.parameters || {}, null, 2);

  const handleParametersChange = (value: string) => {
    try {
      const parsed = JSON.parse(value);
      onFormDataChange({ ...formData, parameters: parsed });
    } catch {
      onFormDataChange({ ...formData, parameters: {} });
    }
  };

  return (
    <Dialog open={open} onOpenChange={(o) => !o && onClose()}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>{selectedJob ? t.editJob : t.addJob}</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <div>
            <label className="text-sm font-medium">{t.jobName}</label>
            <Input
              value={formData.name}
              onChange={(e) =>
                onFormDataChange({ ...formData, name: e.target.value })
              }
            />
          </div>
          <div>
            <label className="text-sm font-medium">{t.description}</label>
            <Input
              value={formData.description}
              onChange={(e) =>
                onFormDataChange({ ...formData, description: e.target.value })
              }
            />
          </div>
          <div>
            <label className="text-sm font-medium">{t.jobType}</label>
            <Select
              value={formData.jobType}
              onValueChange={(v) =>
                onFormDataChange({ ...formData, jobType: v })
              }
              disabled={!!selectedJob}
            >
              <SelectTrigger>
                <SelectValue placeholder={t.jobType} />
              </SelectTrigger>
              <SelectContent>
                {jobTypes.map((jt) => (
                  <SelectItem key={jt.type} value={jt.type}>
                    {lang === "zh" ? jt.nameZh : jt.nameEn}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          <div>
            <label className="text-sm font-medium">{t.cronExpression}</label>
            <Input
              value={formData.cronExpression}
              onChange={(e) =>
                onFormDataChange({
                  ...formData,
                  cronExpression: e.target.value,
                })
              }
              placeholder="0 0 * * *"
            />
            <p className="text-xs text-muted-foreground mt-1">{t.cronHelp}</p>
          </div>
          <div>
            <label className="text-sm font-medium">{t.parameters}</label>
            <Textarea
              value={parametersStr}
              onChange={(e) => handleParametersChange(e.target.value)}
              rows={4}
              placeholder="{}"
            />
          </div>
          <div className="flex items-center gap-2">
            <Switch
              checked={formData.isActive}
              onCheckedChange={(v) =>
                onFormDataChange({ ...formData, isActive: v })
              }
            />
            <label className="text-sm">{t.enabled}</label>
          </div>
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={onClose}>
            {t.cancel}
          </Button>
          <Button onClick={onSave} disabled={isSubmitting}>
            {isSubmitting ? t.loading : t.save}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
