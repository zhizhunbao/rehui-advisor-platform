import { useState, useEffect, useCallback } from "react";
import { adminLocales, type Language } from "@/locales";
import { useDomains, useDomainCategories } from "@/modules/admin/hooks";
import type {
  Domain,
  DomainCategory,
  CreateDomainDto,
  UpdateDomainDto,
} from "@/modules/admin/types/admin.types";
import { StatCard } from "@/modules/admin/components/StatCard";
import {
  TagFilter,
  type TagOption,
} from "@/modules/admin/components/TagFilter";
import { Button } from "@/libs/shadcn/ui/button";
import { Input } from "@/libs/shadcn/ui/input";
import { Textarea } from "@/libs/shadcn/ui/textarea";
import { Badge } from "@/libs/shadcn/ui/badge";
import { Card, CardContent } from "@/libs/shadcn/ui/card";
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

interface DomainsViewProps {
  lang: Language;
}

export default function DomainsView({ lang }: DomainsViewProps) {
  const t = adminLocales[lang];
  const { categories, isLoading: categoriesLoading } = useDomainCategories();
  const {
    domains,
    isLoading: domainsLoading,
    createDomain,
    updateDomain,
  } = useDomains();

  const [search, setSearch] = useState("");
  const [filterCategoryId, setFilterCategoryId] = useState<string>("__all__");
  const [editingDomain, setEditingDomain] = useState<Domain | null>(null);
  const [isCreatingDomain, setIsCreatingDomain] = useState(false);

  const isGroupedMode = !search && filterCategoryId === "__all__";

  const getCategoryName = useCallback(
    (categoryId: string) => {
      const category = categories.find((c) => c.id === categoryId);
      if (!category) return t.uncategorized;
      return lang === "zh" ? category.name : category.nameEn;
    },
    [categories, lang, t.uncategorized]
  );

  // 构建分类标签选项
  const categoryOptions: TagOption[] = categories.map((cat) => ({
    value: cat.id,
    label: lang === "zh" ? cat.name : cat.nameEn,
    count: domains.filter((d) => d.categoryId === cat.id).length,
  }));

  const filteredDomains = domains.filter((d) => {
    const matchCategory =
      filterCategoryId === "__all__" || d.categoryId === filterCategoryId;
    const matchSearch =
      !search ||
      d.name.toLowerCase().includes(search.toLowerCase()) ||
      d.nameEn.toLowerCase().includes(search.toLowerCase()) ||
      d.code.toLowerCase().includes(search.toLowerCase());
    return matchCategory && matchSearch;
  });

  // 按分类分组
  const groupedDomains = categories
    .filter((cat) => domains.some((d) => d.categoryId === cat.id))
    .map((cat) => ({
      category: cat,
      domains: domains.filter((d) => d.categoryId === cat.id),
    }));

  // 统计数据
  const stats = {
    total: domains.length,
    active: domains.filter((d) => d.isActive).length,
    inactive: domains.filter((d) => !d.isActive).length,
    categories: categories.length,
  };

  const handleSaveDomain = async (data: CreateDomainDto | UpdateDomainDto) => {
    if (editingDomain) {
      await updateDomain(editingDomain.id, data as UpdateDomainDto);
      setEditingDomain(null);
    } else {
      await createDomain(data as CreateDomainDto);
      setIsCreatingDomain(false);
    }
  };

  const handleToggle = async (domain: Domain) => {
    await updateDomain(domain.id, {
      name: domain.name,
      nameEn: domain.nameEn,
      description: domain.description,
      descriptionEn: domain.descriptionEn,
      icon: domain.icon,
      color: domain.color,
      promptTemplateId: domain.promptTemplateId,
      categoryId: domain.categoryId,
      isActive: !domain.isActive,
      sortOrder: domain.sortOrder,
      discoveryKeywords: domain.discoveryKeywords || [],
    });
  };

  const handleReset = () => {
    setSearch("");
    setFilterCategoryId("__all__");
  };

  const isLoading = categoriesLoading || domainsLoading;

  if (isLoading && !domains.length) {
    return (
      <div className="flex items-center justify-center h-full text-muted-foreground">
        {t.loading}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-foreground">{t.domains}</h1>
        <Button onClick={() => setIsCreatingDomain(true)}>{t.addDomain}</Button>
      </div>

      <div className="grid grid-cols-4 gap-4">
        <StatCard value={stats.total} label={t.total} />
        <StatCard value={stats.active} label={t.active} color="green" />
        <StatCard value={stats.inactive} label={t.inactive} color="muted" />
        <StatCard
          value={stats.categories}
          label={t.domainCategories}
          color="violet"
        />
      </div>

      <Card>
        <CardContent className="p-4 space-y-4">
          <div className="flex gap-4 items-center">
            <Input
              type="text"
              placeholder={t.search}
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-64"
            />
            <Button variant="outline" onClick={handleReset}>
              {t.reset}
            </Button>
          </div>
          <TagFilter
            lang={lang}
            label={t.category}
            options={categoryOptions}
            value={filterCategoryId}
            onChange={setFilterCategoryId}
            color="violet"
          />
        </CardContent>
      </Card>

      {isGroupedMode ? (
        <GroupedView
          lang={lang}
          groupedDomains={groupedDomains}
          getCategoryName={getCategoryName}
          onSelect={setEditingDomain}
          onToggle={handleToggle}
        />
      ) : (
        <FilteredView
          lang={lang}
          domains={filteredDomains}
          getCategoryName={getCategoryName}
          onSelect={setEditingDomain}
          onToggle={handleToggle}
        />
      )}

      <DomainModal
        lang={lang}
        domain={editingDomain}
        categories={categories}
        open={isCreatingDomain || !!editingDomain}
        onSave={handleSaveDomain}
        onClose={() => {
          setIsCreatingDomain(false);
          setEditingDomain(null);
        }}
      />
    </div>
  );
}

// ============ GroupedView ============
interface GroupedViewProps {
  lang: Language;
  groupedDomains: { category: DomainCategory; domains: Domain[] }[];
  getCategoryName: (categoryId: string) => string;
  onSelect: (domain: Domain) => void;
  onToggle: (domain: Domain) => void;
}

function GroupedView({
  lang,
  groupedDomains,
  getCategoryName,
  onSelect,
  onToggle,
}: GroupedViewProps) {
  const t = adminLocales[lang];

  if (groupedDomains.length === 0) {
    return (
      <div className="text-center text-muted-foreground py-12">{t.noData}</div>
    );
  }

  return (
    <div className="space-y-8">
      {groupedDomains.map(({ category, domains }) => (
        <Card key={category.id}>
          <CardContent className="p-6">
            <div className="flex items-center gap-2 mb-4">
              <span className="text-2xl">{category.icon}</span>
              <h2 className="text-xl font-bold text-foreground">
                {lang === "zh" ? category.name : category.nameEn}{" "}
                <span className="text-sm font-normal text-muted-foreground">
                  ({domains.length})
                </span>
              </h2>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {domains.map((domain) => (
                <DomainCard
                  key={domain.id}
                  domain={domain}
                  lang={lang}
                  categoryName={getCategoryName(domain.categoryId)}
                  onClick={() => onSelect(domain)}
                  onToggle={() => onToggle(domain)}
                />
              ))}
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}

// ============ FilteredView ============
interface FilteredViewProps {
  lang: Language;
  domains: Domain[];
  getCategoryName: (categoryId: string) => string;
  onSelect: (domain: Domain) => void;
  onToggle: (domain: Domain) => void;
}

function FilteredView({
  lang,
  domains,
  getCategoryName,
  onSelect,
  onToggle,
}: FilteredViewProps) {
  const t = adminLocales[lang];

  if (domains.length === 0) {
    return (
      <div className="text-center text-muted-foreground py-12">{t.noData}</div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
      {domains.map((domain) => (
        <DomainCard
          key={domain.id}
          domain={domain}
          lang={lang}
          categoryName={getCategoryName(domain.categoryId)}
          onClick={() => onSelect(domain)}
          onToggle={() => onToggle(domain)}
        />
      ))}
    </div>
  );
}

// ============ DomainCard ============
interface DomainCardProps {
  domain: Domain;
  lang: Language;
  categoryName: string;
  onClick: () => void;
  onToggle: () => void;
}

function DomainCard({
  domain,
  lang,
  categoryName,
  onClick,
  onToggle,
}: DomainCardProps) {
  const t = adminLocales[lang];

  // Extract clean keywords from GitHub search syntax
  const displayKeywords = (domain.discoveryKeywords || [])
    .map((kw) => {
      // Remove stars:>N, forks:>N etc. suffix
      let clean = kw.split(" ")[0];
      // Remove topic: prefix
      if (clean.startsWith("topic:")) {
        clean = clean.replace("topic:", "");
      }
      return clean;
    })
    .filter((kw, idx, arr) => kw && arr.indexOf(kw) === idx); // Remove duplicates
  const keywordsCount = displayKeywords.length;

  return (
    <Card
      className={`cursor-pointer hover:border-primary/50 transition-all ${
        !domain.isActive ? "opacity-60" : ""
      }`}
      onClick={onClick}
    >
      <CardContent className="p-4">
        <div className="flex items-start justify-between mb-2">
          <div className="flex items-center gap-2">
            <span className="text-2xl">{domain.icon}</span>
            <div>
              <h3 className="font-medium text-foreground">
                {lang === "zh" ? domain.name : domain.nameEn}
              </h3>
              <p className="text-xs text-muted-foreground font-mono">
                {domain.code}
              </p>
            </div>
          </div>
        </div>

        <p className="text-sm text-muted-foreground line-clamp-2 mb-3">
          {lang === "zh" ? domain.description : domain.descriptionEn}
        </p>

        {keywordsCount > 0 && (
          <div className="flex flex-wrap gap-1 mb-3">
            {displayKeywords.slice(0, 3).map((kw, idx) => (
              <Badge
                key={idx}
                variant="secondary"
                className="text-xs font-normal max-w-[120px] truncate"
                title={kw}
              >
                {kw}
              </Badge>
            ))}
            {keywordsCount > 3 && (
              <Badge variant="secondary" className="text-xs font-normal">
                +{keywordsCount - 3}
              </Badge>
            )}
          </div>
        )}

        <div className="flex items-center justify-between">
          <Badge variant="outline">{categoryName}</Badge>
          <Button
            variant="ghost"
            size="sm"
            onClick={(e) => {
              e.stopPropagation();
              onToggle();
            }}
          >
            <Badge variant={domain.isActive ? "default" : "secondary"}>
              {domain.isActive ? t.active : t.inactive}
            </Badge>
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}

// ============ DomainModal ============
interface DomainModalProps {
  lang: Language;
  domain: Domain | null;
  categories: DomainCategory[];
  open: boolean;
  onSave: (data: CreateDomainDto | UpdateDomainDto) => Promise<void>;
  onClose: () => void;
}

function DomainModal({
  lang,
  domain,
  categories,
  open,
  onSave,
  onClose,
}: DomainModalProps) {
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
