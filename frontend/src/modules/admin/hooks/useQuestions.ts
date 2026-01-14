// Admin 问题管理 Hook
import { useState, useEffect, useCallback } from "react";
import type { Question, Domain, CreateQuestionDto } from "@/common/types";
import { questionService } from "../services/question.service";
import { domainService } from "../services/domain.service";

export function useQuestions() {
  const [questions, setQuestions] = useState<Question[]>([]);
  const [domains, setDomains] = useState<Domain[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedDomainId, setSelectedDomainId] = useState("all");
  const [isCreating, setIsCreating] = useState(false);

  const fetchDomains = useCallback(async () => {
    const data = await domainService.getAll();
    setDomains(data);
  }, []);

  const fetchQuestions = useCallback(async () => {
    setIsLoading(true);
    try {
      const domainId =
        selectedDomainId === "all" ? undefined : selectedDomainId;
      const data = await questionService.getAll(domainId);
      setQuestions(data);
    } finally {
      setIsLoading(false);
    }
  }, [selectedDomainId]);

  useEffect(() => {
    fetchDomains();
  }, [fetchDomains]);

  useEffect(() => {
    fetchQuestions();
  }, [fetchQuestions]);

  const createQuestion = useCallback(async (data: CreateQuestionDto) => {
    const newQuestion = await questionService.create(data);
    setQuestions((prev) => [...prev, newQuestion]);
    setIsCreating(false);
    return newQuestion;
  }, []);

  const deleteQuestion = useCallback(async (id: string) => {
    await questionService.delete(id);
    setQuestions((prev) => prev.filter((q) => q.id !== id));
  }, []);

  const handleOpenCreate = useCallback(() => {
    setIsCreating(true);
  }, []);

  const handleCloseCreate = useCallback(() => {
    setIsCreating(false);
  }, []);

  return {
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
  };
}
