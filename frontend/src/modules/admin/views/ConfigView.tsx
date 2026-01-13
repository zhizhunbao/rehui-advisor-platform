import { useEffect, useState } from "react";
import { useConfigs } from "@/modules/admin/hooks";
import { adminLocales, type Language } from "@/common/i18n";
import type {
  SystemConfig,
  CreateConfigDto,
  UpdateConfigDto,
} from "@/common/types";
import { Button } from "@/libs/shadcn/ui/button";
import { Input } from "@/libs/shadcn/ui/input";
import { Textarea } from "@/libs/shadcn/ui/textarea";
import { Checkbox } from "@/libs/shadcn/ui/checkbox";
import { Badge } from "@/libs/shadcn/ui/badge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/libs/shadcn/ui/table";
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

interface ConfigViewProps {
  lang: Language;
}

export default function ConfigView({ lang }: ConfigViewProps) {
  const t = adminLocales[lang];
  const {
    configs,
    isLoading,
    fetchConfigs,
    createConfig,
    updateConfig,
    deleteConfig,
  } = useConfigs();
  const [categoryFilter, setCategoryFilter] = useState("__all__");
  const [showForm, setShowForm] = useState(false);
  const [editingConfig, setEditingConfig] = useState<SystemConfig | null>(null);
  const [formData, setFormData] = useState<CreateConfigDto>({
    key: "",
    value: "",
    category: "general",
    description: "",
    isSensitive: false,
  });

  useEffect(() => {
    fetchConfigs(categoryFilter !== "__all__" ? categoryFilter : undefined);
  }, [fetchConfigs, categoryFilter]);

  const handleEdit = (config: SystemConfig) => {
    setEditingConfig(config);
    setFormData({
      key: config.key,
      value: config.value,
      category: config.category,
      description: config.description,
      isSensitive: config.isSensitive,
    });
    setShowForm(true);
  };

  const handleCreate = () => {
    setEditingConfig(null);
    setFormData({
      key: "",
      value: "",
      category: "general",
      description: "",
      isSensitive: false,
    });
    setShowForm(true);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (editingConfig) {
      await updateConfig(editingConfig.key, {
        value: formData.value,
        category: formData.category,
        description: formData.description,
        isSensitive: formData.isSensitive,
      } as UpdateConfigDto);
    } else {
      await createConfig(formData);
    }
    setShowForm(false);
  };

  const handleDelete = async (key: string) => {
    if (window.confirm(t.confirmDelete)) {
      await deleteConfig(key);
    }
  };

  const categories = ["general", "security", "notification", "payment"];

  const getCategoryLabel = (cat: string) => {
    switch (cat) {
      case "general":
        return t.general;
      case "security":
        return t.security;
      case "notification":
        return t.notification;
      case "payment":
        return t.payment;
      default:
        return cat;
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-foreground">{t.configs}</h1>
        <Button onClick={handleCreate}>{t.addConfig}</Button>
      </div>

      <div>
        <Select value={categoryFilter} onValueChange={setCategoryFilter}>
          <SelectTrigger className="w-48">
            <SelectValue placeholder={t.configCategory} />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="__all__">{t.configCategory}</SelectItem>
            {categories
              .filter((cat) => cat)
              .map((cat) => (
                <SelectItem key={cat} value={cat}>
                  {getCategoryLabel(cat)}
                </SelectItem>
              ))}
          </SelectContent>
        </Select>
      </div>

      {isLoading ? (
        <div className="text-center py-8 text-muted-foreground">
          {t.loading}
        </div>
      ) : configs.length === 0 ? (
        <div className="text-center py-8 text-muted-foreground">{t.noData}</div>
      ) : (
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>{t.configKey}</TableHead>
              <TableHead>{t.configValue}</TableHead>
              <TableHead>{t.configCategory}</TableHead>
              <TableHead>{t.configDescription}</TableHead>
              <TableHead>{t.isSensitive}</TableHead>
              <TableHead>{t.actions}</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {configs.map((config) => (
              <TableRow key={config.key}>
                <TableCell className="font-mono">{config.key}</TableCell>
                <TableCell className="max-w-xs truncate">
                  {config.isSensitive ? "•••••••�? : config.value}
                </TableCell>
                <TableCell>{getCategoryLabel(config.category)}</TableCell>
                <TableCell className="max-w-xs truncate text-muted-foreground">
                  {config.description}
                </TableCell>
                <TableCell>
                  {config.isSensitive && (
                    <Badge variant="destructive">{t.isSensitive}</Badge>
                  )}
                </TableCell>
                <TableCell className="space-x-2">
                  <Button
                    variant="link"
                    size="sm"
                    onClick={() => handleEdit(config)}
                  >
                    {t.edit}
                  </Button>
                  <Button
                    variant="link"
                    size="sm"
                    className="text-destructive"
                    onClick={() => handleDelete(config.key)}
                  >
                    {t.delete}
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      )}

      <Dialog open={showForm} onOpenChange={(o) => !o && setShowForm(false)}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>
              {editingConfig ? t.editConfig : t.addConfig}
            </DialogTitle>
          </DialogHeader>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <label className="text-sm font-medium">{t.configKey}</label>
              <Input
                value={formData.key}
                onChange={(e) =>
                  setFormData({ ...formData, key: e.target.value })
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
                  setFormData({ ...formData, value: e.target.value })
                }
                required
                rows={3}
              />
            </div>
            <div className="space-y-2">
              <label className="text-sm font-medium">{t.configCategory}</label>
              <Select
                value={formData.category}
                onValueChange={(v) => setFormData({ ...formData, category: v })}
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
              <label className="text-sm font-medium">
                {t.configDescription}
              </label>
              <Input
                value={formData.description}
                onChange={(e) =>
                  setFormData({ ...formData, description: e.target.value })
                }
              />
            </div>
            <div className="flex items-center gap-2">
              <Checkbox
                id="isSensitive"
                checked={formData.isSensitive}
                onCheckedChange={(checked) =>
                  setFormData({ ...formData, isSensitive: checked === true })
                }
              />
              <label htmlFor="isSensitive" className="text-sm">
                {t.isSensitive}
              </label>
            </div>
            <DialogFooter>
              <Button
                type="button"
                variant="outline"
                onClick={() => setShowForm(false)}
              >
                {t.cancel}
              </Button>
              <Button type="submit">{t.save}</Button>
            </DialogFooter>
          </form>
        </DialogContent>
      </Dialog>
    </div>
  );
}
