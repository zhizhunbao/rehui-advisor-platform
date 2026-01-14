// Admin 领域筛选器
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import { AdminTagFilter, type TagOption } from "./AdminTagFilter";
import { Button } from "@/libs/shadcn/ui/button";
import { Input } from "@/libs/shadcn/ui/input";
import { Card, CardContent } from "@/libs/shadcn/ui/card";

interface Props {
  search: string;
  onSearchChange: (value: string) => void;
  filterCategoryId: string;
  onFilterCategoryIdChange: (value: string) => void;
  categoryOptions: TagOption[];
  onReset: () => void;
}

export function AdminDomainsFilter({
  search,
  onSearchChange,
  filterCategoryId,
  onFilterCategoryIdChange,
  categoryOptions,
  onReset,
}: Props) {
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
        <AdminTagFilter
          label={t.category}
          options={categoryOptions}
          value={filterCategoryId}
          onChange={onFilterCategoryIdChange}
          color="violet"
        />
      </CardContent>
    </Card>
  );
}
