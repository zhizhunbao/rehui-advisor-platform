"""文档转换器 - docx/pdf 转 markdown"""
import io
from src.common.errors import AppError, AppErrorCode


class DocumentConverter:
    """文档转换服务"""

    def convert(self, filename: str, content: bytes) -> str:
        """根据文件类型转换为 markdown"""
        ext = filename.lower().split(".")[-1] if "." in filename else ""
        
        if ext in ("docx", "doc"):
            return self._convert_docx(content)
        elif ext == "pdf":
            return self._convert_pdf(content)
        else:
            raise AppError(
                AppErrorCode.VALIDATION_ERROR,
                f"Unsupported file type: {ext}. Supported: docx, pdf",
            )

    def _convert_docx(self, content: bytes) -> str:
        """将 docx 转换为 markdown"""
        try:
            import mammoth
        except ImportError:
            raise AppError(
                AppErrorCode.CONFIGURATION_ERROR,
                "mammoth library not installed. Run: pip install mammoth",
            )
        
        result = mammoth.convert_to_markdown(io.BytesIO(content))
        return result.value

    def _convert_pdf(self, content: bytes) -> str:
        """将 pdf 转换为 markdown"""
        try:
            import pymupdf
        except ImportError:
            raise AppError(
                AppErrorCode.CONFIGURATION_ERROR,
                "pymupdf library not installed. Run: pip install pymupdf",
            )
        
        doc = pymupdf.open(stream=content, filetype="pdf")
        
        markdown_parts = []
        for page_num, page in enumerate(doc, 1):
            text = page.get_text()
            if text.strip():
                markdown_parts.append(f"## Page {page_num}\n\n{text}")
        
        doc.close()
        return "\n\n".join(markdown_parts)
