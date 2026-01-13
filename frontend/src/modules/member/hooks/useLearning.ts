import { useState, useEffect, useCallback } from "react";
import { learningService } from "../services/learning.service";
import type {
  Course,
  CourseCreate,
  Lab,
  LabCreate,
  Assignment,
  Resource,
  ResourceCreate,
  UploadedFile,
} from "@/common/types";

// ========== Courses ==========
export function useCourses() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetch = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await learningService.listCourses();
      setCourses(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load courses");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetch();
  }, [fetch]);

  const create = async (data: CourseCreate) => {
    const course = await learningService.createCourse(data);
    setCourses((prev) => [course, ...prev]);
    return course;
  };

  const remove = async (id: string) => {
    await learningService.deleteCourse(id);
    setCourses((prev) => prev.filter((c) => c.id !== id));
  };

  return { courses, loading, error, refresh: fetch, create, remove };
}

// ========== Labs ==========
export function useLabs(courseId: string | null) {
  const [labs, setLabs] = useState<Lab[]>([]);
  const [loading, setLoading] = useState(false);

  const fetch = useCallback(async () => {
    if (!courseId) return;
    setLoading(true);
    try {
      const data = await learningService.listLabs(courseId);
      setLabs(data);
    } finally {
      setLoading(false);
    }
  }, [courseId]);

  useEffect(() => {
    fetch();
  }, [fetch]);

  const create = async (data: LabCreate) => {
    const lab = await learningService.createLab(data);
    setLabs((prev) => [...prev, lab].sort((a, b) => a.order - b.order));
    return lab;
  };

  const remove = async (id: string) => {
    await learningService.deleteLab(id);
    setLabs((prev) => prev.filter((l) => l.id !== id));
  };

  return { labs, loading, refresh: fetch, create, remove };
}

// ========== Assignments ==========
export function useAssignments(labId: string | null) {
  const [assignments, setAssignments] = useState<Assignment[]>([]);
  const [loading, setLoading] = useState(false);

  const fetch = useCallback(async () => {
    if (!labId) return;
    setLoading(true);
    try {
      const data = await learningService.listAssignments(labId);
      setAssignments(data);
    } finally {
      setLoading(false);
    }
  }, [labId]);

  useEffect(() => {
    fetch();
  }, [fetch]);

  return { assignments, loading, refresh: fetch };
}

// ========== Resources ==========
export function useResources(params?: { courseId?: string; labId?: string }) {
  const [resources, setResources] = useState<Resource[]>([]);
  const [loading, setLoading] = useState(false);

  const courseId = params?.courseId;
  const labId = params?.labId;

  const fetch = useCallback(async () => {
    setLoading(true);
    try {
      const data = await learningService.listResources({ courseId, labId });
      setResources(data);
    } finally {
      setLoading(false);
    }
  }, [courseId, labId]);

  useEffect(() => {
    fetch();
  }, [fetch]);

  const create = async (data: ResourceCreate) => {
    const resource = await learningService.createResource(data);
    setResources((prev) => [resource, ...prev]);
    return resource;
  };

  const remove = async (id: string) => {
    await learningService.deleteResource(id);
    setResources((prev) => prev.filter((r) => r.id !== id));
  };

  return { resources, loading, refresh: fetch, create, remove };
}

// ========== Files ==========
export function useFiles(category?: string) {
  const [files, setFiles] = useState<UploadedFile[]>([]);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);

  const fetch = useCallback(async () => {
    setLoading(true);
    try {
      const data = await learningService.listFiles(category);
      setFiles(data);
    } finally {
      setLoading(false);
    }
  }, [category]);

  useEffect(() => {
    fetch();
  }, [fetch]);

  const upload = async (file: File, cat = category || "general") => {
    setUploading(true);
    try {
      const uploaded = await learningService.uploadFile(file, cat);
      setFiles((prev) => [uploaded, ...prev]);
      return uploaded;
    } finally {
      setUploading(false);
    }
  };

  const remove = async (id: string) => {
    await learningService.deleteFile(id);
    setFiles((prev) => prev.filter((f) => f.id !== id));
  };

  return { files, loading, uploading, refresh: fetch, upload, remove };
}
