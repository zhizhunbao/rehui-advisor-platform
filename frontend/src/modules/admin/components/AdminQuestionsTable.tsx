// Admin 问题管理表格组件
import type { Question, Domain } from "@/common/types";
import { useAdminSettingsStore } from "@/common/stores";
import { adminLocales } from "@/common/i18n";
import { Button } from "@/libs/shadcn/ui/button";
import { Badge } from "@/libs/shadcn/ui/badge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/libs/shadcn/ui/table";

interface AdminQuestionsTableProps {
  questions: Question[];
  domains: Domain[];
  isLoading: boolean;
  onDelete: (id: string) => void;
}

export function AdminQuestionsTable({
  questions,
  domains,
  isLoading,
  onDelete,
}: AdminQuestionsTableProps) {
  const { lang } = useAdminSettingsStore();
  const t = adminLocales[lang];

  if (isLoading && !questions.length) {
    return (
      <div className="flex items-center justify-center h-40 text-muted-foreground">
        {t.loading}
      </div>
    );
  }

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>{t.questionText}</TableHead>
          <TableHead>{t.questionType}</TableHead>
          <TableHead>{t.domains}</TableHead>
          <TableHead className="text-right">{t.actions}</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {questions.map((q) => (
          <TableRow key={q.id}>
            <TableCell>{lang === "zh" ? q.text : q.textEn}</TableCell>
            <TableCell>
              <Badge variant="secondary">
                {q.type === "single"
                  ? t.typeSingle
                  : q.type === "multiple"
                  ? t.typeMultiple
                  : t.typeText}
              </Badge>
            </TableCell>
            <TableCell>
              {domains.find((d) => d.id === q.domainId)?.name ?? "-"}
            </TableCell>
            <TableCell className="text-right">
              <Button
                variant="link"
                size="sm"
                className="text-destructive"
                onClick={() => onDelete(q.id)}
              >
                {t.delete}
              </Button>
            </TableCell>
          </TableRow>
        ))}
        {!questions.length && (
          <TableRow>
            <TableCell
              colSpan={4}
              className="text-center py-8 text-muted-foreground"
            >
              {t.noData}
            </TableCell>
          </TableRow>
        )}
      </TableBody>
    </Table>
  );
}
