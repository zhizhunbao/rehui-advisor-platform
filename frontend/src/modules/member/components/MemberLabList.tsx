// Member Lab 列表组件 - Props: labs, selectedId, onSelect, onAdd, onDelete
import { FileText, MoreVertical, Plus, Trash2 } from "lucide-react";
import { Button } from "@/libs/shadcn/ui/button";
import { Badge } from "@/libs/shadcn/ui/badge";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/libs/shadcn/ui/dropdown-menu";
import type { Lab } from "@/common/types";

interface MemberLabListProps {
  labs: Lab[];
  selectedId?: string;
  onSelect: (lab: Lab) => void;
  onAdd: () => void;
  onDelete: (id: string) => void;
}

export function MemberLabList({
  labs,
  selectedId,
  onSelect,
  onAdd,
  onDelete,
}: MemberLabListProps) {
  const formatDate = (date: string | null) => {
    if (!date) return null;
    return new Date(date).toLocaleDateString();
  };

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <h3 className="font-medium">Labs</h3>
        <Button size="sm" variant="outline" onClick={onAdd}>
          <Plus className="h-4 w-4 mr-1" /> Add
        </Button>
      </div>

      {labs.length === 0 ? (
        <p className="text-muted-foreground text-sm">No labs yet</p>
      ) : (
        <div className="space-y-1">
          {labs.map((lab) => (
            <div
              key={lab.id}
              className={`flex items-center justify-between p-2 rounded-md cursor-pointer hover:bg-accent ${
                selectedId === lab.id ? "bg-accent" : ""
              }`}
              onClick={() => onSelect(lab)}
            >
              <div className="flex items-center gap-2 min-w-0">
                <FileText className="h-4 w-4 text-muted-foreground shrink-0" />
                <span className="text-sm truncate">{lab.title}</span>
                {lab.dueDate && (
                  <Badge variant="outline" className="text-xs shrink-0">
                    Due: {formatDate(lab.dueDate)}
                  </Badge>
                )}
              </div>
              <DropdownMenu>
                <DropdownMenuTrigger
                  asChild
                  onClick={(e) => e.stopPropagation()}
                >
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-6 w-6 shrink-0"
                  >
                    <MoreVertical className="h-3 w-3" />
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end">
                  <DropdownMenuItem
                    className="text-destructive"
                    onClick={(e) => {
                      e.stopPropagation();
                      onDelete(lab.id);
                    }}
                  >
                    <Trash2 className="h-4 w-4 mr-2" /> Delete
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
