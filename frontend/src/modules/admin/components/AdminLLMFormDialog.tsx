// Admin LLM 表单对话框组件
import { useState } from "react";
import type { LLMModelCreate, LLMModelForm } from "@/common/types";
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import {
  LLMProviderLabel,
  LLMCategoryLabel,
  LLMDeploymentTypeLabel,
  LLMCapabilities,
} from "@/common/enum";
import { Button } from "@/libs/shadcn/ui/button";
import { Input } from "@/libs/shadcn/ui/input";
import { Badge } from "@/libs/shadcn/ui/badge";
import { Switch } from "@/libs/shadcn/ui/switch";
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/libs/shadcn/ui/tabs";
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

interface AdminLLMFormDialogProps {
  open: boolean;
  isEditing: boolean;
  initialForm: LLMModelForm;
  onClose: () => void;
  onSave: (data: LLMModelCreate) => Promise<void>;
}

export function AdminLLMFormDialog({
  open,
  isEditing,
  initialForm,
  onClose,
  onSave,
}: AdminLLMFormDialogProps) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];
  const [activeTab, setActiveTab] = useState("basic");
  const [form, setForm] = useState<LLMModelForm>(initialForm);
  const [formKey, setFormKey] = useState(0);

  if (open && form !== initialForm && formKey === 0) {
    setForm(initialForm);
    setFormKey((k) => k + 1);
    setActiveTab("basic");
  }

  if (!open && formKey !== 0) {
    setFormKey(0);
  }

  const handleSave = async () => {
    const payload: LLMModelCreate = {
      name: form.name,
      displayName: form.displayName,
      provider: form.provider,
      apiEndpoint: form.apiEndpoint,
      version: form.version || undefined,
      category: form.category || undefined,
      deploymentType: form.deploymentType || undefined,
      inputPrice: form.inputPrice || undefined,
      outputPrice: form.outputPrice || undefined,
      isFree: form.isFree || undefined,
      contextWindow: form.contextWindow || undefined,
      maxOutputTokens: form.maxOutputTokens || undefined,
      capabilities:
        form.capabilities.length > 0 ? form.capabilities : undefined,
      description: form.description || undefined,
      dockerImage: form.dockerImage || undefined,
      hardwareRequirements:
        Object.keys(form.hardwareRequirements).length > 0
          ? form.hardwareRequirements
          : undefined,
      rateLimit:
        Object.keys(form.rateLimit).length > 0 ? form.rateLimit : undefined,
      latencyMs: form.latencyMs || undefined,
      qualityScore: form.qualityScore || undefined,
      license: form.license || undefined,
      releaseDate: form.releaseDate || undefined,
      isDeprecated: form.isDeprecated || undefined,
      fallbackModelId: form.fallbackModelId || null,
      isActive: form.isActive,
      isDefault: form.isDefault || undefined,
      config: Object.keys(form.config).length > 0 ? form.config : undefined,
      sortOrder: form.sortOrder || undefined,
    };
    await onSave(payload);
    onClose();
  };

  const toggleCapability = (cap: string) => {
    const caps = form.capabilities.includes(cap)
      ? form.capabilities.filter((c) => c !== cap)
      : [...form.capabilities, cap];
    setForm({ ...form, capabilities: caps });
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="max-w-3xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>{isEditing ? t.editModel : t.addModel}</DialogTitle>
        </DialogHeader>

        <Tabs value={activeTab} onValueChange={setActiveTab}>
          <TabsList className="grid grid-cols-4 w-full">
            <TabsTrigger value="basic">{t.basicInfo}</TabsTrigger>
            <TabsTrigger value="pricing">{t.pricingConfig}</TabsTrigger>
            <TabsTrigger value="capabilities">
              {t.capabilitiesConfig}
            </TabsTrigger>
            <TabsTrigger value="deployment">{t.deploymentConfig}</TabsTrigger>
          </TabsList>

          <TabsContent value="basic" className="space-y-4 mt-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium">{t.modelName}</label>
                <Input
                  value={form.name}
                  onChange={(e) => setForm({ ...form, name: e.target.value })}
                  placeholder="gpt-4o"
                />
              </div>
              <div>
                <label className="text-sm font-medium">{t.displayName}</label>
                <Input
                  value={form.displayName}
                  onChange={(e) =>
                    setForm({ ...form, displayName: e.target.value })
                  }
                  placeholder="GPT-4o"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium">{t.company}</label>
                <Select
                  value={form.provider}
                  onValueChange={(v) => setForm({ ...form, provider: v })}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {Object.entries(LLMProviderLabel).map(([value, label]) => (
                      <SelectItem key={value} value={value}>
                        {label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div>
                <label className="text-sm font-medium">{t.category}</label>
                <Select
                  value={form.category}
                  onValueChange={(v) => setForm({ ...form, category: v })}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {Object.entries(LLMCategoryLabel).map(([value, labels]) => (
                      <SelectItem key={value} value={value}>
                        {labels[lang]}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>

            <div className="flex gap-6">
              <div className="flex items-center gap-2">
                <Switch
                  checked={form.isActive}
                  onCheckedChange={(v) => setForm({ ...form, isActive: v })}
                />
                <span className="text-sm">{t.active}</span>
              </div>
              <div className="flex items-center gap-2">
                <Switch
                  checked={form.isDefault}
                  onCheckedChange={(v) => setForm({ ...form, isDefault: v })}
                />
                <span className="text-sm">{t.setAsDefault}</span>
              </div>
              <div className="flex items-center gap-2">
                <Switch
                  checked={form.isDeprecated}
                  onCheckedChange={(v) => setForm({ ...form, isDeprecated: v })}
                />
                <span className="text-sm">{t.deprecated}</span>
              </div>
            </div>
          </TabsContent>

          <TabsContent value="pricing" className="space-y-4 mt-4">
            <div className="flex items-center gap-2 mb-4">
              <Switch
                checked={form.isFree}
                onCheckedChange={(v) => setForm({ ...form, isFree: v })}
              />
              <span className="text-sm font-medium">{t.free}</span>
            </div>

            {!form.isFree && (
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium">{t.inputPrice}</label>
                  <Input
                    type="number"
                    step="0.01"
                    value={form.inputPrice}
                    onChange={(e) =>
                      setForm({
                        ...form,
                        inputPrice: parseFloat(e.target.value) || 0,
                      })
                    }
                  />
                </div>
                <div>
                  <label className="text-sm font-medium">{t.outputPrice}</label>
                  <Input
                    type="number"
                    step="0.01"
                    value={form.outputPrice}
                    onChange={(e) =>
                      setForm({
                        ...form,
                        outputPrice: parseFloat(e.target.value) || 0,
                      })
                    }
                  />
                </div>
              </div>
            )}

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium">{t.context}</label>
                <Input
                  type="number"
                  value={form.contextWindow}
                  onChange={(e) =>
                    setForm({
                      ...form,
                      contextWindow: parseInt(e.target.value) || 0,
                    })
                  }
                />
              </div>
              <div>
                <label className="text-sm font-medium">{t.maxTokens}</label>
                <Input
                  type="number"
                  value={form.maxOutputTokens}
                  onChange={(e) =>
                    setForm({
                      ...form,
                      maxOutputTokens: parseInt(e.target.value) || 0,
                    })
                  }
                />
              </div>
            </div>
          </TabsContent>

          <TabsContent value="capabilities" className="space-y-4 mt-4">
            <div className="flex flex-wrap gap-2">
              {LLMCapabilities.map((cap) => (
                <Badge
                  key={cap}
                  variant={
                    form.capabilities.includes(cap) ? "default" : "outline"
                  }
                  className="cursor-pointer"
                  onClick={() => toggleCapability(cap)}
                >
                  {cap}
                </Badge>
              ))}
            </div>
          </TabsContent>

          <TabsContent value="deployment" className="space-y-4 mt-4">
            <div>
              <label className="text-sm font-medium">{t.deploymentType}</label>
              <Select
                value={form.deploymentType}
                onValueChange={(v) => setForm({ ...form, deploymentType: v })}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {Object.entries(LLMDeploymentTypeLabel).map(
                    ([value, labels]) => (
                      <SelectItem key={value} value={value}>
                        {labels[lang]}
                      </SelectItem>
                    )
                  )}
                </SelectContent>
              </Select>
            </div>

            {form.deploymentType === "api" && (
              <div>
                <label className="text-sm font-medium">API Endpoint</label>
                <Input
                  value={form.apiEndpoint}
                  onChange={(e) =>
                    setForm({ ...form, apiEndpoint: e.target.value })
                  }
                  placeholder="https://api.openai.com/v1"
                />
              </div>
            )}

            {form.deploymentType === "local" && (
              <div>
                <label className="text-sm font-medium">Docker Image</label>
                <Input
                  value={form.dockerImage}
                  onChange={(e) =>
                    setForm({ ...form, dockerImage: e.target.value })
                  }
                  placeholder="ollama/ollama:latest"
                />
              </div>
            )}
          </TabsContent>
        </Tabs>

        <DialogFooter>
          <Button variant="outline" onClick={onClose}>
            {t.cancel}
          </Button>
          <Button onClick={handleSave}>{t.save}</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
