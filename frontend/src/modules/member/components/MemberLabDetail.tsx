// Member Lab 详情组件 - Props: lab, assignments, resources, onFileUpload, onResourceCreate
import { useState } from "react";
import { FileUp } from "lucide-react";
import { Button } from "@/libs/shadcn/ui/button";
import {
  Tabs,
  TabsContent,
  TabsList,
  TabsTrigger,
} from "@/libs/shadcn/ui/tabs";
import { MemberMarkdownViewer } from "./MemberMarkdownViewer";
import { MemberFileUploader } from "./MemberFileUploader";
import { MemberResourceList } from "./MemberResourceList";
import { MemberAssignmentCard } from "./MemberAssignmentCard";
import type { Lab, Assignment, Resource, UploadedFile } from "@/common/types";

interface MemberLabDetailProps {
  lab: Lab;
  assignments: Assignment[];
  resources: Resource[];
  onFileUpload: (file: File) => Promise<UploadedFile>;
  onFileUploaded: (file: UploadedFile) => Promise<void>;
  onDownloadFile: (fileId: string) => void;
  onResourceCreate: (url: string, title: string) => Promise<void>;
  onResourceDelete: (id: string) => Promise<void>;
}

export function MemberLabDetail({
  lab,
  assignments,
  resources,
  onFileUpload,
  onFileUploaded,
  onDownloadFile,
  onResourceCreate,
  onResourceDelete,
}: MemberLabDetailProps) {
  const [converting, setConverting] = useState(false);

  const handleFileUploaded = async (file: UploadedFile) => {
    if (file.fileType === "docx" || file.fileType === "pdf") {
      setConverting(true);
      try {
        await onFileUploaded(file);
      } finally {
        setConverting(false);
      }
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold">{lab.title}</h2>
        {lab.dueDate && (
          <span className="text-sm text-muted-foreground">
            Due: {new Date(lab.dueDate).toLocaleDateString()}
          </span>
        )}
      </div>

      {lab.description && (
        <p className="text-muted-foreground">{lab.description}</p>
      )}

      <Tabs defaultValue="instructions">
        <TabsList>
          <TabsTrigger value="instructions">Instructions</TabsTrigger>
          <TabsTrigger value="assignments">
            Assignments ({assignments.length})
          </TabsTrigger>
          <TabsTrigger value="resources">
            Resources ({resources.length})
          </TabsTrigger>
        </TabsList>

        <TabsContent value="instructions" className="space-y-4">
          {!lab.instructionsMd ? (
            <div className="border-2 border-dashed rounded-lg p-8 text-center">
              <FileUp className="h-8 w-8 mx-auto text-muted-foreground mb-2" />
              <p className="text-muted-foreground mb-4">
                Upload lab instructions (docx/pdf)
              </p>
              <MemberFileUploader
                accept=".docx,.pdf"
                onUpload={onFileUpload}
                onUploaded={handleFileUploaded}
              />
              {converting && (
                <p className="text-sm text-muted-foreground mt-2">
                  Converting to markdown...
                </p>
              )}
            </div>
          ) : (
            <div className="space-y-2">
              <div className="flex justify-end">
                <MemberFileUploader
                  accept=".docx,.pdf"
                  onUpload={onFileUpload}
                  onUploaded={handleFileUploaded}
                  trigger={
                    <Button variant="outline" size="sm">
                      <FileUp className="h-4 w-4 mr-1" /> Replace
                    </Button>
                  }
                />
              </div>
              <MemberMarkdownViewer content={lab.instructionsMd} />
            </div>
          )}
        </TabsContent>

        <TabsContent value="assignments">
          {assignments.length === 0 ? (
            <p className="text-muted-foreground text-center py-8">
              No assignments yet
            </p>
          ) : (
            <div className="space-y-3">
              {assignments.map((a) => (
                <MemberAssignmentCard
                  key={a.id}
                  assignment={a}
                  onDownload={onDownloadFile}
                />
              ))}
            </div>
          )}
        </TabsContent>

        <TabsContent value="resources">
          <MemberResourceList
            resources={resources}
            onCreate={onResourceCreate}
            onDelete={onResourceDelete}
          />
        </TabsContent>
      </Tabs>
    </div>
  );
}
