// Admin Agent 框架统计卡片
import { useAdminSettingsStore } from "@/common/stores";
import { Card, CardContent } from "@/libs/shadcn/ui/card";

interface Props {
  stats: {
    total: number;
    totalStars: number;
    active: number;
    tags: number;
  };
}

export function AdminAgentFrameworksStats({ stats }: Props) {
  const { lang } = useAdminSettingsStore();

  return (
    <div className="grid grid-cols-4 gap-4">
      <Card>
        <CardContent className="p-4">
          <div className="text-2xl font-bold">{stats.total}</div>
          <div className="text-sm text-muted-foreground">
            {lang === "zh" ? "框架总数" : "Total Frameworks"}
          </div>
        </CardContent>
      </Card>
      <Card>
        <CardContent className="p-4">
          <div className="text-2xl font-bold text-yellow-500">
            {stats.totalStars.toLocaleString()} ⭐
          </div>
          <div className="text-sm text-muted-foreground">
            {lang === "zh" ? "总 Stars" : "Total Stars"}
          </div>
        </CardContent>
      </Card>
      <Card>
        <CardContent className="p-4">
          <div className="text-2xl font-bold text-green-500">
            {stats.active}
          </div>
          <div className="text-sm text-muted-foreground">
            {lang === "zh" ? "活跃项目" : "Active"}
          </div>
        </CardContent>
      </Card>
      <Card>
        <CardContent className="p-4">
          <div className="text-2xl font-bold text-blue-500">{stats.tags}</div>
          <div className="text-sm text-muted-foreground">
            {lang === "zh" ? "标签" : "Tags"}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
