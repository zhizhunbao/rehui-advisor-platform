// Admin 领域表单弹窗
import { useState, useEffect } from "react";
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import type {
  Domain,
  DomainCategory,
  CreateDomainDto,
  UpdateDomainDto,
} from "@/common/types";
import { Button } from "@/libs/shadcn/ui/button";
import { Input } from "@/libs/shadcn/ui/input";
import { Textarea } from "@/libs/shadcn/ui/textarea";
import { Badge } from "@/libs/shadcn/ui/badge";
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
import { X } from "lucide-react";

interface Props {
  domain: Domain | null;
  categories: DomainCategory[];
  open: boolean;
  onSave: (data: CreateDomainDto | UpdateDomainDto) => Promise<void>;
  onClose: () => void;
}

export function AdminDomainFormDialog({
  domain,
  categories,
  open,
  onSave,
  onClose,
}: Props) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];
  const [formData, setFormData] = useState<CreateDomainDto>({
    code: "",
    name: "",
    nameEn: "",
    description: "",
    descriptionEn: "",
    icon: "✈️",
    color: "bg-violet-600",
    promptTemplateId: "",
    categoryId: "",
    sortOrder: 0,
    discoveryKeywords: [],
  });
  const [isLoading, setIsLoading] = useState(false);
  const [newKeyword, setNewKeyword] = useState("");

  useEffect(() => {
    if (domain) {
      setFormData({
        code: domain.code,
        name: domain.name,
        nameEn: domain.nameEn,
        description: domain.description,
        descriptionEn: domain.descriptionEn,
        icon: domain.icon,
        color: domain.color,
        promptTemplateId: domain.promptTemplateId || "",
        categoryId: domain.categoryId,
        sortOrder: domain.sortOrder,
        discoveryKeywords: domain.discoveryKeywords || [],
      });
    } else {
      setFormData({
        code: "",
        name: "",
        nameEn: "",
        description: "",
        descriptionEn: "",
        icon: "✈️",
        color: "bg-violet-600",
        promptTemplateId: "",
        categoryId: categories[0]?.id || "",
        sortOrder: 0,
        discoveryKeywords: [],
      });
    }
    setNewKeyword("");
  }, [domain, open, categories]);

  const handleAddKeyword = () => {
    const keyword = newKeyword.trim();
    if (keyword && !formData.discoveryKeywords.includes(keyword)) {
      setFormData({
        ...formData,
        discoveryKeywords: [...formData.discoveryKeywords, keyword],
      });
      setNewKeyword("");
    }
  };

  const handleRemoveKeyword = (keyword: string) => {
    setFormData({
      ...formData,
      discoveryKeywords: formData.discoveryKeywords.filter(
        (k) => k !== keyword
      ),
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      if (domain) {
        await onSave({
          name: formData.name,
          nameEn: formData.nameEn,
          description: formData.description,
          descriptionEn: formData.descriptionEn,
          icon: formData.icon,
          color: formData.color,
          promptTemplateId: formData.promptTemplateId,
          categoryId: formData.categoryId,
          isActive: domain.isActive,
          sortOrder: formData.sortOrder,
          discoveryKeywords: formData.discoveryKeywords,
        } as UpdateDomainDto);
      } else {
        await onSave(formData);
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={(o) => !o && onClose()}>
      <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>{domain ? t.editDomain : t.addDomain}</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">{t.domainCode}</label>
              <Input
                value={formData.code}
                onChange={(e) =>
                  setFormData({ ...formData, code: e.target.value })
                }
                disabled={!!domain}
                required
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">{t.category}</label>
              <Select
                value={formData.categoryId}
                onValueChange={(value) =>
                  setFormData({ ...formData, categoryId: value })
                }
              >
                <SelectTrigger>
                  <SelectValue placeholder={t.selectCategory} />
                </SelectTrigger>
                <SelectContent>
                  {categories.map((cat) => (
                    <SelectItem key={cat.id} value={cat.id}>
                      {lang === "zh" ? cat.name : cat.nameEn}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">{t.domainNameZh}</label>
              <Input
                value={formData.name}
                onChange={(e) =>
                  setFormData({ ...formData, name: e.target.value })
                }
                required
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">{t.domainNameEn}</label>
              <Input
                value={formData.nameEn}
                onChange={(e) =>
                  setFormData({ ...formData, nameEn: e.target.value })
                }
                required
              />
            </div>
          </div>
          <div className="grid grid-cols-3 gap-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">{t.domainIcon}</label>
              <Input
                value={formData.icon}
                onChange={(e) =>
                  setFormData({ ...formData, icon: e.target.value })
                }
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">{t.domainColor}</label>
              <Input
                value={formData.color}
                onChange={(e) =>
                  setFormData({ ...formData, color: e.target.value })
                }
                placeholder="bg-violet-600"
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">{t.sortOrder}</label>
              <Input
                type="number"
                value={formData.sortOrder}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    sortOrder: parseInt(e.target.value) || 0,
                  })
                }
              />
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">{t.domainDescZh}</label>
              <Textarea
                value={formData.description}
                onChange={(e) =>
                  setFormData({ ...formData, description: e.target.value })
                }
                className="h-20"
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">{t.domainDescEn}</label>
              <Textarea
                value={formData.descriptionEn}
                onChange={(e) =>
                  setFormData({ ...formData, descriptionEn: e.target.value })
                }
                className="h-20"
              />
            </div>
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium">
              {t.promptTemplate}
              {domain?.promptTemplates?.name && (
                <span className="ml-2 text-xs text-muted-foreground font-normal">
                  ({domain.promptTemplates.name})
                </span>
              )}
            </label>
            {domain?.promptTemplates?.template ? (
              <div className="space-y-4">
                <div>
                  <label className="text-xs text-muted-foreground mb-1 block">
                    {t.promptTemplateZh}
                  </label>
                  <Textarea
                    value={domain.promptTemplates.template}
                    readOnly
                    className="h-40 bg-muted/50"
                  />
                </div>
                <div>
                  <label className="text-xs text-muted-foreground mb-1 block">
                    {t.promptTemplateEn}
                  </label>
                  <Textarea
                    value={domain.promptTemplates.templateEn || ""}
                    readOnly
                    className="h-40 bg-muted/50"
                  />
                </div>
              </div>
            ) : (
              <p className="text-sm text-muted-foreground">
                {t.noPromptLinked}
              </p>
            )}
            <p className="text-xs text-muted-foreground">
              {t.promptTemplateHint}
            </p>
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium">{t.discoveryKeywords}</label>
            <div className="flex gap-2">
              <Input
                value={newKeyword}
                onChange={(e) => setNewKeyword(e.target.value)}
                placeholder={t.addKeywordPlaceholder}
                onKeyDown={(e) => {
                  if (e.key === "Enter") {
                    e.preventDefault();
                    handleAddKeyword();
                  }
                }}
              />
              <Button
                type="button"
                variant="outline"
                onClick={handleAddKeyword}
              >
                {t.add}
              </Button>
            </div>
            {formData.discoveryKeywords.length > 0 && (
              <div className="flex flex-wrap gap-2 mt-2">
                {formData.discoveryKeywords.map((keyword) => (
                  <Badge key={keyword} variant="secondary" className="gap-1">
                    {keyword}
                    <button
                      type="button"
                      onClick={() => handleRemoveKeyword(keyword)}
                      className="ml-1 hover:text-destructive"
                    >
                      <X className="h-3 w-3" />
                    </button>
                  </Badge>
                ))}
              </div>
            )}
            <p className="text-xs text-muted-foreground">
              {t.discoveryKeywordsHint}
            </p>
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
