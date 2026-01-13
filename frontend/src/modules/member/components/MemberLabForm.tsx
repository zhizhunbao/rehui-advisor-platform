// Member Lab 表单组件 - Props: open, courseId, onClose, onSubmit
import { useState } from "react";
import { Button } from "@/libs/shadcn/ui/button";
import { Input } from "@/libs/shadcn/ui/input";
import { Label } from "@/libs/shadcn/ui/label";
import { Textarea } from "@/libs/shadcn/ui/textarea";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/libs/shadcn/ui/dialog";
import type { LabCreate } from "@/common/types";

interface MemberLabFormProps {
  open: boolean;
  courseId: string;
  onClose: () => void;
  onSubmit: (data: LabCreate) => Promise<void>;
}

export function MemberLabForm({
  open,
  courseId,
  onClose,
  onSubmit,
}: MemberLabFormProps) {
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({ title: "", description: "", dueDate: "" });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.title.trim()) return;

    setLoading(true);
    try {
      await onSubmit({
        courseId,
        title: form.title,
        description: form.description || undefined,
        dueDate: form.dueDate || undefined,
      });
      setForm({ title: "", description: "", dueDate: "" });
      onClose();
    } finally {
      setLoading(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Add Lab</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="title">Lab Title *</Label>
            <Input
              id="title"
              value={form.title}
              onChange={(e) => setForm({ ...form, title: e.target.value })}
              placeholder="e.g., Lab 1: Q-Learning Implementation"
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="dueDate">Due Date</Label>
            <Input
              id="dueDate"
              type="date"
              value={form.dueDate}
              onChange={(e) => setForm({ ...form, dueDate: e.target.value })}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="description">Description</Label>
            <Textarea
              id="description"
              value={form.description}
              onChange={(e) =>
                setForm({ ...form, description: e.target.value })
              }
              placeholder="Lab description..."
              rows={3}
            />
          </div>
          <DialogFooter>
            <Button type="button" variant="outline" onClick={onClose}>
              Cancel
            </Button>
            <Button type="submit" disabled={loading || !form.title.trim()}>
              {loading ? "Creating..." : "Create"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
