import { http } from "@/common/http";
import type {
  Course,
  CourseCreate,
  CourseUpdate,
  Lab,
  LabCreate,
  LabUpdate,
  Assignment,
  AssignmentCreate,
  AssignmentUpdate,
  Resource,
  ResourceCreate,
  ResourceUpdate,
  UploadedFile,
  ConvertResult,
} from "@/common/types";

const BASE = "/learning";

export const learningService = {
  // ========== Courses ==========
  async createCourse(data: CourseCreate): Promise<Course> {
    return http.post<Course>(`${BASE}/courses`, data);
  },

  async listCourses(): Promise<Course[]> {
    return http.get<Course[]>(`${BASE}/courses`);
  },

  async getCourse(id: string): Promise<Course> {
    return http.get<Course>(`${BASE}/courses/${id}`);
  },

  async updateCourse(id: string, data: CourseUpdate): Promise<Course> {
    return http.put<Course>(`${BASE}/courses/${id}`, data);
  },

  async deleteCourse(id: string): Promise<void> {
    return http.delete(`${BASE}/courses/${id}`);
  },

  // ========== Labs ==========
  async createLab(data: LabCreate): Promise<Lab> {
    return http.post<Lab>(`${BASE}/labs`, data);
  },

  async listLabs(courseId: string): Promise<Lab[]> {
    return http.get<Lab[]>(`${BASE}/labs?courseId=${courseId}`);
  },

  async getLab(id: string): Promise<Lab> {
    return http.get<Lab>(`${BASE}/labs/${id}`);
  },

  async updateLab(id: string, data: LabUpdate): Promise<Lab> {
    return http.put<Lab>(`${BASE}/labs/${id}`, data);
  },

  async deleteLab(id: string): Promise<void> {
    return http.delete(`${BASE}/labs/${id}`);
  },

  // ========== Assignments ==========
  async createAssignment(data: AssignmentCreate): Promise<Assignment> {
    return http.post<Assignment>(`${BASE}/assignments`, data);
  },

  async listAssignments(labId: string): Promise<Assignment[]> {
    return http.get<Assignment[]>(`${BASE}/assignments?labId=${labId}`);
  },

  async getAssignment(id: string): Promise<Assignment> {
    return http.get<Assignment>(`${BASE}/assignments/${id}`);
  },

  async updateAssignment(
    id: string,
    data: AssignmentUpdate
  ): Promise<Assignment> {
    return http.put<Assignment>(`${BASE}/assignments/${id}`, data);
  },

  async deleteAssignment(id: string): Promise<void> {
    return http.delete(`${BASE}/assignments/${id}`);
  },

  // ========== Resources ==========
  async createResource(data: ResourceCreate): Promise<Resource> {
    return http.post<Resource>(`${BASE}/resources`, data);
  },

  async listResources(params?: {
    courseId?: string;
    labId?: string;
  }): Promise<Resource[]> {
    const query = new URLSearchParams();
    if (params?.courseId) query.set("courseId", params.courseId);
    if (params?.labId) query.set("labId", params.labId);
    const qs = query.toString();
    return http.get<Resource[]>(`${BASE}/resources${qs ? `?${qs}` : ""}`);
  },

  async getResource(id: string): Promise<Resource> {
    return http.get<Resource>(`${BASE}/resources/${id}`);
  },

  async updateResource(id: string, data: ResourceUpdate): Promise<Resource> {
    return http.put<Resource>(`${BASE}/resources/${id}`, data);
  },

  async deleteResource(id: string): Promise<void> {
    return http.delete(`${BASE}/resources/${id}`);
  },

  // ========== Storage ==========
  async uploadFile(file: File, category = "general"): Promise<UploadedFile> {
    const formData = new FormData();
    formData.append("file", file);

    const token =
      localStorage.getItem("token") || sessionStorage.getItem("sessionToken");
    const res = await fetch(`/api${BASE}/storage/upload?category=${category}`, {
      method: "POST",
      headers: token ? { Authorization: `Bearer ${token}` } : {},
      body: formData,
    });

    const json = await res.json();
    if (!json.success) throw new Error(json.error?.message || "Upload failed");
    return json.data;
  },

  async listFiles(category?: string): Promise<UploadedFile[]> {
    const qs = category ? `?category=${category}` : "";
    return http.get<UploadedFile[]>(`${BASE}/storage${qs}`);
  },

  async getFile(fileId: string): Promise<UploadedFile> {
    return http.get<UploadedFile>(`${BASE}/storage/${fileId}`);
  },

  getDownloadUrl(fileId: string): string {
    return `/api${BASE}/storage/${fileId}/download`;
  },

  async convertToMarkdown(fileId: string): Promise<ConvertResult> {
    return http.post<ConvertResult>(`${BASE}/storage/${fileId}/convert`);
  },

  async deleteFile(fileId: string): Promise<void> {
    return http.delete(`${BASE}/storage/${fileId}`);
  },
};
