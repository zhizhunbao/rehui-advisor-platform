// Admin Agent 框架筛选器
import { useAdminSettingsStore } from "@/common/stores";
import { Input } from "@/libs/shadcn/ui/input";
import { Card, CardContent } from "@/libs/shadcn/ui/card";

interface Props {
  search: string;
  onSearchChange: (value: string) => void;
}

export function AdminAgentFrameworksFilter({ search, onSearchChange }: Props) {
  const { lang } = useAdminSettingsStore();

  return (
    <Card>
      <CardContent className="p-4">
        <Input
          type="text"
          placeholder={lang === "zh" ? "搜索框架..." : "Search frameworks..."}
          value={search}
          onChange={(e) => onSearchChange(e.target.value)}
          className="w-64"
        />
      </CardContent>
    </Card>
  );
}
