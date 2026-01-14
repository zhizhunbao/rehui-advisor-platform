// Admin 数据源筛选组件
import type {
  DataSourceCategory,
  DataSourceDomain,
  DataSourceTypeItem,
  DataSourceStatusItem,
  DataSourceLanguageItem,
} from "@/common/types";
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import { AdminTagFilter } from "./AdminTagFilter";
import { Button } from "@/libs/shadcn/ui/button";
import { Input } from "@/libs/shadcn/ui/input";
import { Card, CardContent } from "@/libs/shadcn/ui/card";

interface AdminDataSourcesFilterProps {
  search: string;
  onSearchChange: (value: string) => void;
  type: string;
  onTypeChange: (value: string) => void;
  categoryId: string;
  onCategoryChange: (value: string) => void;
  domainId: string;
  onDomainChange: (value: string) => void;
  status: string;
  onStatusChange: (value: string) => void;
  language: string;
  onLanguageChange: (value: string) => void;
  types: DataSourceTypeItem[];
  categories: DataSourceCategory[];
  domains: DataSourceDomain[];
  statuses: DataSourceStatusItem[];
  languages: DataSourceLanguageItem[];
  onReset: () => void;
}

export function AdminDataSourcesFilter({
  search,
  onSearchChange,
  type,
  onTypeChange,
  categoryId,
  onCategoryChange,
  domainId,
  onDomainChange,
  status,
  onStatusChange,
  language,
  onLanguageChange,
  types,
  categories,
  domains,
  statuses,
  languages,
  onReset,
}: AdminDataSourcesFilterProps) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  return (
    <Card>
      <CardContent className="p-4 space-y-4">
        <div className="flex gap-4 items-center">
          <Input
            type="text"
            placeholder={t.search}
            value={search}
            onChange={(e) => onSearchChange(e.target.value)}
            className="w-64"
          />
          <Button variant="outline" onClick={onReset}>
            {t.reset}
          </Button>
        </div>

        {types.length > 0 && (
          <AdminTagFilter
            label={t.type}
            options={types.map((item) => ({
              value: item.type,
              label: item.type,
              count: item.count,
            }))}
            value={type}
            onChange={onTypeChange}
            color="violet"
          />
        )}

        {categories.filter((c) => c.id).length > 0 && (
          <AdminTagFilter
            label={t.category}
            options={categories
              .filter((c) => c.id)
              .map((c) => ({
                value: c.id,
                label: lang === "zh" ? c.name : c.nameEn || c.name,
                count: c.count,
              }))}
            value={categoryId}
            onChange={onCategoryChange}
            color="blue"
          />
        )}

        {domains.length > 0 && (
          <AdminTagFilter
            label={t.domain}
            options={domains.map((d) => ({
              value: d.id,
              label: lang === "zh" ? d.name : d.nameEn || d.name,
              count: d.count,
            }))}
            value={domainId}
            onChange={onDomainChange}
            color="emerald"
          />
        )}

        {statuses.length > 0 && (
          <AdminTagFilter
            label={t.status}
            options={statuses.map((s) => ({
              value: s.status,
              label: s.status,
              count: s.count,
            }))}
            value={status}
            onChange={onStatusChange}
            color="amber"
          />
        )}

        {languages.length > 0 && (
          <AdminTagFilter
            label={t.language}
            options={languages.map((l) => ({
              value: l.language,
              label: l.language,
              count: l.count,
            }))}
            value={language}
            onChange={onLanguageChange}
            color="rose"
          />
        )}
      </CardContent>
    </Card>
  );
}
