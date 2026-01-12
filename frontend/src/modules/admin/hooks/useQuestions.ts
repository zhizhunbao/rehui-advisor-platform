import { useState, useEffect, useCallback } from "react";
import { questionService } from "../services/admin.service";
import type { Question, CreateQuestionDto } from "../types/admin.types";

interface UseQuestionsOptions {
  domainId?: string;
  autoFetch?: boolean;
}

export function useQuestions(options: UseQuestionsOptions = {}) {
  const { domainId, autoFetch = true } = options;
  const [questions, setQuestions] = useState<Question[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const fetchQuestions = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await questionService.getAll(domainId);
      setQuestions(data);
    } catch (err) {
      setError(
        err instanceof Error ? err : new Error("Failed to fetch questions")
      );
    } finally {
      setIsLoading(false);
    }
  }, [domainId]);

  const createQuestion = useCallback(async (data: CreateQuestionDto) => {
    setIsLoading(true);
    try {
      const newQuestion = await questionService.create(data);
      setQuestions((prev) => [...prev, newQuestion]);
      return newQuestion;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const deleteQuestion = useCallback(async (id: string) => {
    setIsLoading(true);
    try {
      await questionService.delete(id);
      setQuestions((prev) => prev.filter((q) => q.id !== id));
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    if (autoFetch) {
      fetchQuestions();
    }
  }, [autoFetch, fetchQuestions]);

  return {
    questions,
    isLoading,
    error,
    fetchQuestions,
    createQuestion,
    deleteQuestion,
  };
}
