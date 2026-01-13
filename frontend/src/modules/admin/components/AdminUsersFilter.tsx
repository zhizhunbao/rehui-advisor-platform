// Admin 用户筛选组件
import type { Language } from "@/common/types";
import { adminLocales } from "@/common/i18n";
import { Button } from "@/libs/shadcn/ui/button";
import { Input } from "@/libs/shadcn/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/libs/shadcn/ui/select";

interface AdminUsersFilterProps {
  lang: Language;
  search: string;
  statusFilter: string;
  onSearchChange: (value: string) => void;
  onStatusChange: (value: string) => void;
  onSearch: () => void;
}

export function AdminUsersFilter({
  lang,
  search,
  statusFilter,
  onSearchChange,
  onStatusChange,
  onSearch,
}: AdminUsersFilterProps) {
  const t = adminLocales[lang];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSearch();
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-4">
      <Input
        type="text"
        value={search}
        onChange={(e) => onSearchChange(e.target.value)}
        placeholder={t.search}
        className="flex-1"
      />
      <Select value={statusFilter} onValueChange={onStatusChange}>
        <SelectTrigger className="w-40">
          <SelectValue placeholder={t.status} />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="all">{t.allStatus}</SelectItem>
          <SelectItem value="ACTIVE">{t.active}</SelectItem>
          <SelectItem value="INACTIVE">{t.inactive}</SelectItem>
          <SelectItem value="BANNED">{t.banned}</SelectItem>
        </SelectContent>
      </Select>
      <Button type="submit">{t.search}</Button>
    </form>
  );
}
