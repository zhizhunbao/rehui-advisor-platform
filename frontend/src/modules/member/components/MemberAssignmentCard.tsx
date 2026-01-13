// Member 作业卡片组件 - Props: assignment, onDownload
import { FileCode, Download } from "lucide-react";
import { Button } from "@/libs/shadcn/ui/button";
import { Badge } from "@/libs/shadcn/ui/badge";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/libs/shadcn/ui/card";
import { AssignmentStatusColor, AssignmentStatusLabel } from "@/common/enum";
import type { Assignment } from "@/common/types";

interface MemberAssignmentCardProps {
  assignment: Assignment;
  onDownload?: (fileId: string) => void;
}

export function MemberAssignmentCard({
  assignment,
  onDownload,
}: MemberAssignmentCardProps) {
  const handleDownload = () => {
    if (assignment.notebookFileId && onDownload) {
      onDownload(assignment.notebookFileId);
    }
  };

  return (
    <Card>
      <CardHeader className="pb-2">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <FileCode className="h-4 w-4 text-muted-foreground" />
            <CardTitle className="text-sm">
              {assignment.title || "Assignment"}
            </CardTitle>
          </div>
          <Badge className={AssignmentStatusColor[assignment.status]}>
            {AssignmentStatusLabel[assignment.status]}
          </Badge>
        </div>
      </CardHeader>
      <CardContent className="space-y-2">
        {assignment.notes && (
          <p className="text-sm text-muted-foreground">{assignment.notes}</p>
        )}
        {assignment.score !== null && (
          <div className="text-sm">
            <span className="font-medium">Score:</span> {assignment.score}
          </div>
        )}
        {assignment.feedback && (
          <div className="text-sm">
            <span className="font-medium">Feedback:</span> {assignment.feedback}
          </div>
        )}
        {assignment.notebookFileId && onDownload && (
          <Button variant="outline" size="sm" onClick={handleDownload}>
            <Download className="h-4 w-4 mr-1" /> Download Notebook
          </Button>
        )}
      </CardContent>
    </Card>
  );
}
