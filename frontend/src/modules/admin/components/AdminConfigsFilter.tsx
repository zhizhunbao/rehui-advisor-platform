// Admin 配置筛选器
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/libs/shadcn/ui/select";

interface Props {
  categoryFilter: string;
  onCategoryFilterChange: (value: string) => void;
  getCategoryLabel: (cat: string) => string;
}

export function AdminConfigsFilter({
  categoryFilter,
  onCategoryFilterChange,
  getCategoryLabel,
}: Props) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];
  const categories = ["general", "security", "notification", "payment"];

  return (
    <div>
      <Select value={categoryFilter} onValueChange={onCategoryFilterChange}>
        <SelectTrigger className="w-48">
          <SelectValue placeholder={t.configCategory} />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="__all__">{t.configCategory}</SelectItem>
          {categories.map((cat) => (
            <SelectItem key={cat} value={cat}>
              {getCategoryLabel(cat)}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
}
