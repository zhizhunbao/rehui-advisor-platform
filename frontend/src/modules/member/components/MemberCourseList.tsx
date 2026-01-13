// Member 课程列表组件 - Props: courses, selectedId, onSelect, onAdd, onDelete
import { Book, MoreVertical, Plus, Trash2 } from "lucide-react";
import { Button } from "@/libs/shadcn/ui/button";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/libs/shadcn/ui/card";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/libs/shadcn/ui/dropdown-menu";
import type { Course } from "@/common/types";

interface MemberCourseListProps {
  courses: Course[];
  selectedId?: string;
  onSelect: (course: Course) => void;
  onAdd: () => void;
  onDelete: (id: string) => void;
}

export function MemberCourseList({
  courses,
  selectedId,
  onSelect,
  onAdd,
  onDelete,
}: MemberCourseListProps) {
  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold">Courses</h2>
        <Button size="sm" variant="outline" onClick={onAdd}>
          <Plus className="h-4 w-4 mr-1" /> Add
        </Button>
      </div>

      {courses.length === 0 ? (
        <p className="text-muted-foreground text-sm">No courses yet</p>
      ) : (
        <div className="space-y-2">
          {courses.map((course) => (
            <Card
              key={course.id}
              className={`cursor-pointer transition-colors hover:bg-accent ${
                selectedId === course.id ? "border-primary" : ""
              }`}
              onClick={() => onSelect(course)}
            >
              <CardHeader className="p-3 pb-1">
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-2">
                    <Book className="h-4 w-4 text-muted-foreground" />
                    <CardTitle className="text-sm">{course.name}</CardTitle>
                  </div>
                  <DropdownMenu>
                    <DropdownMenuTrigger
                      asChild
                      onClick={(e) => e.stopPropagation()}
                    >
                      <Button variant="ghost" size="icon" className="h-6 w-6">
                        <MoreVertical className="h-3 w-3" />
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuItem
                        className="text-destructive"
                        onClick={(e) => {
                          e.stopPropagation();
                          onDelete(course.id);
                        }}
                      >
                        <Trash2 className="h-4 w-4 mr-2" /> Delete
                      </DropdownMenuItem>
                    </DropdownMenuContent>
                  </DropdownMenu>
                </div>
              </CardHeader>
              <CardContent className="p-3 pt-0">
                <div className="text-xs text-muted-foreground space-x-2">
                  {course.code && <span>{course.code}</span>}
                  {course.semester && <span>• {course.semester}</span>}
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
