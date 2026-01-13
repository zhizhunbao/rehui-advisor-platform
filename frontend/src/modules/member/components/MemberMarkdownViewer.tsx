// Member Markdown 查看器组件 - Props: content
interface MemberMarkdownViewerProps {
  content: string;
}

export function MemberMarkdownViewer({ content }: MemberMarkdownViewerProps) {
  return (
    <div className="prose prose-sm max-w-none dark:prose-invert whitespace-pre-wrap">
      {content}
    </div>
  );
}
