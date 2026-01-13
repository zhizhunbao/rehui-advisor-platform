import { useState } from "react";
import { adminLocales, type Language } from "@/common/i18n";
import { useDomains, useQuestions } from "@/modules/admin/hooks";
import type { CreateQuestionDto } from "@/common/types";
import { Button } from "@/libs/shadcn/ui/button";
import { Textarea } from "@/libs/shadcn/ui/textarea";
import { Badge } from "@/libs/shadcn/ui/badge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/libs/shadcn/ui/table";
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

interface QuestionsViewProps {
  lang: Language;
}

export default function QuestionsView({ lang }: QuestionsViewProps) {
  const t = adminLocales[lang];
  const { domains } = useDomains();
  const [selectedDomainId, setSelectedDomainId] = useState<string>("all");
  const { questions, isLoading, createQuestion, deleteQuestion } = useQuestions(
    { domainId: selectedDomainId === "all" ? undefined : selectedDomainId }
  );
  const [isCreating, setIsCreating] = useState(false);

  const handleSave = async (data: CreateQuestionDto) => {
    await createQuestion(data);
    setIsCreating(false);
  };

  const handleDelete = async (id: string) => {
    if (confirm(t.confirmDelete)) {
      await deleteQuestion(id);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-2xl font-bold text-foreground">{t.questions}</h1>
        <Button onClick={() => setIsCreating(true)}>{t.addQuestion}</Button>
      </div>

      <div>
        <Select value={selectedDomainId} onValueChange={setSelectedDomainId}>
          <SelectTrigger className="w-48">
            <SelectValue placeholder={t.allDomains} />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">{t.allDomains}</SelectItem>
            {domains.map((d) => (
              <SelectItem key={d.id} value={d.id}>
                {lang === "zh" ? d.name : d.nameEn}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {isLoading && !questions.length ? (
        <div className="flex items-center justify-center h-40 text-muted-foreground">
          {t.loading}
        </div>
      ) : (
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
                    onClick={() => handleDelete(q.id)}
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
      )}

      <Dialog open={isCreating} onOpenChange={setIsCreating}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{t.addQuestion}</DialogTitle>
          </DialogHeader>
          <QuestionForm
            lang={lang}
            domains={domains}
            onSave={handleSave}
            onClose={() => setIsCreating(false)}
          />
        </DialogContent>
      </Dialog>
    </div>
  );
}

interface QuestionFormProps {
  lang: Language;
  domains: { id: string; name: string; nameEn: string }[];
  onSave: (data: CreateQuestionDto) => Promise<void>;
  onClose: () => void;
}

function QuestionForm({ lang, domains, onSave, onClose }: QuestionFormProps) {
  const t = adminLocales[lang];
  const [formData, setFormData] = useState<CreateQuestionDto>({
    domainId: domains[0]?.id ?? "",
    text: "",
    textEn: "",
    type: "single",
    options: [],
    sortOrder: 0,
  });
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      await onSave(formData);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="space-y-2">
        <label className="text-sm font-medium">{t.domains}</label>
        <Select
          value={formData.domainId}
          onValueChange={(value) =>
            setFormData({ ...formData, domainId: value })
          }
        >
          <SelectTrigger>
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            {domains.map((d) => (
              <SelectItem key={d.id} value={d.id}>
                {lang === "zh" ? d.name : d.nameEn}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      <div className="space-y-2">
        <label className="text-sm font-medium">{t.questionTextZh}</label>
        <Textarea
          value={formData.text}
          onChange={(e) => setFormData({ ...formData, text: e.target.value })}
          className="h-20"
          required
        />
      </div>

      <div className="space-y-2">
        <label className="text-sm font-medium">{t.questionTextEn}</label>
        <Textarea
          value={formData.textEn}
          onChange={(e) => setFormData({ ...formData, textEn: e.target.value })}
          className="h-20"
          required
        />
      </div>

      <div className="space-y-2">
        <label className="text-sm font-medium">{t.questionType}</label>
        <Select
          value={formData.type}
          onValueChange={(value) =>
            setFormData({
              ...formData,
              type: value as "single" | "multiple" | "text",
            })
          }
        >
          <SelectTrigger>
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="single">{t.typeSingle}</SelectItem>
            <SelectItem value="multiple">{t.typeMultiple}</SelectItem>
            <SelectItem value="text">{t.typeText}</SelectItem>
          </SelectContent>
        </Select>
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
  );
}
