// Admin 问题管理页面
import { useQuestions } from "../hooks/useQuestions";
import { AdminQuestionsHeader } from "../components/AdminQuestionsHeader";
import { AdminQuestionsFilter } from "../components/AdminQuestionsFilter";
import { AdminQuestionsTable } from "../components/AdminQuestionsTable";
import { AdminQuestionFormDialog } from "../components/AdminQuestionFormDialog";

export default function QuestionsView() {
  const {
    questions,
    domains,
    isLoading,
    selectedDomainId,
    setSelectedDomainId,
    isCreating,
    createQuestion,
    deleteQuestion,
    handleOpenCreate,
    handleCloseCreate,
  } = useQuestions();

  return (
    <>
      <AdminQuestionsHeader onAdd={handleOpenCreate} />

      <AdminQuestionsFilter
        domains={domains}
        selectedDomainId={selectedDomainId}
        onDomainChange={setSelectedDomainId}
      />

      <AdminQuestionsTable
        questions={questions}
        domains={domains}
        isLoading={isLoading}
        onDelete={deleteQuestion}
      />

      <AdminQuestionFormDialog
        open={isCreating}
        domains={domains}
        onSave={createQuestion}
        onClose={handleCloseCreate}
      />
    </>
  );
}
