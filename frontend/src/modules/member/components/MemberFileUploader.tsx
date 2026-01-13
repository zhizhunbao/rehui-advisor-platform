// Member 文件上传组件 - Props: onUpload, accept, children
import { useRef, useState, type ReactNode } from "react";
import { Upload } from "lucide-react";
import { Button } from "@/libs/shadcn/ui/button";

interface MemberFileUploaderProps<T = unknown> {
  accept?: string;
  onUpload: (file: File) => Promise<T>;
  onUploaded?: (result: T) => void;
  trigger?: ReactNode;
  label?: string;
}

export function MemberFileUploader<T = unknown>({
  accept = ".docx,.pdf,.ipynb",
  onUpload,
  onUploaded,
  trigger,
  label = "Upload File",
}: MemberFileUploaderProps<T>) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [uploading, setUploading] = useState(false);

  const handleClick = () => {
    inputRef.current?.click();
  };

  const handleChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    try {
      const result = await onUpload(file);
      onUploaded?.(result);
    } finally {
      setUploading(false);
      if (inputRef.current) {
        inputRef.current.value = "";
      }
    }
  };

  return (
    <>
      <input
        ref={inputRef}
        type="file"
        accept={accept}
        onChange={handleChange}
        className="hidden"
      />
      {trigger ? (
        <div onClick={handleClick}>{trigger}</div>
      ) : (
        <Button variant="outline" onClick={handleClick} disabled={uploading}>
          <Upload className="h-4 w-4 mr-2" />
          {uploading ? "Uploading..." : label}
        </Button>
      )}
    </>
  );
}
