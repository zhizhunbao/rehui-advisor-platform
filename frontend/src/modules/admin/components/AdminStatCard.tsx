// Admin 统计卡片组件 - Props: value, label, color, icon
import { Card, CardContent } from "@/libs/shadcn/ui/card";

interface AdminStatCardProps {
  value: number | string;
  label: string;
  color?:
    | "default"
    | "green"
    | "muted"
    | "violet"
    | "rose"
    | "amber"
    | "blue"
    | "orange";
}

const colorClasses: Record<string, string> = {
  default: "text-foreground",
  green: "text-green-600 dark:text-green-400",
  muted: "text-muted-foreground",
  violet: "text-violet-600 dark:text-violet-400",
  rose: "text-rose-600 dark:text-rose-400",
  amber: "text-amber-600 dark:text-amber-400",
  blue: "text-blue-600 dark:text-blue-400",
  orange: "text-orange-600 dark:text-orange-400",
};

export function AdminStatCard({
  value,
  label,
  color = "default",
}: AdminStatCardProps) {
  return (
    <Card>
      <CardContent className="p-4">
        <div className={`text-2xl font-bold ${colorClasses[color]}`}>
          {value}
        </div>
        <div className="text-sm text-muted-foreground">{label}</div>
      </CardContent>
    </Card>
  );
}
