// Admin Agent 框架添加弹窗
import { useState } from "react";
import { useAdminSettingsStore } from "@/common/stores";
import type { CreateAgentFrameworkDto } from "@/common/types";
import { Button } from "@/libs/shadcn/ui/button";
import { Input } from "@/libs/shadcn/ui/input";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/libs/shadcn/ui/dialog";

interface Props {
  open: boolean;
  onClose: () => void;
  onSubmit: (data: CreateAgentFrameworkDto) => Promise<void>;
}

export function AdminAgentFrameworkAddDialog({
  open,
  onClose,
  onSubmit,
}: Props) {
  const { lang } = useAdminSettingsStore();
  const [url, setUrl] = useState("");
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [tags, setTags] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async () => {
    if (!url) return;
    setIsSubmitting(true);
    try {
      await onSubmit({
        url,
        name: name || undefined,
        description: description || undefined,
        tags: tags
          .split(",")
          .map((t) => t.trim())
          .filter(Boolean),
      });
      setUrl("");
      setName("");
      setDescription("");
      setTags("");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <Dialog open={open} onOpenChange={(o) => !o && onClose()}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>
            {lang === "zh" ? "添加 Agent 框架" : "Add Agent Framework"}
          </DialogTitle>
        </DialogHeader>
        <div className="space-y-4">
          <div>
            <label className="text-sm font-medium">GitHub URL *</label>
            <Input
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://github.com/owner/repo"
            />
          </div>
          <div>
            <label className="text-sm font-medium">
              {lang === "zh" ? "名称" : "Name"}
            </label>
            <Input
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder={lang === "zh" ? "可选，默认使用仓库名" : "Optional"}
            />
          </div>
          <div>
            <label className="text-sm font-medium">
              {lang === "zh" ? "描述" : "Description"}
            </label>
            <Input
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder={lang === "zh" ? "框架描述" : "Framework description"}
            />
          </div>
          <div>
            <label className="text-sm font-medium">
              {lang === "zh" ? "标签 (逗号分隔)" : "Tags (comma separated)"}
            </label>
            <Input
              value={tags}
              onChange={(e) => setTags(e.target.value)}
              placeholder="agent, multi-agent, workflow"
            />
          </div>
          <div className="flex gap-2 justify-end">
            <Button variant="outline" onClick={onClose}>
              {lang === "zh" ? "取消" : "Cancel"}
            </Button>
            <Button onClick={handleSubmit} disabled={!url || isSubmitting}>
              {isSubmitting
                ? lang === "zh"
                  ? "添加中..."
                  : "Adding..."
                : lang === "zh"
                ? "添加"
                : "Add"}
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
