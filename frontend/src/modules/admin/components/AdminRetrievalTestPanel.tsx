// Admin 检索引擎测试面板组件
import type { RetrievalEngine, RetrievalTestResult } from "@/common/types";
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import { RetrievalEngineTypeConfig } from "@/common/enum";
import { Button } from "@/libs/shadcn/ui/button";
import { Textarea } from "@/libs/shadcn/ui/textarea";
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

interface AdminRetrievalTestPanelProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  engines: RetrievalEngine[];
  testEngineId: string;
  onTestEngineIdChange: (id: string) => void;
  testQuery: string;
  onTestQueryChange: (query: string) => void;
  isTesting: boolean;
  testResult: RetrievalTestResult | null;
  onTest: () => void;
}

export function AdminRetrievalTestPanel({
  open,
  onOpenChange,
  engines,
  testEngineId,
  onTestEngineIdChange,
  testQuery,
  onTestQueryChange,
  isTesting,
  testResult,
  onTest,
}: AdminRetrievalTestPanelProps) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>{t.testEngine}</DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <div className="space-y-2">
            <label className="text-sm font-medium">{t.retrieval}</label>
            <Select value={testEngineId} onValueChange={onTestEngineIdChange}>
              <SelectTrigger>
                <SelectValue placeholder={t.selectDomain} />
              </SelectTrigger>
              <SelectContent>
                {engines
                  .filter((e) => e.isActive)
                  .map((e) => (
                    <SelectItem key={e.id} value={e.id}>
                      {RetrievalEngineTypeConfig[e.type]?.icon} {e.displayName}
                    </SelectItem>
                  ))}
              </SelectContent>
            </Select>
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium">{t.searchQuery}</label>
            <Textarea
              value={testQuery}
              onChange={(e) => onTestQueryChange(e.target.value)}
              placeholder={t.search}
              rows={3}
            />
          </div>
          <Button
            onClick={onTest}
            disabled={isTesting || !testEngineId || !testQuery}
          >
            {isTesting ? t.searching : t.search}
          </Button>
          {testResult && (
            <div className="space-y-2">
              <label className="text-sm font-medium">{t.result}</label>
              <pre className="p-4 bg-slate-100 dark:bg-slate-800 rounded-lg text-xs overflow-auto max-h-64">
                {JSON.stringify(testResult, null, 2)}
              </pre>
            </div>
          )}
        </div>
        <DialogFooter>
          <Button variant="outline" onClick={() => onOpenChange(false)}>
            {t.close}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
