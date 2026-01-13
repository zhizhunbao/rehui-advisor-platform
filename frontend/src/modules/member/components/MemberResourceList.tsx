// Member 资源列表组件 - Props: resources, onCreate, onDelete
import { useState } from "react";
import { ExternalLink, Plus, Trash2, Link as LinkIcon } from "lucide-react";
import { Button } from "@/libs/shadcn/ui/button";
import { Input } from "@/libs/shadcn/ui/input";
import { Badge } from "@/libs/shadcn/ui/badge";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/libs/shadcn/ui/dialog";
import { ResourceTypeColor } from "@/common/enum";
import type { Resource } from "@/common/types";

interface MemberResourceListProps {
  resources: Resource[];
  onCreate: (url: string, title: string) => Promise<void>;
  onDelete: (id: string) => Promise<void>;
}

export function MemberResourceList({
  resources,
  onCreate,
  onDelete,
}: MemberResourceListProps) {
  const [showAdd, setShowAdd] = useState(false);
  const [url, setUrl] = useState("");
  const [title, setTitle] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAdd = async () => {
    if (!url.trim() || !title.trim()) return;
    setLoading(true);
    try {
      await onCreate(url, title);
      setUrl("");
      setTitle("");
      setShowAdd(false);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-3">
      <div className="flex justify-end">
        <Button size="sm" variant="outline" onClick={() => setShowAdd(true)}>
          <Plus className="h-4 w-4 mr-1" /> Add Link
        </Button>
      </div>

      {resources.length === 0 ? (
        <p className="text-muted-foreground text-center py-4">
          No resources yet
        </p>
      ) : (
        <div className="space-y-2">
          {resources.map((resource) => (
            <div
              key={resource.id}
              className="flex items-center justify-between p-3 border rounded-lg hover:bg-accent"
            >
              <div className="flex items-center gap-3 min-w-0">
                <LinkIcon className="h-4 w-4 text-muted-foreground shrink-0" />
                <div className="min-w-0">
                  <a
                    href={resource.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm font-medium hover:underline flex items-center gap-1"
                  >
                    {resource.title}
                    <ExternalLink className="h-3 w-3" />
                  </a>
                  {resource.description && (
                    <p className="text-xs text-muted-foreground truncate">
                      {resource.description}
                    </p>
                  )}
                </div>
                <Badge
                  variant="secondary"
                  className={ResourceTypeColor[resource.type]}
                >
                  {resource.type}
                </Badge>
              </div>
              <Button
                variant="ghost"
                size="icon"
                className="h-8 w-8 text-destructive"
                onClick={() => onDelete(resource.id)}
              >
                <Trash2 className="h-4 w-4" />
              </Button>
            </div>
          ))}
        </div>
      )}

      <Dialog open={showAdd} onOpenChange={setShowAdd}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Add Resource Link</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <Input
              placeholder="Title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            />
            <Input
              placeholder="URL"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
            />
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowAdd(false)}>
              Cancel
            </Button>
            <Button onClick={handleAdd} disabled={loading || !url || !title}>
              {loading ? "Adding..." : "Add"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
