import { useState } from "react";
import { MemberCourseList } from "../components/MemberCourseList";
import { MemberCourseForm } from "../components/MemberCourseForm";
import { MemberLabList } from "../components/MemberLabList";
import { MemberLabForm } from "../components/MemberLabForm";
import { MemberLabDetail } from "../components/MemberLabDetail";
import {
  useCourses,
  useLabs,
  useAssignments,
  useResources,
} from "../hooks/useLearning";
import { learningService } from "../services/learning.service";
import type {
  Course,
  Lab,
  CourseCreate,
  LabCreate,
  UploadedFile,
} from "@/common/types";

export function LearningDashboard() {
  const [selectedCourse, setSelectedCourse] = useState<Course | null>(null);
  const [selectedLab, setSelectedLab] = useState<Lab | null>(null);
  const [showCourseForm, setShowCourseForm] = useState(false);
  const [showLabForm, setShowLabForm] = useState(false);

  const { courses, create: createCourse, remove: removeCourse } = useCourses();
  const {
    labs,
    create: createLab,
    remove: removeLab,
    refresh: refreshLabs,
  } = useLabs(selectedCourse?.id || null);
  const { assignments } = useAssignments(selectedLab?.id || null);
  const {
    resources,
    create: createResource,
    remove: removeResource,
  } = useResources(selectedLab ? { labId: selectedLab.id } : undefined);

  const handleCourseSelect = (course: Course) => {
    setSelectedCourse(course);
    setSelectedLab(null);
  };

  const handleCourseCreate = async (data: CourseCreate) => {
    const course = await createCourse(data);
    setSelectedCourse(course);
  };

  const handleCourseDelete = async (id: string) => {
    await removeCourse(id);
    if (selectedCourse?.id === id) {
      setSelectedCourse(null);
      setSelectedLab(null);
    }
  };

  const handleLabSelect = (lab: Lab) => {
    setSelectedLab(lab);
  };

  const handleLabCreate = async (data: LabCreate) => {
    const lab = await createLab(data);
    setSelectedLab(lab);
  };

  const handleLabDelete = async (id: string) => {
    await removeLab(id);
    if (selectedLab?.id === id) {
      setSelectedLab(null);
    }
  };

  const handleFileUpload = async (file: File): Promise<UploadedFile> => {
    return learningService.uploadFile(file, "labs");
  };

  const handleFileUploaded = async (file: UploadedFile) => {
    if (!selectedLab) return;
    const result = await learningService.convertToMarkdown(file.id);
    const updated = await learningService.updateLab(selectedLab.id, {
      instructionsMd: result.markdown,
      originalFileId: file.id,
    });
    setSelectedLab(updated);
    refreshLabs();
  };

  const handleDownloadFile = (fileId: string) => {
    window.open(learningService.getDownloadUrl(fileId), "_blank");
  };

  const handleResourceCreate = async (url: string, title: string) => {
    await createResource({
      url,
      title,
      labId: selectedLab?.id,
      courseId: selectedCourse?.id,
    });
  };

  return (
    <div className="h-full flex">
      {/* Left sidebar - Courses */}
      <div className="w-64 border-r p-4 overflow-y-auto">
        <MemberCourseList
          courses={courses}
          selectedId={selectedCourse?.id}
          onSelect={handleCourseSelect}
          onAdd={() => setShowCourseForm(true)}
          onDelete={handleCourseDelete}
        />
      </div>

      {/* Middle - Labs */}
      {selectedCourse && (
        <div className="w-64 border-r p-4 overflow-y-auto">
          <MemberLabList
            labs={labs}
            selectedId={selectedLab?.id}
            onSelect={handleLabSelect}
            onAdd={() => setShowLabForm(true)}
            onDelete={handleLabDelete}
          />
        </div>
      )}

      {/* Right - Lab Detail */}
      <div className="flex-1 p-6 overflow-y-auto">
        {selectedLab ? (
          <MemberLabDetail
            lab={selectedLab}
            assignments={assignments}
            resources={resources}
            onFileUpload={handleFileUpload}
            onFileUploaded={handleFileUploaded}
            onDownloadFile={handleDownloadFile}
            onResourceCreate={handleResourceCreate}
            onResourceDelete={removeResource}
          />
        ) : selectedCourse ? (
          <div className="text-center text-muted-foreground py-12">
            Select a lab or create a new one
          </div>
        ) : (
          <div className="text-center text-muted-foreground py-12">
            Select a course to get started
          </div>
        )}
      </div>

      {/* Dialogs */}
      <MemberCourseForm
        open={showCourseForm}
        onClose={() => setShowCourseForm(false)}
        onSubmit={handleCourseCreate}
      />

      {selectedCourse && (
        <MemberLabForm
          open={showLabForm}
          courseId={selectedCourse.id}
          onClose={() => setShowLabForm(false)}
          onSubmit={handleLabCreate}
        />
      )}
    </div>
  );
}
