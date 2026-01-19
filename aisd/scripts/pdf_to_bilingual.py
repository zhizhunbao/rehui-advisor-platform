"""
PDF to Bilingual Markdown Converter
PDF转双语Markdown转换器

Usage:
    python scripts/pdf_to_bilingual.py <pdf_path> [--format side-by-side|separate|inline]
"""

import sys
import argparse
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    print("Error: pypdf not installed. Run: uv add pypdf")
    sys.exit(1)


class PDFToBilingualConverter:
    """PDF to bilingual markdown converter"""
    
    def __init__(self, pdf_path: str, format_type: str = "inline"):
        self.pdf_path = Path(pdf_path)
        self.format_type = format_type
        self.content = []
        
    def extract_pdf(self) -> list[str]:
        """Extract text from PDF page by page"""
        print(f"📄 Extracting PDF: {self.pdf_path.name}")
        
        with open(self.pdf_path, 'rb') as file:
            reader = PdfReader(file)
            total_pages = len(reader.pages)
            
            pages = []
            for i, page in enumerate(reader.pages, 1):
                print(f"  Processing page {i}/{total_pages}...")
                text = page.extract_text()
                if text and text.strip():
                    pages.append(text.strip())
                else:
                    pages.append("*[Image-only or empty page]*")
            
            print(f"✓ Extracted {total_pages} pages\n")
            return pages
    
    def create_bilingual_template(self, pages: list[str]) -> str:
        """Create bilingual markdown template"""
        
        if self.format_type == "side-by-side":
            return self._format_side_by_side(pages)
        elif self.format_type == "separate":
            return self._format_separate(pages)
        else:  # inline
            return self._format_inline(pages)
    
    def _format_inline(self, pages: list[str]) -> str:
        """Inline bilingual format"""
        output = []
        output.append(f"# {self.pdf_path.stem}")
        output.append(f"\n**Source:** `{self.pdf_path.name}`")
        output.append(f"**来源:** `{self.pdf_path.name}`")
        output.append("\n---\n")
        
        for i, page_text in enumerate(pages, 1):
            output.append(f"## Page {i} | 第{i}页\n")
            
            # English section
            output.append("### English Version\n")
            output.append(page_text)
            output.append("\n")
            
            # Chinese translation placeholder
            output.append("### 中文翻译\n")
            output.append("<!-- TODO: Add Chinese translation here -->")
            output.append("<!-- 待添加: 在此处添加中文翻译 -->\n")
            
            output.append("\n---\n")
        
        return "\n".join(output)
    
    def _format_side_by_side(self, pages: list[str]) -> str:
        """Side-by-side bilingual format"""
        output = []
        output.append(f"# {self.pdf_path.stem}\n")
        output.append("| English | 中文 |")
        output.append("|---------|------|")
        
        for i, page_text in enumerate(pages, 1):
            # Split into paragraphs
            paragraphs = [p.strip() for p in page_text.split('\n\n') if p.strip()]
            
            output.append(f"| **Page {i}** | **第{i}页** |")
            
            for para in paragraphs:
                # Escape pipe characters in content
                para_escaped = para.replace('|', '\\|').replace('\n', ' ')
                output.append(f"| {para_escaped} | *[Translation needed]* |")
            
            output.append(f"| --- | --- |")
        
        return "\n".join(output)
    
    def _format_separate(self, pages: list[str]) -> str:
        """Separate sections bilingual format"""
        output = []
        
        # English section
        output.append(f"# {self.pdf_path.stem}\n")
        output.append("## English Version\n")
        
        for i, page_text in enumerate(pages, 1):
            output.append(f"### Page {i}\n")
            output.append(page_text)
            output.append("\n")
        
        output.append("\n---\n")
        output.append("---\n")
        output.append("---\n\n")
        
        # Chinese section
        output.append("## 中文版本\n")
        
        for i, page_text in enumerate(pages, 1):
            output.append(f"### 第{i}页\n")
            output.append("<!-- TODO: Add Chinese translation -->")
            output.append("<!-- 待翻译 -->\n")
        
        return "\n".join(output)
    
    def save_output(self, content: str, output_path: Path):
        """Save bilingual markdown to file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Saved to: {output_path}")
    
    def convert(self, output_dir: Path = None):
        """Main conversion workflow"""
        # Extract PDF
        pages = self.extract_pdf()
        
        # Create bilingual template
        print(f"📝 Creating bilingual template ({self.format_type} format)...")
        bilingual_content = self.create_bilingual_template(pages)
        
        # Determine output path
        if output_dir is None:
            output_dir = self.pdf_path.parent
        
        output_path = output_dir / f"{self.pdf_path.stem}_bilingual.md"
        
        # Save
        self.save_output(bilingual_content, output_path)
        
        print("\n" + "=" * 60)
        print("✓ Conversion complete!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Open the generated markdown file")
        print("2. Add Chinese translations in the marked sections")
        print("3. Review and adjust formatting as needed")
        print("4. Add explanatory notes if desired")
        
        return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Convert PDF to bilingual (English-Chinese) markdown"
    )
    parser.add_argument(
        "pdf_path",
        help="Path to the PDF file"
    )
    parser.add_argument(
        "--format",
        choices=["inline", "side-by-side", "separate"],
        default="inline",
        help="Bilingual format type (default: inline)"
    )
    parser.add_argument(
        "--output-dir",
        help="Output directory (default: same as PDF)"
    )
    
    args = parser.parse_args()
    
    # Validate PDF exists
    pdf_path = Path(args.pdf_path)
    if not pdf_path.exists():
        print(f"Error: PDF file not found: {pdf_path}")
        sys.exit(1)
    
    # Convert
    converter = PDFToBilingualConverter(args.pdf_path, args.format)
    output_dir = Path(args.output_dir) if args.output_dir else None
    converter.convert(output_dir)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("PDF to Bilingual Markdown Converter")
        print("=" * 60)
        print("\nUsage:")
        print("  python scripts/pdf_to_bilingual.py <pdf_path> [options]")
        print("\nOptions:")
        print("  --format {inline|side-by-side|separate}")
        print("  --output-dir <directory>")
        print("\nExamples:")
        print("  python scripts/pdf_to_bilingual.py courses/ml/slides/lecture1.pdf")
        print("  python scripts/pdf_to_bilingual.py lecture.pdf --format separate")
        print("\nFormats:")
        print("  inline:       English and Chinese in alternating sections")
        print("  side-by-side: Table format with parallel columns")
        print("  separate:     Complete English section, then Chinese section")
        sys.exit(0)
    
    main()
